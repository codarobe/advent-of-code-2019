class Move:
    def __init__(self, item):
        self.direction = item[0]
        self.spaces = int(item[1:])

    def __repr__(self):
        return "[{}, {}]".format(self.direction, self.spaces)

    def __str__(self):
        return "[{}, {}]".format(self.direction, self.spaces)


NO_PATH_SYMBOL = "."
CENTER_PATH_SYMBOL = "o"
PATH_ONE_SYMBOL = "-"
PATH_TWO_SYMBOL = "|"
CROSS_SYMBOL = "X"

def parse_move(item):
    return item[0], int(item[1:])


def parse_path(path):
    return list(map(Move, path))


def get_total_spaces(path):
    return sum(move.spaces for move in path)


def apply_move(grid, current_x, current_y, center_x, center_y, move, symbol):
    # print(move)
    for space in range(move.spaces):
        if move.direction == "U":
            current_y -= 1
        elif move.direction == "D":
            current_y += 1
        elif move.direction == "L":
            current_x -= 1
        else:
            current_x += 1
        current_space = grid[current_y][current_x]
        if current_space == NO_PATH_SYMBOL:
            grid[current_y][current_x] = symbol
        elif (current_space != CENTER_PATH_SYMBOL
                and current_space != symbol):
            grid[current_y][current_x] = CROSS_SYMBOL
            print(abs(current_x - center_x) + abs(current_y - center_y))
    return grid, current_x, current_y


def apply_path(grid, center_x, center_y, path, symbol):
    current_x = center_x
    current_y = center_y
    for move in path:
        (grid, current_x, current_y) = apply_move(grid, current_x, current_y, center_x, center_y, move, symbol)
    return grid



def manhattan(path1, path2):
    size = max(get_total_spaces(firstPath), get_total_spaces(secondPath)) // 5
    print("Creating Board of size {} x {}".format(size, size))
    grid = [[NO_PATH_SYMBOL for col in range(size)] for row in range(size)]
    grid[size//2][size//2] = CENTER_PATH_SYMBOL
    print("Simulating Paths")
    grid = apply_path(grid, size//2, size//2, path1, PATH_ONE_SYMBOL)
    grid = apply_path(grid, size//2, size//2, path2, PATH_TWO_SYMBOL)
    print_grid(grid)


def print_grid(grid):
    for row in grid:
        line = ""
        for i in row:
            line += i
        print(line)


if __name__ == "__main__":
    with open("./part1.txt") as file:
        firstPath = parse_path(file.readline().split(','))
        secondPath = parse_path(file.readline().split(','))
        manhattan(firstPath, secondPath)
