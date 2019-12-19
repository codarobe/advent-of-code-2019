import operator

class IntCode:
    def __init__(self, program):
        additional_memory = [0 for i in range(len(program) * 5 + 1000)]
        self.mem_start = len(program)
        self.program = program + additional_memory
        self.current_index = 0
        self.inputs = []
        self.awaiting_input = False
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
        if len(self.inputs) > 0 or self.awaiting_input:
            self.awaiting_input = False
            if len(self.inputs) > 0:
                value = self.inputs.pop(0)
            else:
                print("Please input a number: ")
                value = int(input())
            write_location = self.get_literal_from_value(self.program[self.current_index + 1], param_types[0])
            self.program[write_location] = value
            self.current_index += 2
        else:
            self.awaiting_input = True
            return

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
            elif op_code == 3 and self.awaiting_input:
                return None
            (op_code, param_types) = self.parse_op_code(self.program[self.current_index])
        self.is_halted = True
        return self.program

    def flush_outputs(self):
        self.outputs = []


class ArcadeGame:
    def __init__(self):
        self.grid = [[]]
        self.score = 0
        self.computer = None

    def extend_grid_if_needed(self, x_distance, y_distance):
        while y_distance+1 > len(self.grid):
            self.grid.append([0 for _ in self.grid[0]])
        while x_distance+1 > len(self.grid[-1]):
            difference = x_distance+1 - len(self.grid[-1])
            for row in self.grid:
                row.extend([0 for _ in range(difference)])

    def set_cell(self, x_distance, y_distance, tile_type):
        self.extend_grid_if_needed(x_distance, y_distance)
        self.grid[y_distance][x_distance] = tile_type

    def get_blocks_remaining(self):
        count = 0
        for row in self.grid:
            count += len(list(filter(lambda cell: cell == 2, row)))
        return count

    def find_symbol(self, symbol):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == symbol:
                    return x, y

    def get_x_of_ball(self):
        (x, _) = self.find_symbol(4)
        return x

    def get_x_of_paddle(self):
        (x, _) = self.find_symbol(3)
        return x

    def get_suggested_move(self):
        ball_x = self.get_x_of_ball()
        paddle_x = self.get_x_of_paddle()
        if paddle_x < ball_x:
            return 1
        elif paddle_x > ball_x:
            return -1
        else:
            return 0

    def update_grid(self):
        while not self.computer.is_halted:
            self.computer.run_program()
            if len(self.computer.outputs) == 3:
                (x, y, tile) = self.computer.outputs
                self.computer.flush_outputs()
                if x == -1 and y == 0:
                    self.score = tile
                else:
                    self.set_cell(x, y, tile)
            elif self.computer.awaiting_input:
                print("Your score: {}".format(self.score))
                self.print_grid()
                print("Computer is awaiting input")
                return

    def start_game(self):
        with open("./input.txt") as file:
            program = list(map(int, file.readline().split(',')))
        self.computer = IntCode(program)
        # computer.program[computer.mem_start] = 2
        self.computer.program[0] = 2
        self.computer.run_program()
        self.update_grid()
        print("Your score: {}".format(self.score))
        self.print_grid()
        print(self.get_blocks_remaining())

    def print_grid(self):
        for row in self.grid:
            line = ""
            for cell in row:
                if cell == 0:
                    line += " "
                elif cell == 1:
                    line += "#"
                elif cell == 2:
                    line += "X"
                elif cell == 3:
                    line += "-"
                elif cell == 4:
                    line += "o"
            print(line)


if __name__ == "__main__":
    game = ArcadeGame()
    game.start_game()

