import time
import operator


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "[{}, {}]".format(self.x, self.y)

    def __str__(self):
        return "[{}, {}]".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


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
        # print("Output: ", self.outputs[-1])
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


class HullPainter:
    def __init__(self, program):
        self.computer = IntCode(program)
        self.directions = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
        self.robot_symbols = ['^', '>', 'v', '<']
        self.robot_direction_index = 0  # begin facing up
        self.grid = [[0 for i in range(100)] for i in range(100)]
        self.robot_location = Point(len(self.grid[0]) // 2, len(self.grid) // 2)
        self.grid[self.robot_location.y][self.robot_location.x] = 1
        self.painted_locations = set()

    def is_done(self):
        return self.computer.is_halted

    def paint_location(self):
        # each iteration outputs the color (0:black, 1:white)
        # then outputs the direction
        if len(self.computer.outputs) > 1:
            self.grid[self.robot_location.y][self.robot_location.x] = self.computer.outputs[-2]
            self.painted_locations.add((self.robot_location.x, self.robot_location.y))

    def update_robot_direction(self):
        if len(self.computer.outputs) > 1:
            if self.computer.outputs[-1] == 0:
                # turn left
                self.robot_direction_index = (self.robot_direction_index - 1) % 4
            else:
                # turn right
                self.robot_direction_index = (self.robot_direction_index + 1) % 4

    def move_robot(self):
        direction = self.directions[self.robot_direction_index]
        self.robot_location.x += direction.x
        self.robot_location.y += direction.y

    def paint_and_move_robot(self):
        self.paint_location()
        self.update_robot_direction()
        self.move_robot()

    def process_next_inputs(self):
        output_count = len(self.computer.outputs)
        self.computer.inputs.append(self.grid[self.robot_location.y][self.robot_location.x])
        self.computer.run_program()

        if not self.is_done():
            self.computer.run_program()
            self.paint_and_move_robot()
        elif len(self.computer.outputs) > output_count:
            self.paint_location()

    def paint_ship(self, in_step=False):
        if in_step:
            self.print_grid()
            time.sleep(0.2)
        self.process_next_inputs()
        while not self.is_done():
            if in_step:
                self.print_grid()
                time.sleep(0.2)
            self.process_next_inputs()
        self.print_grid(with_robot=False)

    def print_grid(self, with_robot=True):
        for y in range(len(self.grid)):
            line = ""
            for x in range(len(self.grid[y])):
                if with_robot and self.robot_location.x == x and self.robot_location.y == y:
                    line += self.robot_symbols[self.robot_direction_index]
                elif self.grid[y][x] == 0:
                    line += '⬛'
                elif self.grid[y][x] == 1:
                    line += '⬜️'
            print(line)


if __name__ == "__main__":
    with open("./input.txt") as file:
        program = list(map(int, file.readline().split(',')))
    robot = HullPainter(program)
    robot.paint_ship(in_step=True)
    print(len(robot.painted_locations))

