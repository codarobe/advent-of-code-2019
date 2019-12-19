class BiDirectionalPair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __eq__(self, other):
        same_order = self.first == other.first and self.second == other.second
        reverse_order = self.first == other.second and self.second == other.first
        return same_order or reverse_order

    def __hash__(self):
        return hash(self.first) + hash(self.second)

    def __repr__(self):
        return "({}, {})".format(self.first, self.second)


class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def to_tuple(self):
        return self.x, self.y, self.z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return "<x={}, y={}, z={}>".format(self.x, self.y, self.z)

    def __str__(self):
        return "<x={}, y={}, z={}>".format(self.x, self.y, self.z)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


class GravitySimulation:
    def __init__(self, initial_locations_as_points, initial_velocities_as_points):
        self.moon_locations = initial_locations_as_points
        self.moon_velocities = initial_velocities_as_points
        self.moon_pairs = self.get_all_moon_pairs()
        self.moon_locations_over_time = [self.moon_locations.copy()]
        self.moon_velocities_over_time = [self.moon_velocities.copy()]
        self.system_energy_over_time = {self.get_energy_of_system(): [0]}
        self.is_in_historical_state = False
        self.current_time = 0

    def get_all_moon_pairs(self):
        pairs = set()
        for i in range(len(self.moon_locations)):
            for j in range(len(self.moon_locations)):
                if i != j:
                    pairs.add(BiDirectionalPair(i, j))
        return list(pairs)

    def get_change_in_axis(self, first_axis, second_axis):
        if first_axis == second_axis:
            return 0
        elif first_axis > second_axis:
            return -1
        else:
            return 1

    def get_change_in_velocity(self, first_point, second_point):
        delta_x = self.get_change_in_axis(first_point.x, second_point.x)
        delta_y = self.get_change_in_axis(first_point.y, second_point.y)
        delta_z = self.get_change_in_axis(first_point.z, second_point.z)
        return Point(delta_x, delta_y, delta_z)

    def update_velocities(self):
        velocity_changes = [Point() for i in range(len(self.moon_velocities))]
        for pair in self.moon_pairs:
            first_location = self.moon_locations[pair.first]
            second_location = self.moon_locations[pair.second]
            velocity_changes[pair.first] += self.get_change_in_velocity(first_location, second_location)
            velocity_changes[pair.second] += self.get_change_in_velocity(second_location, first_location)

        for i in range(len(velocity_changes)):
            self.moon_velocities[i] += velocity_changes[i]

    def apply_velocities(self):
        for i in range(len(self.moon_velocities)):
            self.moon_locations[i] += self.moon_velocities[i]

    def update_moons(self):
        self.update_velocities()
        self.apply_velocities()
        self.current_time += 1
        self.moon_locations_over_time.append(self.moon_locations.copy())
        self.moon_velocities_over_time.append(self.moon_velocities.copy())

        energy = self.get_energy_of_system()
        if energy in self.system_energy_over_time.keys():
            self.check_if_historical_state(energy)
            self.system_energy_over_time[energy].append(self.current_time)
        else:
            self.is_in_historical_state = False
            self.system_energy_over_time[energy] = [self.current_time]

    def update_moons_to_time(self, time):
        for i in range(time):
            self.update_moons()

    def is_historic_state(self, time):
        for i in range(len(self.moon_locations)):
            if self.moon_locations[i] != self.moon_locations_over_time[time][i]:
                return False
            if self.moon_velocities[i] != self.moon_velocities_over_time[time][i]:
                return False
        return True

    def check_if_historical_state(self, energy):
        potential_matches = self.system_energy_over_time[energy]
        self.is_in_historical_state = False
        for potential_match in potential_matches:
            self.is_in_historical_state = self.is_in_historical_state or self.is_historic_state(potential_match)

    def simulate_system_until_history_repeats(self):
        while not self.is_in_historical_state:
            self.update_moons()
            if (self.current_time % 100000) == 0:
                print(self.current_time)

    def get_energy_of_moon_at_time(self, time, i):
        moon_position = self.moon_locations_over_time[time][i]
        moon_velocity = self.moon_velocities_over_time[time][i]
        potential_energy = abs(moon_position.x) + abs(moon_position.y) + abs(moon_position.z)
        kinetic_energy = abs(moon_velocity.x) + abs(moon_velocity.y) + abs(moon_velocity.z)
        return potential_energy * kinetic_energy

    def get_energy_of_system_at_time(self, time):
        total = 0
        for i in range(len(self.moon_locations_over_time[time])):
            total += self.get_energy_of_moon_at_time(time, i)
        return total

    def get_energy_of_moon(self, i):
        moon_position = self.moon_locations[i]
        moon_velocity = self.moon_velocities[i]
        potential_energy = abs(moon_position.x) + abs(moon_position.y) + abs(moon_position.z)
        kinetic_energy = abs(moon_velocity.x) + abs(moon_velocity.y) + abs(moon_velocity.z)
        return potential_energy * kinetic_energy

    def get_energy_of_system(self):
        total = 0
        for i in range(len(self.moon_locations)):
            total += self.get_energy_of_moon(i)
        return total

    def print_positions_and_velocities_at_time(self, time):
        for i in range(len(self.moon_locations)):
            print("pos={}, vel={}".format(self.moon_locations_over_time[time][i], self.moon_velocities_over_time[time][i]))

    def print_positions_and_velocities(self):
        for i in range(len(self.moon_locations)):
            print("pos={}, vel={}".format(self.moon_locations[i], self.moon_velocities[i]))


def parse_input_to_point(line):
    (x, y, z) = line[1:-1].split(', ')
    x = int(x[2::])
    y = int(y[2::])
    z = int(z[2::])
    return Point(x, y, z)


if __name__ == "__main__":
    start_locations = []
    start_velocities = []
    for line in open("./input.txt"):
        start_locations.append(parse_input_to_point(line.strip()))
        start_velocities.append(Point())
    simulation = GravitySimulation(start_locations, start_velocities)
    simulation.simulate_system_until_history_repeats()
    print(simulation.current_time)

    # steps_to_simulate = 1000
    # simulation.update_moons_to_time(steps_to_simulate)
    # for i in range(0, steps_to_simulate + 1, 1):
    # print("After {} steps:".format(i))
    # simulation.print_positions_and_velocities_at_time(i)
    # print()
    # print("Energy at {} steps: {}".format(steps_to_simulate, simulation.get_energy_of_system_at_time(steps_to_simulate)))


