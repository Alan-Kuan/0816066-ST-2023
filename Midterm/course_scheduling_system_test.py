import unittest
from unittest.mock import patch
from course_scheduling_system import CSS

class Test(unittest.TestCase):
    @patch.object(CSS, 'check_course_exist', return_value=True)
    def test_q1_1(self, _):
        css = CSS()
        course = ('Software Testing', 'Thursday', 5, 7)

        added = css.add_course(course)
        self.assertTrue(added)

        course_list = css.get_course_list()
        self.assertEqual(len(course_list), 1)
        self.assertTupleEqual(course_list[0], course)

    @patch.object(CSS, 'check_course_exist', return_value=True)
    def test_q1_2(self, _):
        css = CSS()
        cases = [
            (('Software Testing', 'Thursday', 5, 7), True),
            (('Physics', 'Thursday', 7, 8), False)
        ]

        for case in cases:
            with self.subTest(f'add { case[0][0] }'):
                added = css.add_course(case[0])
                self.assertEqual(added, case[1])

        course_list = css.get_course_list()
        self.assertEqual(len(course_list), 1)
        self.assertTupleEqual(course_list[0], cases[0][0])

    @patch.object(CSS, 'check_course_exist', return_value=False)
    def test_q1_3(self, _):
        css = CSS()
        course = ('Software Testing', 'Thursday', 5, 7)

        added = css.add_course(course)
        self.assertFalse(added)

    @patch.object(CSS, 'check_course_exist', return_value=True)
    def test_q1_4(self, _):
        css = CSS()
        course = 'Software Testing'

        self.assertRaises(TypeError, css.add_course, course)

    @patch.object(CSS, 'check_course_exist', return_value=True)
    def test_q1_5(self, m_check_course_exist):
        css = CSS()
        courses = [
            ('Software Testing I', 'Monday', 5, 7),
            ('Software Testing II', 'Tuesday', 5, 7),
            ('Software Testing III', 'Wednesday', 5, 7)
        ]

        for course in courses:
            with self.subTest(f'add { course[0] }'):
                added = css.add_course(course)
                self.assertTrue(added)
        removed = css.remove_course(courses[1])
        self.assertTrue(removed)

        course_list = css.get_course_list()
        self.assertEqual(len(course_list), 2)
        self.assertTupleEqual(course_list[0], courses[0])
        self.assertTupleEqual(course_list[1], courses[2])

        self.assertEqual(m_check_course_exist.call_count, 4)

        print(css)
	
if __name__ == '__main__':  # pragma: no cover
    unittest.main()
