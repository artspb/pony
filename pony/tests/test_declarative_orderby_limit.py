import unittest
from pony.orm import *
from testutils import *

db = Database('sqlite', ':memory:')

class Student(db.Entity):
    name = Required(unicode)
    scholarship = Optional(int)
    group = Required(int)

db.generate_mapping(create_tables=True)

@with_transaction
def populate_db():
    Student(id=1, name="B", scholarship=None, group=41)
    Student(id=2, name="C", scholarship=700, group=41)
    Student(id=3, name="A", scholarship=500, group=42)
    Student(id=4, name="D", scholarship=500, group=43)
    Student(id=5, name="E", scholarship=700, group=42)
populate_db()

class TestOrderbyLimit(unittest.TestCase):
    def setUp(self):
        rollback()
    def tearDown(self):
        rollback()

    def test1(self):
        students = set(query(s for s in Student).orderby(Student.name))
        self.assertEqual(students, set([Student[3], Student[1], Student[2], Student[4], Student[5]]))
        
    def test2(self):
        students = set(query(s for s in Student).orderby(Student.name.asc))
        self.assertEqual(students, set([Student[3], Student[1], Student[2], Student[4], Student[5]]))
        
    def test3(self):
        students = set(query(s for s in Student).orderby(Student.id.desc))
        self.assertEqual(students, set([Student[5], Student[4], Student[3], Student[2], Student[1]]))
        
    def test4(self):
        students = set(query(s for s in Student).orderby(Student.scholarship.asc, Student.group.desc))
        self.assertEqual(students, set([Student[1], Student[4], Student[3], Student[5], Student[2]]))
        
    def test5(self):
        students = set(query(s for s in Student).orderby(Student.name).limit(3))
        self.assertEqual(students, set([Student[3], Student[1], Student[2]]))
        
    def test6(self):
        students = set(query(s for s in Student).orderby(Student.name).limit(3, 1))
        self.assertEqual(students, set([Student[1], Student[2], Student[4]]))
        
    def test7(self):
        q = query(s for s in Student).orderby(Student.name).limit(3, 1)
        students = set(q)
        self.assertEqual(students, set([Student[1], Student[2], Student[4]]))
        students = set(q)
        self.assertEqual(students, set([Student[1], Student[2], Student[4]]))
        
    @raises_exception(TypeError, "query.orderby() arguments must be attributes. Got: 'name'")
    def test8(self):
        students = query(s for s in Student).orderby("name")
        
    def test9(self):
        students = set(query(s for s in Student).orderby(Student.id)[1:4])
        self.assertEqual(students, set([Student[2], Student[3], Student[4]]))
        
    def test10(self):
        students = set(query(s for s in Student).orderby(Student.id)[:4])
        self.assertEqual(students, set([Student[1], Student[2], Student[3], Student[4]]))
        
    @raises_exception(TypeError, "Parameter 'stop' of slice object should be specified")
    def test11(self):
        students = query(s for s in Student).orderby(Student.id)[4:]
        
    @raises_exception(TypeError, "Parameter 'start' of slice object cannot be negative")
    def test12(self):
        students = query(s for s in Student).orderby(Student.id)[-3:2]
        
    def test13(self):
        students = query(s for s in Student).orderby(Student.id)[3]
        self.assertEqual(students, Student[4])
        
    @raises_exception(TypeError, "Incorrect argument type: 'a'")
    def test14(self):
        students = query(s for s in Student).orderby(Student.id)["a"]
        
    def test15(self):
        students = set(query(s for s in Student).orderby(Student.id)[0:4][1:3])
        self.assertEqual(students, set([Student[2], Student[3]]))
        
    def test16(self):
        students = set(query(s for s in Student).orderby(Student.id)[0:4][1:])
        self.assertEqual(students, set([Student[2], Student[3], Student[4]]))
        
    def test17(self):
        students = set(query(s for s in Student).orderby(Student.id)[:4][1:])
        self.assertEqual(students, set([Student[2], Student[3], Student[4]]))
        
    def test18(self):
        students = set(query(s for s in Student).orderby(Student.id)[:])
        self.assertEqual(students, set([Student[1], Student[2], Student[3], Student[4], Student[5]]))
        
if __name__ == "__main__":
    unittest.main()
