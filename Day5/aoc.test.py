import unittest
from unittest.mock import patch
from Day5.aoc import IntCode


class IntCodeTests(unittest.TestCase):
    def setUp(self):
        self.computer = IntCode()

    def test_day_2_operations(self):
        # map program to expected output
        test_programs = []
        expected_results = []

        test_program_1 = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
        expected_result_1 = [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
        test_programs.append(test_program_1)
        expected_results.append(expected_result_1)

        test_program_2 = [1, 0, 0, 0, 99]
        expected_result_2 = [2, 0, 0, 0, 99]
        test_programs.append(test_program_2)
        expected_results.append(expected_result_2)

        test_program_3 = [2, 3, 0, 3, 99]
        expected_result_3 = [2, 3, 0, 6, 99]
        test_programs.append(test_program_3)
        expected_results.append(expected_result_3)

        test_program_4 = [2, 4, 4, 5, 99, 0]
        expected_result_4 = [2, 4, 4, 5, 99, 9801]
        test_programs.append(test_program_4)
        expected_results.append(expected_result_4)

        test_program_5 = [1, 1, 1, 4, 99, 5, 6, 0, 99]
        expected_result_5 = [30, 1, 1, 4, 2, 5, 6, 0, 99]
        test_programs.append(test_program_5)
        expected_results.append(expected_result_5)

        for i in range(len(test_programs)):
            with self.subTest("Test Day2 Program Output for: {}".format(test_programs[i])):
                actual_result = self.computer.run_program(test_programs[i])
                self.assertEqual(actual_result, expected_results[i])

    @patch('builtins.input', lambda *args: '10')
    def test_day_5_operations(self):
        # map program to expected output
        test_program = [3, 0, 4, 0, 99]
        expected_result = [10, 0, 4, 0, 99]

        actual_result = self.computer.run_program(test_program)
        self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
    unittest.main()
