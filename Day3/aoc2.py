class Move:
    def __init__(self, item):
        self.direction = item[0]
        self.spaces = int(item[1:])

    def __repr__(self):
        return "[{}, {}]".format(self.direction, self.spaces)

    def __str__(self):
        return "[{}, {}]".format(self.direction, self.spaces)


def parse_move(item):
    return item[0], int(item[1:])


def parse_path(path):
    return list(map(Move, path))


def apply_move(current_x, current_y, move):
    points = set()
    for space in range(move.spaces):
        if move.direction == "U":
            current_y -= 1
        elif move.direction == "D":
            current_y += 1
        elif move.direction == "L":
            current_x -= 1
        elif move.direction == "R":
            current_x += 1
        else:
            assert False
        points.add((current_x, current_y))
    return points, current_x, current_y


def apply_path(path):
    current_x = 0
    current_y = 0
    points = set()
    for move in path:
        (new_points, current_x, current_y) = apply_move(current_x, current_y, move)
        points.update(new_points)
    return points


def distance(point):
    (x, y) = point
    return abs(x) + abs(y)


def manhattan(path1, path2):
    print("Simulating Paths")
    first_points = apply_path(path1)
    second_points = apply_path(path2)
    return min(list(map(distance, list(first_points.intersection(second_points)))))


if __name__ == "__main__":
    with open("./part1.txt") as file:
        firstPath = parse_path(file.readline().split(','))
        secondPath = parse_path(file.readline().split(','))
        minimum = manhattan(firstPath, secondPath)
        print(minimum)
