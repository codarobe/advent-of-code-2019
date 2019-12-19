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


def apply_move(current_x, current_y, current_length, points, move):
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
        current_length += 1
        if (current_x, current_y) not in points:
            points[(current_x, current_y)] = current_length
    return points, current_x, current_y, current_length


def apply_path(path):
    current_x = 0
    current_y = 0
    current_length = 0
    points = {}
    for move in path:
        (points, current_x, current_y, current_length) = apply_move(current_x, current_y, current_length, points, move)
    return points


def manhattan(path1, path2):
    print("Simulating Paths")
    first_points = apply_path(path1)
    second_points = apply_path(path2)
    intersections = set(first_points.keys()).intersection(set(second_points.keys()))
    minimum = None
    for intersection in intersections:
        combined_distance = first_points[intersection] + second_points[intersection]
        if minimum is None or combined_distance < minimum:
            minimum = combined_distance
    return minimum


if __name__ == "__main__":
    with open("./part2.txt") as file:
        firstPath = parse_path(file.readline().split(','))
        secondPath = parse_path(file.readline().split(','))
        minimum = manhattan(firstPath, secondPath)
        print(minimum)
