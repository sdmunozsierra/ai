"""Read a map file.txt and perform Path Finding."""
from collections import deque
import sys
import time


class ReadMap:
    """Read a map class."""

    def __init__(self, filename):
        """Initialize function.
            :param filename: Filename to be utilized"""
        self.filename = filename
        self.dimensions = None
        self.starting_loc = None
        self.goal_loc = None
        self.map = []  # Map as an array

    def read_filemap(self):
        """Read a map file."""
        # Check that the extension is .txt
        if not self.filename.lower().endswith(('.txt')):
            print("File not recognized as a map.")

        # Open file
        with open(self.filename, 'r', encoding='utf-8') as mapfile:
            for e, line in enumerate(mapfile):
                # First line has the dimensions of the map
                if e == 0:
                    self.dimensions = line
                # Second line has the coordinates of the starting location
                elif e == 1:
                    self.starting_loc = line
                # Third line has the coordinates of the goal location
                elif e == 2:
                    self.goal_loc = line
                # Append lines to map
                else:
                    line = line.rstrip('\n')
                    arr = []
                    for e in line:
                        if e != " ":
                            arr.append(int(e))
                    self.map.append(arr)
        # Clean inputs
        self.clean_inputs()
        print("Loaded file {}".format(self.filename))

    def clean_inputs(self):
        """Converts strings into integers."""
        # Clean dimensions
        dimensions = self.dimensions.split(" ")
        self.dimensions = (int(dimensions[0]),
                           int(dimensions[1].rsplit('\n')[0]))
        # Clean starting location
        start = self.starting_loc.split(" ")
        self.starting_loc = (int(start[0]),
                             int(start[1].rsplit('\n')[0]))
        # Clean goal location
        goal = self.goal_loc.split(" ")
        self.goal_loc = (int(goal[0]),
                         int(goal[1].rsplit('\n')[0]))

    def print_map_info(self):
        """Prints out the information extracted from the map file."""
        d = "Dimensions: {}".format(self.dimensions)
        lo = "Starting Location: {}\nGoal Location: {}".format(
            self.starting_loc, self.goal_loc)
        m = "Map: {}".format(self.map)
        info = "Parsed the following map:\n{}\n{}\n{}\n".format(d, lo, m)
        print('-'*60)
        print(info)
        print('-'*60)


class SearchAlgorithms():
    """Create a search algorithms class."""

    def __init__(self, map):
        """Initialize function.
            :param map: ReadMap object"""
        self.map = map
        self.grid = map.map
        self.visited = []  # Visited nodes
        self.queue = None  # Nodes to visit for BFS
        self.stack = None  # Stack t
        self.cost = 0
        self.max_nodes = 0
        self.finished = False
        self.time = time.time()  # Start time

    def get_path_cost(self, x, y):
        """Return the path cost of moving to x, y.
            :param x: Row axis
            :param y: Column axis"""
        try:
            cost = self.grid[x][y]
            print("Cost of path({},{}) is: {}".format(x, y, cost))
            return cost
        except IndexError:
            print("Out of bounds.")
            return None

    def expand_neighboors(self, x, y):
        """Return valid neighbors to visit (if they haven't been visited).
            :param x: Row axis
            :param y: Column axis"""
        possible_neighboors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        print("Generating all neighboors of({},{}): {}".format(
            x, y, possible_neighboors))
        valid_neighboors = []
        for neighboor in possible_neighboors:
            # Check positive neighboors
            if neighboor[0] < 0 or neighboor[1] < 0:
                continue
            # Skip neighboor if already visited
            if neighboor in self.visited:
                continue
            # Check if the path has a cost
            if self.get_path_cost(neighboor[0], neighboor[1]):
                valid_neighboors.append(neighboor)
        # Return valid neighboors
        if valid_neighboors:
            print("Found these valid neighboors:", valid_neighboors)
            return valid_neighboors
        return None

    def is_goal(self, x, y):
        """Check if the current path is the goal."""
        try:
            goal = (x, y) == self.map.goal_loc
            print("Checking for goal {}: current {} vs expected {}".format(
                goal, (x, y), self.map.goal_loc))
            return goal
        except IndexError:
            return False

    def bfs(self):
        """Run BFS. First checks all neighboors"""
        print("Starting BFS search")
        self.queue = deque([self.map.starting_loc])
        max_nodes = len(self.queue)
        print("queue:", self.queue)
        while self.queue:

            # Check for current nodes in memory
            if max_nodes < len(self.queue):
                max_nodes = len(self.queue)
            x, y = self.queue.popleft()
            self.cost = self.cost + self.get_path_cost(x, y)  # Update cost
            self.visited.append((x, y))  # Mark as visited
            print("Visited locations:", self.visited)

            # Check for a goal
            if self.is_goal(x, y):
                # self.cost = self.cost + self.get_path_cost(x, y)
                print("Finished with cost:", self.cost)
                self.finished = True
                self.max_nodes = max
                return self.visited

            # Expand Neighboors
            neighboors = self.expand_neighboors(x, y)
            if neighboors:
                for n in neighboors:
                    self.queue.append(n)
        # Did not found a solution
        print("There is not solution")
        return None

    def dfs(self):
        """Run DFS. First checks all neighboors"""
        print("Starting bfs")
        self.queue = deque([self.map.starting_loc])
        max_nodes = len(self.queue)
        print("queue:", self.queue)
        while self.queue:

            # Check for current nodes in memory
            if max_nodes < len(self.queue):
                max_nodes = len(self.queue)
            x, y = self.queue.popleft()
            self.visited.append((x, y))
            self.cost = self.cost + self.get_path_cost(x, y)
            print("visited:", self.visited)

            # Check for a goal
            if self.is_goal(x, y):
                print("Finished with cost:", self.cost)
                self.finished = True
                self.max_nodes = max
                return self.visited

            # Expand Neighboors
            neighboors = self.expand_neighboors(x, y)
            if neighboors:
                # Append only first neighboor
                self.queue.append(neighboors[0])
                self.cost = self.cost + self.get_path_cost(x, y)

        # Did not found a solution
        print("There is not solution")
        return None

    def a_star(self):
        """Run A* Search. Uses a heuristic function."""
        print("Running A* Search\n")
        self.queue = deque([self.map.starting_loc])
        max_nodes = len(self.queue)
        print("queue:", self.queue)
        while self.queue:

            # Check for current nodes in memory
            if max_nodes < len(self.queue):
                max_nodes = len(self.queue)
            x, y = self.queue.popleft()
            self.visited.append((x, y))
            self.cost = self.cost + self.get_path_cost(x, y)
            print("visited:", self.visited)

            # Check for a goal
            if self.is_goal(x, y):
                # self.cost = self.cost + self.get_path_cost(x, y)
                print("Finished with cost:", self.cost)
                self.finished = True
                self.max_nodes = max
                return self.visited
            neighboors = self.expand_neighboors(x, y)
            if neighboors:
                self.queue.append(self.heuristic_function(neighboors))
        # Did not found a solution
        print("There is not solution")
        return None

    def algorithm_logic(self, search_alg):
        """Chooses a logic for a specified algorithm.
            :param search_alg: 'bfs', 'dfs', or 'a_star'"""
        print("Running {}\n".format(search_alg))
        self.queue = deque([self.map.starting_loc])
        max_nodes = len(self.queue)
        print("queue:", self.queue)
        while self.queue:

            # Check for current nodes in memory
            if max_nodes < len(self.queue):
                max_nodes = len(self.queue)
            x, y = self.queue.popleft()
            self.visited.append((x, y))
            self.cost = self.cost + self.get_path_cost(x, y)
            print("visited:", self.visited)

            # Check for a goal
            if self.is_goal(x, y):
                # self.cost = self.cost + self.get_path_cost(x, y)
                print("Finished with cost:", self.cost)
                self.finished = True
                self.max_nodes = max
                self.time = time.time() - self.time
                return self.visited

            # Expand neighboors according to search_alg
            if search_alg == 'bfs':
                # Expand Neighboors from root and add all
                neighboors = self.expand_neighboors(x, y)
                if neighboors:
                    for n in neighboors:
                        self.queue.append(n)
            if search_alg == 'dfs':
                # Expand neighboors from root and add only the first one
                neighboors = self.expand_neighboors(x, y)
                if neighboors:
                    # Append only first neighboor
                    self.queue.append(neighboors[0])
                    self.cost = self.cost + self.get_path_cost(x, y)

            if search_alg == 'astar':
                # Expand neighboors but use heuristic function
                neighboors = self.expand_neighboors(x, y)
                if neighboors:
                    self.queue.append(self.heuristic_function(neighboors))

        # Did not found a solution
        print("There is not solution")
        self.time = time.time() - self.time
        return None

    def heuristic_function(self, neighboors):
        """Finds the heuristic (lowest cost) neighboor.
            :neighboors: List of neighboors
            :return: Lowest cost neighboor
        """
        print("Heuristic information for {} neighboors".format(neighboors))
        lowest_cost = None
        lowest_cost_neighboor = None
        if isinstance(neighboors, tuple):
            print("Returning only one neighboor {}".format(neighboors))
            return neighboors
        for n in neighboors:
            current_cost = self.get_path_cost(n[0], n[1])
            print("Comparing cost:{} node:{} with cost:{} node:{}".format(
                lowest_cost, lowest_cost_neighboor, current_cost, n))
            try:
                # Saves the current cost as the lowest cost
                if lowest_cost > current_cost:
                    lowest_cost = current_cost
                    lowest_cost_neighboor = n
                continue
            except TypeError:
                lowest_cost = current_cost
                lowest_cost_neighboor = n
        # Returns lowest cost neighboor
        print("Heuristic determined cost{}: node{}:".format(
            lowest_cost, lowest_cost_neighboor))
        return lowest_cost_neighboor

    def print_results(self):
        if self.finished:
            path_cost = "Path cost found is:", self.cost
            number = "The number of nodes expanded:", len(self.visited)
            maximum = "Maximum number of nodes in memory:", self.max_nodes
            runtime = "Runtime of the algorithm in ms:", 0
            path = "The path sequence as (row, col):", self.visited
            print(path_cost, number, maximum, runtime, path)
        else:
            print("The algorith did no finished in 3 mins.")


if __name__ == "__main__":
    # Read user arguments from command line
    filename = sys.argv[1]
    search_algorithm = sys.argv[2]
    search_algorithm = search_algorithm.lower()
    print(sys.argv)
    if search_algorithm not in ('dfs', 'bfs', 'astar'):
        print("Invalid command!\nPlease use either dfs, bfs or astar")
        exit()

    # Use defaults if not filename
    if not filename:
        filename = "map1.txt"
    if not search_algorithm:
        search_algorithm = "dfs"
    print("Performing {} in filename: {}".format(filename, search_algorithm))

    # Create a map from file
    file_map = ReadMap(filename)
    file_map.read_filemap()
    file_map.print_map_info()

    # Create a SearchAlgorithms class
    search = SearchAlgorithms(file_map)
    search.algorithm_logic(search_algorithm)
    search.print_results()
