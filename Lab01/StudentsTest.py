import unittest
import Students

def get_mex(arr):
    mex = 0
    for x in sorted(arr):
        if x == mex:
            mex += 1
    return mex

class Test(unittest.TestCase):
    students = Students.Students()

    user_name = ['John', 'Mary', 'Thomas', 'Jane']
    user_id = []

    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        print('Start set_name test\n')

        for name in self.user_name:
            id = self.students.set_name(name)
            print(id, name)

            self.assertIsInstance(id, int)      # check its type
            self.assertGreaterEqual(id, 0)      # check its value's range
            self.assertNotIn(id, self.user_id)  # check its uniqueness

            self.user_id.append(id)

        print('\nFinish set_name test\n\n')

    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        print('Start get_name test\n')

        user_id_len = len(self.user_id)
        user_name_len = len(self.user_name)
        print('user_id length =', user_id_len)
        print('user_name length =', user_name_len)
        print()

        self.assertEqual(user_id_len, user_name_len)

        self.user_id.append(get_mex(self.user_id))
        self.user_name.append('There is no such user')

        for id, name in zip(self.user_id, self.user_name):
            print(f'id {id}: {name}')
            self.assertEqual(self.students.get_name(id), name)

        print('\nFinish get_name test')

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
