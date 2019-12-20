from math import gcd

class BiDirectionalPair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __eq__(self, other):
        same = self.first == other.first and self.second == other.second
        reverse = self.first == other.second and self.second == other.first
        return same or reverse

    def __repr__(self):
        return "({}, {})".format(self.first, self.second)

    def __str__(self):
        return "({}, {})".format(self.first, self.second)

    def __hash__(self):
        return hash(self.first) + hash(self.second)


class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return "<x={}, y={}, z={}>".format(self.x, self.y, self.z)

    def __str__(self):
        return "<x={}, y={}, z={}>".format(self.x, self.y, self.z)

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y, self.z-other.z)

    def normalize(self):
        if self.x != 0:
            self.x //= abs(self.x)
        if self.y != 0:
            self.y //= abs(self.y)
        if self.z != 0:
            self.z //= abs(self.z)
        return self

    def as_tuple(self):
        return self.x, self.y, self.z


class SystemSimulation:
    def __init__(self, start_locations, start_velocities):
        self.start_locations = start_locations.copy()
        self.start_velocities = start_velocities.copy()
        self.moon_locations = start_locations.copy()
        self.moon_velocities = start_velocities.copy()
        self.moon_pairs = self.get_all_moon_pairs()
        self.current_time = 0

    def get_all_moon_pairs(self):
        pairs = set()
        for i in range(len(self.moon_locations)):
            for j in range(len(self.moon_locations)):
                pairs.add(BiDirectionalPair(i, j))
        return list(pairs)

    def update_velocities(self):
        velocity_changes = [Point() for _ in self.moon_velocities]
        for pair in self.moon_pairs:
            change_to_first = (self.moon_locations[pair.second] - self.moon_locations[pair.first]).normalize()
            change_to_second = (self.moon_locations[pair.first] - self.moon_locations[pair.second]).normalize()
            velocity_changes[pair.first] = velocity_changes[pair.first] + change_to_first
            velocity_changes[pair.second] = velocity_changes[pair.second] + change_to_second
        for i in range(len(self.moon_velocities)):
            self.moon_velocities[i] = self.moon_velocities[i] + velocity_changes[i]

    def update_positions(self):
        for i in range(len(self.moon_locations)):
            self.moon_locations[i] = self.moon_locations[i] + self.moon_velocities[i]

    def simulate_step(self):
        self.update_velocities()
        self.update_positions()
        self.current_time += 1

    def simulate_until_time(self, time):
        self.current_time = 0
        self.moon_velocities = self.start_velocities.copy()
        self.moon_locations = self.start_locations.copy()
        while self.current_time < time:
            self.simulate_step()

    def get_energy_of_system(self):
        total = 0
        for i in range(len(self.moon_locations)):
            total += self.get_energy_of_moon(self.moon_locations[i], self.moon_velocities[i])
        return total

    def get_energy_of_moon(self, location, velocity):
        potential_energy = sum(list(map(abs, location.as_tuple())))
        kinetic_energy = sum(list(map(abs, velocity.as_tuple())))
        return potential_energy * kinetic_energy

    def least_common_multiple(self, x, y, z):
        # greatest = max(x, y, z)
        # current = greatest
        # while current % x != 0 or current % y != 0 or current % z != 0:
        #     current += greatest
        # return current
        return (x * y * z) // gcd(x, gcd(y, z))

    def simulate_axes_until_loop(self):
        self.current_time = 0
        self.moon_velocities = self.start_velocities.copy()
        self.moon_locations = self.start_locations.copy()

        x_loop = 0
        y_loop = 0
        z_loop = 0

        while x_loop == 0 or y_loop == 0 or z_loop == 0:
            self.simulate_step()
            aggregate = Point()
            for velocity in self.moon_velocities:
                aggregate.x += abs(velocity.x)
                aggregate.y += abs(velocity.y)
                aggregate.z += abs(velocity.z)
            if x_loop == 0 and aggregate.x == 0:
                x_loop = self.current_time
            if y_loop == 0 and aggregate.y == 0:
                y_loop = self.current_time
            if z_loop == 0 and aggregate.z == 0:
                z_loop = self.current_time

        return self.least_common_multiple(x_loop, y_loop, z_loop)

    def print_moons(self):
        for i in range(len(self.moon_locations)):
            print("pos={}, vel={}".format(self.moon_locations[i], self.moon_velocities[i]))


def parse_position_from_text(text):
    (x, y, z) = text[1:-1].split(", ")
    x = int(x[2:])
    y = int(y[2:])
    z = int(z[2:])
    return Point(x, y, z)


if __name__ == "__main__":
    positions = []
    for line in open("./input.txt"):
        positions.append(parse_position_from_text(line.strip()))
    velocities = [Point() for _ in positions]
    simulation = SystemSimulation(positions, velocities)
    simulation.simulate_until_time(10)
    simulation.print_moons()
    print(simulation.get_energy_of_system())
    print(simulation.simulate_axes_until_loop() * 2)
