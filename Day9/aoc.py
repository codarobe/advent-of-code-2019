import itertools
import operator


class IntCode:
    def __init__(self, program):
        additional_memory = [0 for i in range(len(program) * 5 + 1000)]
        self.program = program + additional_memory
        self.current_index = 0
        self.inputs = []
        self.outputs = []
        self.is_halted = True
        self.relative_base = 0

    def parse_op_code(self, op_code):
        code = op_code % 100
        param_1_type = ((op_code - code) % 1000) // 100
        param_2_type = ((op_code - param_1_type - code) % 10000) // 1000
        param_3_type = ((op_code - param_2_type - param_1_type - code) % 100000) // 10000
        return code, (param_1_type, param_2_type, param_3_type)

    def get_parameter_from_value(self, value, param_type):
        if param_type == 0:
            return self.program[value]
        if param_type == 1:
            return value
        if param_type == 2:
            return self.program[value + self.relative_base]
        assert False, "Unsupported parameter type: {}".format(param_type)

    def get_literal_from_value(self, value, param_type):
        if param_type == 0 or param_type == 1:
            return value
        else:
            return value + self.relative_base

    def do_two_param_op_and_store(self, operation, param1, param2, write_location):
        self.program[write_location] = operation(param1, param2)
        self.current_index += 4

    def perform_op_and_store(self, op_code, param_types):
        if op_code == 1:
            operation = operator.add
        else:
            operation = operator.mul
        first_parameter = self.get_parameter_from_value(self.program[self.current_index + 1], param_types[0])
        second_parameter = self.get_parameter_from_value(self.program[self.current_index + 2], param_types[1])
        write_location = self.get_literal_from_value(self.program[self.current_index + 3], param_types[2])
        self.do_two_param_op_and_store(operation, first_parameter, second_parameter, write_location)

    def get_input_and_store_op(self, param_types):
        if len(self.inputs) > 0:
            value = self.inputs.pop(0)
        else:
            print("Please input a number: ")
            value = int(input())
        write_location = self.get_literal_from_value(self.program[self.current_index + 1], param_types[0])
        self.program[write_location] = value
        self.current_index += 2

    def output_value_op(self, param_types):
        self.outputs.append(self.get_parameter_from_value(self.program[self.current_index + 1], param_types[0]))
        print("Output: ", self.outputs[-1])
        self.current_index += 2

    def jump_if_true_op(self, param_types):
        compare_value = self.get_parameter_from_value(self.program[self.current_index + 1], param_types[0])
        jump_location = self.get_parameter_from_value(self.program[self.current_index + 2], param_types[1])
        if compare_value != 0:
            self.current_index = jump_location
        else:
            self.current_index += 3

    def jump_if_false_op(self, param_types):
        compare_value = self.get_parameter_from_value(self.program[self.current_index + 1], param_types[0])
        jump_location = self.get_parameter_from_value(self.program[self.current_index + 2], param_types[1])
        if compare_value != 0:
            self.current_index += 3
        else:
            self.current_index = jump_location

    def less_than_op(self, param_types):
        first_value = self.get_parameter_from_value(self.program[self.current_index + 1], param_types[0])
        second_value = self.get_parameter_from_value(self.program[self.current_index + 2], param_types[1])
        write_location = self.get_literal_from_value(self.program[self.current_index + 3], param_types[2])
        self.program[write_location] = 1 if first_value < second_value else 0
        self.current_index += 4

    def equals_op(self, param_types):
        first_value = self.get_parameter_from_value(self.program[self.current_index + 1], param_types[0])
        second_value = self.get_parameter_from_value(self.program[self.current_index + 2], param_types[1])
        write_location = self.get_literal_from_value(self.program[self.current_index + 3], param_types[2])
        self.program[write_location] = 1 if first_value == second_value else 0
        self.current_index += 4

    def adjust_relative_base_op(self, param_types):
        first_value = self.get_parameter_from_value(self.program[self.current_index + 1], param_types[0])
        self.relative_base += first_value
        self.current_index += 2

    def handle_valid_op(self, op_code, param_types):
        if op_code == 1 or op_code == 2:
            # print("Add or Multiply")
            self.perform_op_and_store(op_code, param_types)
        elif op_code == 3:
            # print("Get Input")
            self.get_input_and_store_op(param_types)
        elif op_code == 4:
            # print("Output Value")
            self.output_value_op(param_types)
        elif op_code == 5:
            # print("Jump if True")
            self.jump_if_true_op(param_types)
        elif op_code == 6:
            # print("Jump if False")
            self.jump_if_false_op(param_types)
        elif op_code == 7:
            # print("Less Than")
            self.less_than_op(param_types)
        elif op_code == 8:
            # print("Equals")
            self.equals_op(param_types)
        elif op_code == 9:
            # print("Adjust Relative Base", op_code, param_types)
            self.adjust_relative_base_op(param_types)
        else:
            assert False, "Unsupported Op-Code {}".format(op_code)

    def run_program(self):
        op_code_before_parse = self.program[self.current_index]
        (op_code, param_types) = self.parse_op_code(op_code_before_parse)
        # print("Op: {} => {}, {}".format(op_code_before_parse, op_code, param_types))
        while op_code != 99:
            self.is_halted = False
            self.handle_valid_op(op_code, param_types)
            if op_code == 4:
                return self.outputs[-1]
            (op_code, param_types) = self.parse_op_code(self.program[self.current_index])
        self.is_halted = True
        return self.program


class Amplifier:
    def __init__(self, program, setting):
        self.setting = setting
        self.computer = IntCode(program.copy())

    def begin_execution(self, input_value):
        self.computer.inputs = [self.setting, input_value]
        self.computer.run_program()
        return self.computer.outputs[-1]

    def resume_execution(self, input_value):
        self.computer.inputs.append(input_value)
        self.computer.run_program()
        return self.computer.outputs[-1]


class AmplifierChain:
    def __init__(self, program, settings_list):
        self.program = program
        self.settings_list = settings_list
        self.amplifiers = []
        for i in range(5):
            self.amplifiers.append(Amplifier(program, settings_list[i]))

    def execute_chain(self):
        result = self.amplifiers[0].begin_execution(0)
        result = self.amplifiers[1].begin_execution(result)
        result = self.amplifiers[2].begin_execution(result)
        result = self.amplifiers[3].begin_execution(result)
        return self.amplifiers[4].begin_execution(result)

    def resume_chain(self, starting_value):
        result = self.amplifiers[0].resume_execution(starting_value)
        result = self.amplifiers[1].resume_execution(result)
        result = self.amplifiers[2].resume_execution(result)
        result = self.amplifiers[3].resume_execution(result)
        return self.amplifiers[4].resume_execution(result)

    def execute_feedback_loop(self):
        result = self.execute_chain()
        while not self.amplifiers[4].computer.is_halted:
            result = self.resume_chain(result)
        return result


class MaxAmplifiedOutputAcrossPermutations:
    def __init__(self, program, settings_list):
        self.program = program
        self.settings_list = settings_list

    def get_from_single_pass(self):
        permutations = list(itertools.permutations(self.settings_list))
        max_result = -1000
        for permutation in permutations:
            chain = AmplifierChain(self.program, permutation)
            result = chain.execute_chain()
            max_result = max(max_result, result)
        return max_result

    def get_from_feedback_loop(self):
        permutations = list(itertools.permutations(self.settings_list))
        max_result = -1000
        for permutation in permutations:
            chain = AmplifierChain(self.program, permutation)
            result = chain.execute_feedback_loop()
            max_result = max(max_result, result)
        return max_result


if __name__ == "__main__":
    with open("../Day9/input.txt") as file:
        program = list(map(int, file.readline().split(',')))
    computer = IntCode(program)
    computer.run_program()
    while not computer.is_halted:
        # print(computer.current_index, computer.program[computer.current_index:])
        computer.run_program()
    print("Halted with final output: {}".format(computer.outputs[-1]))
    # print(computer.program)
