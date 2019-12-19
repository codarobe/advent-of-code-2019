import operator


class IntCode:
    def __init__(self):
        self.program = []
        self.current_index = 0

    def parse_op_code(self, op_code):
        code = op_code % 100
        param_1_type = ((op_code - code) % 1000) // 100
        param_2_type = ((op_code - param_1_type - code) % 10000) // 1000
        param_3_type = ((op_code - param_2_type - param_1_type - code) % 100000) // 10000
        return code, (param_1_type, param_2_type, param_3_type)

    def get_parameter_from_value(self, value, param_type):
        return value if param_type == 1 else self.program[value]

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
        write_location = self.program[self.current_index + 3]
        self.do_two_param_op_and_store(operation, first_parameter, second_parameter, write_location)

    def get_input_and_store_op(self):
        print("Please input a number: ")
        value = int(input())
        write_location = self.program[self.current_index + 1]
        self.program[write_location] = value
        self.current_index += 2

    def output_value_op(self, param_types):
        output = self.get_parameter_from_value(self.program[self.current_index + 1], param_types[0])
        print("Output: {}".format(output))
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
        write_location = self.program[self.current_index + 3]
        self.program[write_location] = 1 if first_value < second_value else 0
        self.current_index += 4

    def equals_op(self, param_types):
        first_value = self.get_parameter_from_value(self.program[self.current_index + 1], param_types[0])
        second_value = self.get_parameter_from_value(self.program[self.current_index + 2], param_types[1])
        write_location = self.program[self.current_index + 3]
        self.program[write_location] = 1 if first_value == second_value else 0
        self.current_index += 4

    def handle_valid_op(self, op_code, param_types):
        if op_code == 1 or op_code == 2:
            self.perform_op_and_store(op_code, param_types)
        elif op_code == 3:
            self.get_input_and_store_op()
        elif op_code == 4:
            self.output_value_op(param_types)
        elif op_code == 5:
            self.jump_if_true_op(param_types)
        elif op_code == 6:
            self.jump_if_false_op(param_types)
        elif op_code == 7:
            self.less_than_op(param_types)
        elif op_code == 8:
            self.equals_op(param_types)
        else:
            assert False, "Unsupported Op-Code {}".format(op_code)

    def run_program(self, program):
        self.program = program
        self.current_index = 0
        (op_code, param_types) = self.parse_op_code(self.program[self.current_index])
        while op_code != 99:
            self.handle_valid_op(op_code, param_types)
            (op_code, param_types) = self.parse_op_code(self.program[self.current_index])
        return self.program


if __name__ == "__main__":
    with open("./part1.txt") as file:
        program = list(map(int, file.readline().split(',')))
    # program = [3, 0, 4, 0, 99]
    program = IntCode().run_program(program)
    print(program)
