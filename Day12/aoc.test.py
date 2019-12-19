import unittest
from Day12.aoc import Point, GravitySimulation


class MyTestCase(unittest.TestCase):
    def test_simulation_steps(self):
        # arrange
        start_positions = [Point(-1, 0, 2), Point(2, -10, -7), Point(4, -8, 8), Point(3, 5, -1)]
        start_velocities = [Point() for _ in start_positions]
        simulator = GravitySimulation(start_positions, start_velocities)
        expected_positions = [Point(2, 1, -3), Point(1, -8, 0), Point(3, -6, 1), Point(2, 0, 4)]
        expected_velocities = [Point(-3, -2, 1), Point(-1, 1, 3), Point(3, 2, -3), Point(1, -1, -1)]
        expected_time = 10
        expected_energy = 179

        # act
        simulator.update_moons_to_time(expected_time)

        # assert
        self.assertEqual(simulator.current_time, expected_time)
        self.assertEqual(simulator.moon_locations, expected_positions)
        self.assertEqual(simulator.moon_locations_over_time[expected_time], expected_positions)
        self.assertEqual(simulator.moon_velocities, expected_velocities)
        self.assertEqual(simulator.moon_velocities_over_time[expected_time], expected_velocities)
        self.assertEqual(simulator.get_energy_of_system(), expected_energy)
        self.assertEqual(simulator.get_energy_of_system_at_time(expected_time), expected_energy)

    def test_check_if_historical_state(self):
        start_locations = []
        stop_locations = []
        simulator = GravitySimulation()


if __name__ == '__main__':
    unittest.main()
