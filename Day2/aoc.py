import operator


def do_op(operation, current_index, program):
    integers = program
    first_parameter = integers[integers[current_index+1]]
    second_parameter = integers[integers[current_index+2]]
    integers[integers[current_index+3]] = operation(first_parameter, second_parameter)
    return integers


def int_code(program):
    integers = program
    current_index = 0
    op_code = integers[current_index]
    while op_code != 99:
        if op_code != 1 and op_code != 2:
            return []
        elif op_code == 1
            operation = operator.add
        else:
            operation = operator.mul
        integers = do_op(operation, current_index, program)
        current_index += 4
        op_code = integers[current_index]
    return integers


def brute_force_result(program, desired_result):
    for i in range(0, 100):
        for j in range(0, 100):
            integers = program.copy()
            integers[1] = i
            integers[2] = j
            print(integers)
            result = int_code(integers)
            print(result)
            if result[0] == desired_result:
                return i, j
    return -1, -1


if __name__ == "__main__":
    with open("./input.txt") as file:
        program = list(map(int, file.readline().split(',')))
        print(brute_force_result(program, 19690720))
    print(program)