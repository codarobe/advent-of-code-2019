from functools import partial
from math import gcd, inf


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

    def get_reduced_slope_to_point(self, other):
        delta_x = other.x - self.x
        delta_y = other.y - self.y
        if delta_x != 0 and delta_y != 0:
            divisor = abs(gcd(delta_y, delta_x))
            if divisor != 0:
                delta_x //= divisor
                delta_y //= divisor
        if delta_x == 0:
            delta_y //= abs(delta_y)
        if delta_y == 0:
            delta_x //= abs(delta_x)
        return delta_x, delta_y


def parse_slope_from_deltas(delta_tuple):
    (delta_x, delta_y) = delta_tuple
    if delta_x == 0 and delta_y != 0:
        return inf if delta_y > 0 else -inf
    return delta_y / delta_x


class AsteroidBlaster:
    def __init__(self, grid, ):
        self.grid = grid
        self.asteroids = self.get_asteroids_from_grid()

    def get_asteroids_from_grid(self):
        asteroids = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] != ".":
                    asteroids.append(Point(j, i))
        return asteroids

    def get_all_firing_directions_from_station_ordered(self):
        (_, station_point) = self.get_max_asteroid()
        slopes = set()
        for asteroid in self.asteroids:
            if station_point != asteroid:
                (delta_x, delta_y) = station_point.get_reduced_slope_to_point(asteroid)
                slopes.add((delta_x, delta_y))
                slopes.add((-delta_x, delta_y))
                slopes.add((delta_x, -delta_y))
                slopes.add((-delta_x, -delta_y))
        first_half = sorted(list(filter(lambda p: p[0] >= 0, slopes)), key=parse_slope_from_deltas)
        # print(first_half)
        second_half = sorted(list(filter(lambda p: p[0] < 0, slopes)), key=parse_slope_from_deltas)
        # print(second_half)
        return first_half + second_half

    def get_first_asteroid_in_direction(self, source_point, delta_x, delta_y):
        current_point = Point(source_point.x + delta_x, source_point.y + delta_y)
        while 0 <= current_point.y < len(self.grid) and 0 <= current_point.x < len(self.grid[0]):
            cell = self.grid[current_point.y][current_point.x]
            if cell != ".":
                return current_point
            current_point.x += delta_x
            current_point.y += delta_y
        return None

    def has_line_of_sight(self, source_point, target_point):
        if source_point == target_point:
            return False
        (delta_x, delta_y) = source_point.get_reduced_slope_to_point(target_point)
        asteroid = self.get_first_asteroid_in_direction(source_point, delta_x, delta_y)
        if asteroid is not None and asteroid == target_point:
            return True
        return False

    def print_grid(self):
        for row in self.grid:
            line = ""
            for item in row:
                line += "{:>3}   ".format(item)
            print(line)

    def populate_number_of_asteroids_visible_by_potential_stations(self):
        grid_copy = self.grid.copy()
        for asteroid in self.asteroids:
            func = partial(self.has_line_of_sight, asteroid)
            asteroids_in_sight = list(filter(func, self.asteroids))
            grid_copy[asteroid.y][asteroid.x] = str(len(asteroids_in_sight))
        return grid_copy

    def get_max_asteroid(self):
        grid_copy = self.populate_number_of_asteroids_visible_by_potential_stations()
        max_value = 0
        station_point = Point(0, 0)
        for i in range(len(grid_copy)):
            for j in range(len(grid_copy[i])):
                cell = grid_copy[i][j]
                if cell != '.' and int(cell) > max_value:
                    max_value = int(cell)
                    station_point = Point(j, i)
        return max_value, station_point

    def blast_asteroid(self, asteroid):
        self.grid[asteroid.y][asteroid.x] = '.'


if __name__ == "__main__":
    grid = []
    for line in open("./input.txt"):
        grid.append([char for char in line.strip()])
    blaster = AsteroidBlaster(grid)
    (max_value, _) = blaster.get_max_asteroid()
    blaster.print_grid()
    print(max_value)

    asteroids_destroyed = []
    (_, station) = blaster.get_max_asteroid()
    directions = blaster.get_all_firing_directions_from_station_ordered()
    while len(blaster.get_asteroids_from_grid()) > 1:
        for direction in directions:
            asteroid = blaster.get_first_asteroid_in_direction(station, direction[0], direction[1])
            if asteroid is not None:
                blaster.blast_asteroid(asteroid)
                asteroids_destroyed.append(asteroid)
                print("----------------------------------------------")
                blaster.print_grid()
    print(asteroids_destroyed[199])
