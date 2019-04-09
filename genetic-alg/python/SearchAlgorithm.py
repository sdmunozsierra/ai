"""SearchAlgorithm class implementation."""
import math

class SearchAlgorithm:
    # Your search algorithm should return a solution in the form of a valid
    # schedule before the deadline given (deadline is given by system time in ms)
    @staticmethod
    def solve(problem, deadline):
        # get an empty solution to start from
        solution = problem.getEmptySchedule()
        # YOUR CODE HERE
        return solution

    # This is a very naive baseline scheduling strategy
    # It should be easily beaten by any reasonable strategy
    @staticmethod
    def naiveBaseline(problem, deadline):
        # get an empty solution to start from
        solution = problem.getEmptySchedule()

        for i in range(len(problem.courses)):
            c = problem.courses[i]
            scheduled = False

            for j in range(len(c.timeSlotValues)):
                if scheduled:
                    break
                if c.timeSlotValues[j] > 0:
                    for k in range(len(problem.rooms)):
                        if solution.schedule[k][j] < 0:
                            solution.schedule[k][j] = i
                            scheduled = True
                            break
        print("solution:\n")
        for row in solution.schedule:
            for val in row:
                print(val, end=' ')
            print()
        return solution

    @staticmethod
    def greedy(problem, deadline):
        solution = problem.getEmptySchedule()
        print("Courses {} values inorder:".format(len(problem.courses)))
        for course in problem.courses:
            print("{},".format(course.value), end='')

        def generate_idx(problem):
            size = len(problem.courses)
            i = problem.random.nextInt(size)  # Uses same random seed
            u = 1   # Noise
            if i+u > size:
                return i-1
            if i-u < 0:
                return i+1
            return i

        x = problem.courses[0]  # Start at the beggining
        history = []  # History to keep track of visited

        while len(history) is not len(problem.courses):
            if x in history:
                # print("x in history")
                pass
            else:
                history.append(x)
            i = generate_idx(problem)
            j = generate_idx(problem)
            try:
                right = problem.courses[i]
                left = problem.courses[j]
            except IndexError:
                continue
            if left.value > right.value:
                x = left
            else:
                x = right

        print("history ({}) elements:".format(len(history)))
        for course in history:
            print("{},".format(course.value), end='')

        # Find a schedule
        for i in range(len(history)):
            c = history[i]
            scheduled = False

            for j in range(len(c.timeSlotValues)):
                if scheduled:
                    break
                if c.timeSlotValues[j] > 0:
                    for k in range(len(problem.rooms)):
                        if (solution.schedule[k][j] < 0):
                            solution.schedule[k][j] = i
                            scheduled = True
                            break
        print("solution:\n")
        for row in solution.schedule:
            for val in row:
                print(val, end=' ')
            print()
        # print(solution.schedule)
        return solution


class SimulatedAnnealing():
    """Class to contain a Simulated Annealing algorithm."""

    def __init__(self, problem, deadline):
        """Create an Algorithm according to the heuristic."""
        self.problem = problem
        self.deadline = deadline
        self.heuristic = None
        self.limit = None
        self.prob_l = None  # Problem length

    def set_heuristic(self, heuristic):
        """Sets the heuristic."""
        self.heuristic = self._validate_heuristic(heuristic)  # update heuristic
        self.prob_l = self._get_problem_length()  # update problem length

    def set_limit(self, limit):
        """Sets the limit."""
        self.limit = limit

    def _validate_heuristic(self, heuristic):
        """Validates the heuristic input.
        :param heuristic: Either Value or Distance.
        :returns: valid heuristic (lowercase).
        """
        heuristic = heuristic.lower()
        if heuristic not in ['value', 'distance']:
            print("Heuristic not recognized, try either value or distance.")
            exit(1)
        return heuristic

    def _get_problem_length(self):
        if self.heuristic == "value":
            return len(self.problem.courses)
        if self.heuristic == "distance":
            return len(self.problem.rooms)
        print("Could not get problem length from unknown heuristic.")
        exit(1)

    def _get_neighbors(self, i):
        """Get a neighbor from index i.
        :param i: Index i.
        :returns: indices of neighbors.
        """
        # Debugging
        print("Getting neighbors of i:{}".format(i))
        # Make sure i is in bounds
        assert self.prob_l > 1 and i >= 0 and i < self.prob_l
        if i == 0:
            print("Neighbor: ", [1])
            return [1]
        if i == self.prob_l - 1:
            print("Neighbor: ", [self.prob_l - 2])
            return [self.prob_l - 2]
        print("Neighbor: ", [i - 1, i + 1])
        return [i - 1, i + 1]

    def _get_delta(self, x, random_index):
        """Get a delta value according to the heuristic.
        :param x: Current x index value.
        :param random_index: Random index to compare x to.
        :returns: delta value (difference between x and random[x]).
        """
        if not self.heuristic:
            print("Could not get delta value from unknown heuristic.")
            exit(1)
        if self.heuristic == "value":
            domain = self.problem.courses
            delta = domain[random_index].value - domain[x].value
            return delta
        print("Heuristic not recognized no delta was found.")
        exit(1)

    def _set_start_temperature(self):
        """Sets a starting temperature. This can be optimized."""
        if not self.heuristic:
            print("Could set temperature value from unknown heuristic.")
            exit(1)
        if self.heuristic == "value":
            temperature = self.prob_l * 10.7  # High enough
            return temperature
        print("Heuristic not recognized no temperature was set.")
        exit(1)


    def update_temperature(self, temperature, k=None):
        """Updates temperature using k.
        :param temperature: Temperature to be updated.
        :param k: value k to be substracted from temperature.
        """
        if not k:
            # No temperature set by user
            k = self.prob_l/1000
        # Return updated temperature
        print("Current k: ", k)
        return temperature - k

    def make_move(self, x, temperature):
        """Move towards the best state.
        :param x: Current state index.
        :param temperature: Current temperature.
        :returns: Most probable index to visit.
        """
        random_index = self.problem.random.nextInt(self.prob_l)
        delta = self._get_delta(x, random_index)

        # Delta is less than zero, return random index
        if delta < 0:
            return random_index

        # Get probability of using another index
        prob = math.exp(-delta / temperature)
        if self.problem.random.nextDouble() < prob:
            return random_index
        return x  # Return same state

    def _get_neighbor_local_maxima(self, i):
        """Get local maxima touple list.
        :param i: index to find the local maxima.
        """
        if not self.heuristic:
            print("Could not get local maxima from unknown heuristic.")
            exit(1)
        print("Getting local maxima indices:")
        if self.heuristic == "value":
            domain = self.problem.courses
            return all(
                domain[i].value > domain[ix].value for ix in self._get_neighbors(i))
        print("Heuristic not recognized local maxima not computed.")
        exit(1)

    def _get_local_maxima(self):
        """Get the local maxima from all neighbors.
        :returns: Local maxima list as tuple.
        """
        if not self.heuristic:
            print("Could not get local maxima list from unknown heuristic.")
            exit(1)
        print("Getting local maxima list indices:")
        if self.heuristic == "value":
            local_maxima = []
            for i in range(self.prob_l):
                if self._get_neighbor_local_maxima(i):
                    local_maxima.append([i, self.problem.courses[i]])
            return local_maxima
        print("Heuristic not recognized local maxima list not computed.")
        exit(1)


    def reorder_as_local_maxima(self, local_maxima):
        """Reorders the problem's courses indices towards local_maxima.
        moves maximum values to the front of the list.
        Moves minimum values to the end of the list and
        :param local_maxima: tuple list contaning indices for local maximum
            values found.
        :returns: SchedulingProblem with best indices first and worst last.
        """
        if not self.heuristic:
            print("Could not reorder maxima indices from unknown heuristic.")
            exit(1)
        print("Reordering local maxima indices:")
        if self.heuristic == "value":
            domain = self.problem.courses
            for idx, course in local_maxima:
                domain.pop(idx)
                domain.insert(0, course)
            return self.problem
        print("Heuristic not recognized local maxima indices not rearranged.")
        exit(1)

    def reorder_as_global_maxima(self, global_maximum):
        """Reorder the problem's courses indices towars global_maxima.
        :param global_maximum: index global maximum.
        :returns: SchedulingProblem with global maximum on the front.
        """
        if not self.heuristic:
            print("Could not reorder global maxima from unknown heuristic.")
            exit(1)
        print("Reordering local maxima indices:")
        if self.heuristic == "value":
            print("Global maximum index:", global_maximum)
            domain = self.problem.courses
            course_max = domain[global_maximum]
            domain.pop(global_maximum)
            domain.insert(0, course_max)
            return self.problem
        print("Heuristic not recognized gobal maxima not rearranged.")
        exit(1)

    def compare_results(self, x, global_maximum):
        """Compares current x value against the global maxima using a heuristic.
        :param x: Current state index.
        :param global_maximum: Current maximum index found.
        :returns: True if x is bigger than global_maximum.
        """
        if not self.heuristic:
            print("Could not compare results from unknown heuristic.")
            exit(1)
        print("Comparing results:")
        if self.heuristic == "value":
            domain = self.problem.courses
            if domain[x].value > domain[global_maximum].value:
                return True  # Update global maximum
            return False
        print("Heuristic not recognized values were compared.")
        exit(1)


    def _get_neighbor_distance_list(self):
        """Get the distance list from all neighbors.
        :returns: Best neighbor distance neighbor.
        """
        if not self.heuristic:
            print("Could not get distance list from unknown heuristic.")
            exit(1)
        print("Getting distance list indices:")
        if self.heuristic == "distance":
            distance_list = []
            max_dist = float('-inf')
            min_dist = float('+inf')
            for i in range(len(self.problem.courses)):
                distance = self._calculate_distance(i)
                if distance > max_dist:
                    max_dist = distance
                if distance < min_dist:
                    min_dist = distance
            # dist = all(
            #     distance < self._calculate_distance(ix) for ix in self._get_neighbors(i))
            print("max_dist:", max_dist)
            print("min_dist:", min_dist)
            # return dist
        print("Heuristic not recognized local maxima list not computed.")
        exit(1)

    def _calculate_distance(self, x):
        """Calculate the distance between the room and preferred location.
        :param x: Current state x index.
        :returns: distance.
        """
        if not self.heuristic:
            print("Could not get distance from unknown heuristic.")
            exit(1)
        print("Getting distance:")
        if self.heuristic == "distance":
            r = self.problem.rooms[x]
            c = self.problem.courses[x]
            b1 = r.b
            b2 = c.preferredLocation
            xDist = (b1.xCoord - b2.xCoord) * (b1.xCoord - b2.xCoord)
            yDist = (b1.yCoord - b2.yCoord) * (b1.yCoord - b2.yCoord)
            dist = math.sqrt(xDist + yDist)
            print("distance: ", dist)
            return dist
        print("Heuristic not recognized distance not computed.")
        exit(1)

    def start_simulated_annealing(self):
        """Simulated Annealing implementation.
        :param problem: SchedulingProblem.
        :param deadline: Remaining time to finish the algorithm.
        """
        # Initialize variables
        start_x = self.problem.random.nextInt(self.prob_l)  # Start randomly
        temperature = self._set_start_temperature()
        k = 1  # Each iteration cost is 1  # Change if needed
        x = start_x  # Current x state index
        global_maximum = x  # Global maximum found

        # Distance check
        self._get_neighbor_distance_list()



        # Reorder courses with local maxima
        local_maxima = self._get_local_maxima()
        self.problem = self.reorder_as_local_maxima(local_maxima)

        # Loop until temperature almost 0
        while temperature > 1e-3:
            x = self.make_move(x, temperature)
            if self.compare_results(x, global_maximum):
                global_maximum = x
            temperature = self.update_temperature(temperature, k)
            k += 1  # Update iteration

        print("Total iterations: ", k)
        # Reorder with global maxima
        self._print_stats(x, global_maximum, start_x)
        self.problem = self.reorder_as_global_maxima(global_maximum)
        return self.problem

    def _print_stats(self, x, global_maximum, start_x):
        if not x or not global_maximum or not start_x:
            print("Could not get stats from unfinished algorithms.")
            exit(1)
        if self.heuristic == "value":
            domain = self.problem.courses
            print("Start solution index: {} = {:3f}".format(
                start_x, domain[start_x].value))
            print("Current solution index: {} = {:1.3f}".format(
                x, domain[x].value))
            print("Best solution (global_maxima) index: {} = {:0.3f}".format(
                global_maximum, domain[global_maximum].value))
        else:
            print("Heuristic not recognized stats were not computed.")
            exit(1)
