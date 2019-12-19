def calculate_fuel(mass):
    return int(mass / 3.0) - 2


def calculate_total_needed_fuel_for_mass(mass):
    total = 0
    fuel = calculate_fuel(mass)
    while fuel > 0:
        total += fuel
        fuel = calculate_fuel(fuel)
    return total


if __name__ == "__main__":
    total = 0
    for line in open("./input.txt"):
        total += calculate_total_needed_fuel_for_mass(int(line))
    print(total)
