import unittest
from unittest.mock import patch
from Day7.aoc import IntCode, AmplifierChain, MaxAmplifiedOutputAcrossPermutations


class IntCodeTests(unittest.TestCase):

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
                computer = IntCode(test_programs[i])
                actual_result = computer.run_program()
                self.assertEqual(actual_result, expected_results[i])

    def test_day_5_operations(self):
        # map program to expected output
        test_program = [3, 0, 4, 0, 99]
        expected_result = [10, 0, 4, 0, 99]

        computer = IntCode(test_program)
        computer.inputs = [10]
        computer.run_program()
        actual_result = computer.program
        self.assertEqual(actual_result, expected_result)

    def test_day_7_part_1(self):
        test_program = [3, 8, 1001, 8, 10, 8, 105, 1, 0, 0, 21, 46, 59, 84, 93, 102, 183, 264, 345, 426, 99999, 3, 9, 1002, 9, 4, 9, 1001, 9, 3, 9, 102, 2, 9, 9, 1001, 9, 5, 9, 102, 3, 9, 9, 4, 9, 99, 3, 9, 1002, 9, 3, 9, 101, 4, 9, 9, 4, 9, 99, 3, 9, 1002, 9, 4, 9, 1001, 9, 4, 9, 102, 2, 9, 9, 1001, 9, 2, 9, 1002, 9, 3, 9, 4, 9, 99, 3, 9, 1001, 9, 5, 9, 4, 9, 99, 3, 9, 1002, 9, 4, 9, 4, 9, 99, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 99, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 99, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 99]
        expected_result = 47064

        driver = MaxAmplifiedOutputAcrossPermutations(test_program, [0, 1, 2, 3, 4])
        actual_result = driver.get_from_single_pass()
        self.assertEqual(actual_result, expected_result)

    def test_day_7_part_2(self):
        test_program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
        expected_result = 139629729

        driver = MaxAmplifiedOutputAcrossPermutations(test_program, [5, 6, 7, 8, 9])
        actual_result = driver.get_from_feedback_loop()
        self.assertEqual(actual_result, expected_result)

        test_program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
        expected_result = 18216

        driver = MaxAmplifiedOutputAcrossPermutations(test_program, [5, 6, 7, 8, 9])
        actual_result = driver.get_from_feedback_loop()
        self.assertEqual(actual_result, expected_result)

        test_program = [3,8,1001,8,10,8,105,1,0,0,21,46,59,84,93,102,183,264,345,426,99999,3,9,1002,9,4,9,1001,9,3,9,102,2,9,9,1001,9,5,9,102,3,9,9,4,9,99,3,9,1002,9,3,9,101,4,9,9,4,9,99,3,9,1002,9,4,9,1001,9,4,9,102,2,9,9,1001,9,2,9,1002,9,3,9,4,9,99,3,9,1001,9,5,9,4,9,99,3,9,1002,9,4,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99]
        expected_result = 4248984

        driver = MaxAmplifiedOutputAcrossPermutations(test_program, [5, 6, 7, 8, 9])
        actual_result = driver.get_from_feedback_loop()
        self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
    unittest.main()

