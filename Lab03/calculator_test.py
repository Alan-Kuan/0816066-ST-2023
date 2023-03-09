import unittest
from calculator import Calculator

calc = Calculator()


def run_test(testcase, func, valid, invalid):
    func_name = func.__name__

    for args, ans in valid:
        call_body = str(args).replace(',)', ')')
        print(f'{ func_name }{ call_body } = { ans }')
        res = func(*args)
        testcase.assertEqual(res, ans)

    args, ex = invalid
    call_body = str(args).replace(',)', ')')
    print(f'{ func_name }{ call_body } raises { ex.__name__ }')
    testcase.assertRaises(ex, func, *args)

    print()


class ApplicationTest(unittest.TestCase):

    def test_add(self):
        valid = [
            ((1, 2), 3),
            ((4, 5), 9),
            ((0, 0), 0),
            ((1, 1), 2),
            ((4, 1), 5),
        ]
        invalid = ((1, '0'), TypeError)
        run_test(self, calc.add, valid, invalid)

    def test_divide(self):
        valid = [
            ((1, 1), 1),
            ((2, 2), 1),
            ((3, 3), 1),
            ((6, 2), 3),
            ((4, 1), 4),
        ]
        invalid = ((1, 0), ZeroDivisionError)
        run_test(self, calc.divide, valid, invalid)

    def test_sqrt(self):
        valid = [
            ((1,), 1),
            ((4,), 2),
            ((9,), 3),
            ((16,), 4),
            ((25,), 5),
        ]
        invalid = ((-1,), ValueError)
        run_test(self, calc.sqrt, valid, invalid)

    def test_exp(self):
        valid = [
            ((0,), 1),
            ((1,), 2.718281828459045),
            ((2,), 7.38905609893065),
            ((3,), 20.085536923187668),
            ((4,), 54.598150033144236),
        ]
        invalid = (('1',), TypeError)
        run_test(self, calc.exp, valid, invalid)


if __name__ == '__main__':
    unittest.main()
