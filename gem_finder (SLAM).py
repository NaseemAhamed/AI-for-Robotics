"""
 === Introduction ===

   The assignment is broken up into three parts.

   Part A:

        Create a SLAM implementation to process a series of landmark (gem) measurements and movement updates.
        The movements are defined for you so there are no decisions for you to make, you simply process the movements
        given to you.

        Hint: A planner with an unknown number of motions works well with an online version of SLAM.

    Part B:

        Here you will create the action planner for the robot.  The returned actions will be executed with the goal
        being to navigate to and extract a list of needed gems from the environment.  You will earn points by
        successfully extracting the list of gems from the environment.
        Example Actions (more explanation below):
            'move 3.14 1'
            'extract B'

    Part C:

        The only addition for part C will be to provide more information upon issuing the extract action.  The extra
        information will be the location of the gem you are attempting to extract.  The extra data will be compared
        to the real locations and you will be given points based on how close your estimates are to the real values.
        Example Action (more explanation below):
            'extract B 1.5 -0.2'

    Note: All of your estimates should be given relative to your robot's starting location.

    Details:

    - Start position
      - The robot will land at an unknown location on the map, however, you can represent this starting location
        as (0,0), so all future robot location estimates will be relative to this starting location.

    - Measurements
      - Measurements will come from gems located throughout the terrain.
        * The format is {'landmark id':{'distance':0.0, 'bearing':0.0, 'type':'D'}, ...}
      - All gems on the terrain will return a measurement.

    - Movements
      - Action: 'move 1.570963 1.0'
        * The robot will turn counterclockwise 90 degrees and then move 1.0
      - Movements are stochastic due to, well, it being a robot.
      - If max distance or steering is exceeded, the robot will not move.

    - Needed Gems
      - Provided as list of gem types: ['A', 'B', 'L', ...]
      - Although the gem names aren't real, as a convenience there are 26 total names, each represented by an
        upper case letter of the alphabet (ABC...).
      - Action: 'extract'
        * The robot will attempt to extract a specified gem from the current location..
      - When a gem is extracted from the terrain, it no longer exists in the terrain, and thus won't return a
        measurement.
      - The robot must be with 0.25 distance to successfully extract a gem.
      - There may be gems in the environment which are not required to be extracted, which means you could extract
        them if you so desire, however, I advise you not to be greedy!  This is your warning.

    The robot will always execute a measurement first, followed by an action.

    The robot will have a time limit of 5 seconds to find and extract all of the needed gems.
"""

import random
import math

import robot
import matrix

pi = math.pi


class SLAM:
    """Create a basic SLAM module.
    """

    def __init__(self):
        """Initialize SLAM components here.
        """
        self.bearing = 0
        self.landmarks = {}
        self.Omega = matrix.matrix()
        self.Xi = matrix.matrix()
        self.Omega.identity(2)
        self.Xi.zero(2, 1)
        self.r = robot.Robot(0, 0, 0, 1.0, pi / 2)

    def xy_distance(self, bearing, distance, movement=True):
        if movement:
            self.bearing += bearing
            dx = distance * math.cos(self.bearing)
            dy = distance * math.sin(self.bearing)
        else:
            adj_bearing = robot.truncate_angle(self.bearing + float(bearing))
            dx = distance * math.cos(adj_bearing)
            dy = distance * math.sin(adj_bearing)
        return [dx, dy]

    def calculate_noise(self, bearing, distance):

        #referenced to the robot class and piazza discussion
        factor_dist = 0.05
        factor_bearing = 0.02
        noise_factor = 100

        distance_sigma = factor_dist * distance
        bearing_sigma = factor_bearing * distance

        noise_x = math.sqrt(
            (distance_sigma ** 2) * (math.cos(bearing) ** 2) + (distance ** 2) * (bearing_sigma ** 2) * (
                    math.sin(bearing) ** 2))
        noise_y = math.sqrt(
            (distance_sigma ** 2) * (math.sin(bearing) ** 2) + (distance ** 2) * (bearing_sigma ** 2) * (
                    math.cos(bearing) ** 2))

        noise_x = abs(random.gauss(0, noise_x)) * noise_factor
        noise_y = abs(random.gauss(0, noise_y)) * noise_factor

        return [noise_x, noise_y]

    def process_measurements(self, measurements):
        """Process a new series of measurements.

        Args:
            measurements(dict): Collection of measurements
                in the format {'landmark id':{'distance':0.0, 'bearing':0.0, 'type':'B'}, ...}

        Returns:
            x, y: current belief in location of the robot
        """
        # referenced to the code in quiz, problem and piazza
        for landmark_id, mea in measurements.items():
            distance = mea['distance']
            bearing = mea['bearing']

            xy_distance = self.xy_distance(bearing, distance, False)

            measurement_noise = self.calculate_noise(bearing, distance)

            if landmark_id not in self.landmarks:
                rows = len(self.Omega.value)
                cols = len(self.Omega.value[0])
                self.Xi = self.Xi.expand(rows + 2, 1, [r for r in range(rows)], [0])
                self.Omega = self.Omega.expand(rows + 2, cols + 2, [r for r in range(rows)], [c for c in range(cols)])
                self.landmarks[landmark_id] = 2 * (len(self.landmarks) + 1)

            i = self.landmarks[landmark_id]
            for j in range(2):
                self.Omega.value[j][j] += 1.0 / measurement_noise[j]
                self.Omega.value[i + j][j] += -1.0 / measurement_noise[j]
                self.Omega.value[j][i + j] += -1.0 / measurement_noise[j]
                self.Omega.value[i + j][i + j] += 1.0 / measurement_noise[j]

                self.Xi.value[j][0] += -xy_distance[j] / measurement_noise[j]
                self.Xi.value[i + j][0] += xy_distance[j] / measurement_noise[j]

        mu = self.Omega.inverse() * self.Xi

        return mu

    def process_movement(self, steering, distance, motion_noise=0.01):
        """Process a new movement.

        Args:
            steering(float): amount to turn
            distance(float): distance to move
            motion_noise(float): movement noise

        Returns:
            x, y: current belief in location of the robot
        """
        # referenced to the code in quiz, problem and piazza

        xy_distance = self.xy_distance(steering, distance)

        rows = len(self.Omega.value)
        cols = len(self.Omega.value[0])
        matrix_index = [0, 1] + [r for r in range(4, rows + 2)]
        self.Omega = self.Omega.expand(rows + 2, cols + 2, matrix_index,
                                       matrix_index)
        self.Xi = self.Xi.expand(rows + 2, 1, matrix_index, [0])

        for i in range(2):
            self.Omega.value[i + 2][i] += -1.0 / motion_noise
            self.Omega.value[i][i + 2] += -1.0 / motion_noise
            self.Xi.value[i + 2][0] += xy_distance[i] / motion_noise
            self.Xi.value[i][0] += -xy_distance[i] / motion_noise

        for i in range(4):
            self.Omega.value[i][i] += 1.0 / motion_noise

        matrix_index = range(2, len(self.Omega.value))
        temp1_matrix = self.Omega.take([0, 1], matrix_index)
        temp2_matrix = self.Omega.take([0, 1])
        temp3_matrix = self.Xi.take([0, 1], [0])
        self.Xi = self.Xi.take(matrix_index, [0]) - temp1_matrix.transpose() * temp2_matrix.inverse() * temp3_matrix
        self.Omega = self.Omega.take(matrix_index) - temp1_matrix.transpose() * temp2_matrix.inverse() * temp1_matrix

        mu = self.Omega.inverse() * self.Xi
        x, y = mu.value[0][0], mu.value[1][0]
        return x, y


class GemExtractionPlanner:
    """
    Create a planner to navigate the robot to reach and extract all the needed gems from an unknown start position.
    """

    def __init__(self, max_distance, max_steering):
        """Initialize your planner here.

        Args:
            max_distance(float): the max distance the robot can travel in a single move.
            max_steering(float): the max steering angle the robot can turn in a single move.
        """
        # TODO
        #
        self.x = 0
        self.y = 0
        self.max_distance = max_distance
        self.max_steering = max_steering
        self.bearing = 0
        self.slam = SLAM()
        # self.r = robot.Robot(0, 0, 0, max_distance, max_steering)

    def next_move(self, needed_gems, measurements):
        """Next move based on the current set of measurements.

        Args:
            needed_gems(list): List of gems remaining which still need to be found and extracted.
            measurements(dict): Collection of measurements from gems in the area.
                                {'landmark id': {
                                                    'distance': 0.0,
                                                    'bearing' : 0.0,
                                                    'type'    :'B'
                                                },
                                ...}

        Return:
            Next command to execute on the robot.
                allowed:
                    'move 1.570963 1.0'  - Turn left 90 degrees and move 1.0 distance.
                    'extract D'          - [Part B] Attempt to extract a gem of type D from your current location.
                                           This will succeed if the specified gem is within the minimum sample distance.
                    'extract D 2.4 -1.6' - [Part C (also works for part B)] Attempt to extract a gem of type D
                                            from your current location.
                                           Specify the estimated location of gem D as (x=2.4, y=-1.6).
                                           This location is relative to your starting location (x=0, y=0).
                                           This will succeed if the specified gem is within the minimum sample distance.
        """
        mu = self.slam.process_measurements(measurements)
        self.x = mu.value[0][0]
        self.y = mu.value[1][0]

        for id, mea in measurements.items():
            distance = mea['distance']
            bearing = mea['bearing']
            gem_type = mea['type']

            for gem in needed_gems:
                if gem_type == gem:
                    if distance < 0.25:
                        steering = max(-self.max_steering, bearing)
                        steering = min(self.max_steering, steering)
                        distance = max(0, distance)
                        x_gem, y_gem = self.slam.process_movement(float(steering), float(distance))
                        action = 'extract ' + gem_type + ' ' + str(x_gem) + ' ' + str(y_gem)
                        return action
                    else:

                        steering = max(-self.max_steering, bearing)
                        steering = min(self.max_steering, steering)
                        distance = max(0, distance)
                        distance = min(self.max_distance, distance)
                        # bearing = robot.truncate_angle(self.bearing + steering)

                        action = 'move ' + str(steering) + ' ' + str(distance)

                        # bearing = self.bearing + steering
                        # self.x, self.y = self.slam.process_movement(float(bearing), float(distance))
                        # self.bearing += steering
                        # print('after move', (self.x, self.y, self.bearing))

                        return action
