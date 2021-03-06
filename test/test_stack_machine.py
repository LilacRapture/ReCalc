import re_calc.stack_machine as stack_machine
from re_calc.exceptions import MathException, CalcException
from re_calc.meta_containers import set_meta_indices

import unittest


class TestStackMachine(unittest.TestCase):

    def test_stack_machine(self):
        rpn_list = [1.0, 2.0, '+', 3.0, '/']
        result = stack_machine.calculate(rpn_list)
        expected_result = 1.0
        self.assertEqual(expected_result, result)

    def test_right_associativity(self):
        rpn_list = [1.0, 1.0, '+', 2.0, '^']
        result = stack_machine.calculate(rpn_list)
        expected_result = 4.0
        self.assertEqual(expected_result, result)

    def test_function(self):
        rpn_list = [1.0, 27.0, 3.0, 'log', '+']
        result = stack_machine.calculate(rpn_list)
        expected_result = 4.0
        self.assertEqual(expected_result, result)

    def test_function_with_power(self):
        rpn_list = [2.0, 27.0, 3.0, 'log', '^']
        result = stack_machine.calculate(rpn_list)
        expected_result = 8.0
        self.assertEqual(expected_result, result)

    def test_function_with_double_power(self):
        rpn_list = [3.0, 9.0, 3.0, 'log', 2.0, '^', '^']
        result = stack_machine.calculate(rpn_list)
        expected_result = 81.0
        self.assertEqual(expected_result, result)

    def test_sin(self):
        rpn_list = [30.0, 'sin']
        result = stack_machine.calculate(rpn_list)
        self.assertEqual(-0.9880316240928618, result)

    def test_cos(self):
        rpn_list = [30.0, 'cos']
        result = stack_machine.calculate(rpn_list)
        self.assertEqual(0.15425144988758405, result)

    def test_tan(self):
        rpn_list = [30.0, 'tan']
        result = stack_machine.calculate(rpn_list)
        self.assertEqual(-6.405331196646276, result)

    def test_atan(self):
        rpn_list = [30.0, 'atan']
        result = stack_machine.calculate(rpn_list)
        self.assertEqual(1.5374753309166493, result)

    def test_factorial(self):
        rpn_list = [10.0, 'factorial']
        result = stack_machine.calculate(rpn_list)
        self.assertEqual(3628800, result)

    def test_get_arity(self):
        def fun_two_args(a, b): return a + b
        def fun_three_args(a, b, c): return a ** 2 + b ** 2 == c ** 2
        self.assertEqual(2, stack_machine.get_arity(fun_two_args))
        self.assertEqual(3, stack_machine.get_arity(fun_three_args))

    def test_unary_operator(self):
        rpn_list = [4.0, 'sqrt']
        result = stack_machine.calculate(rpn_list)
        self.assertEqual(result, 2.0)

    def test_abs(self):
        rpn_list = [1.0, -2.0, 'abs', '-']
        result = stack_machine.calculate(rpn_list)
        self.assertEqual(-1.0, result)

    def test_divide_by_zero(self):
        rpn_list = [1.0, 0.0, '/']
        with self.assertRaisesRegex(MathException, "Division by zero"):
            stack_machine.calculate(rpn_list)

    def test_log_error(self):
        rpn_list = [-1.0, 1.0, 'log']
        with self.assertRaisesRegex(MathException, "Out of log function domain"):
            stack_machine.calculate(rpn_list)

    def test_invalid_expression_operators(self):
        rpn_list = set_meta_indices([1.0, '+', '+'])
        with self.assertRaisesRegex(CalcException, "Invalid expression"):
            stack_machine.calculate(rpn_list)

    def test_invalid_expression_operands(self):
        rpn_list = set_meta_indices([1.0, 1.0, 1.0, '+'])
        with self.assertRaisesRegex(CalcException, "Invalid expression"):
            stack_machine.calculate(rpn_list)

    def test_invalid_expression_operands_reverse(self):
        rpn_list = set_meta_indices(['+', 1.0, 1.0, 1.0])
        with self.assertRaisesRegex(CalcException, "Invalid expression"):
            stack_machine.calculate(rpn_list)
