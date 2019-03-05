"""Read a map file.txt and perform Path Finding."""
from collections import deque
from bisect import insort
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
        self.parent = {}  # Parent nodes
        self.visited = []  # Visited (opened) nodes
        self.path = []  # Solution path (if any)
        self.queue = None  # Queue for BFS
        self.stack = None  # Stack for DFS
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
        possible_neighboors = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
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
        """Check if the current path is the goal.
            :param x: Row axis
            :param y: Column axis"""
        try:
            goal = (x, y) == self.map.goal_loc
            print("Checking for goal {}: current {} vs expected {}".format(
                goal, (x, y), self.map.goal_loc))
            return goal
        except IndexError:
            return False

    def print_path(self, parent):
        """Prints the path solution by keeping track of the parent. Used by BFS
            :param parent: Parent dictionary containing the solution"""
        goal = self.map.goal_loc
        self.path = [goal]
        # trace the path back till we reach start
        while goal != self.map.starting_loc:
            self.cost = self.cost + self.get_path_cost(goal[0], goal[1])
            goal = parent[goal]
            self.path.insert(0, goal)
        return self.path

    def calculate_path_cost(self, path):
        """Calculates the path cost. Used by DFS.
            :param path: Valid path to solution"""
        for vertex in path:
            self.cost = self.cost + self.get_path_cost(vertex[0], vertex[1])
        return self.cost

    def bfs(self):
        """BFS with parent tracking."""
        start = self.map.starting_loc

        # Start Queue
        self.queue = deque([start])
        self.parent[start] = start
        opened = len(self.queue)

        # Iterate every node until solution
        while self.queue:
            # Update opened nodes
            opened = len(self.queue) if opened < len(self.queue) else opened
            curr_node = self.queue.popleft()  # Open left node
            # Expand neighbors
            neighbors = self.expand_neighboors(curr_node[0], curr_node[1])
            for neighbor in neighbors:
                # goal found
                if self.is_goal(neighbor[0], neighbor[1]):
                    # Mark as finished, update time and nodes
                    self.finished = True
                    self.time = time.time() - self.time
                    self.max_nodes = opened
                    self.parent[neighbor] = curr_node
                    self.print_path(self.parent)
                    return True
                # check if neighbor already seen
                if neighbor not in self.parent:
                    self.parent[neighbor] = curr_node
                    self.queue.append(neighbor)
        # No solution found
        print("No path found.")
        return False

    def dfs(self):
        """Implement dfs."""
        start = self.map.starting_loc
        self.stack = [(start, [start])]
        self.visited = set()
        opened = len(self.stack)

        while self.stack:
            opened = len(self.stack) if opened < len(self.stack) else opened
            (vertex, path) = self.stack.pop()
            if vertex not in self.visited:
                if self.is_goal(vertex[0], vertex[1]):
                    # Mark as finished, update time and nodes
                    self.finished = True
                    self.time = time.time() - self.time
                    self.max_nodes = opened - 1
                    self.path = path
                    self.parent = self.visited  # To measure expanded nodes
                    self.calculate_path_cost(path)
                    return True
                self.visited.add(vertex)
                neighboors = self.expand_neighboors(vertex[0], vertex[1])
                if neighboors:
                    for neighbor in neighboors:
                        self.stack.append((neighbor, path + [neighbor]))
        # No solution found
        print("No path found.")
        return False

    def astar(self):
        """A* BFS with heuristic function."""
        start = self.map.starting_loc

        # Start Queue
        self.queue = deque([start])
        self.parent[start] = start
        opened = len(self.queue)

        # Iterate every node until solution
        while self.queue:
            # Update opened nodes
            opened = len(self.queue) if opened < len(self.queue) else opened
            curr_node = self.queue.popleft()  # Open left node
            # Expand neighbors
            neighbors = self.expand_neighboors(curr_node[0], curr_node[1])
            neighbors = (self.heuristic_function_as_list(neighbors))
            print(neighbors)
            for neighbor in neighbors:
                # goal found
                if self.is_goal(neighbor[0], neighbor[1]):
                    # Mark as finished, update time and nodes
                    self.finished = True
                    self.parent[neighbor] = curr_node
                    self.print_path(self.parent)
                    return True
                # check if neighbor already seen
                if neighbor not in self.parent:
                    self.parent[neighbor] = curr_node
                    self.queue.append(neighbor)
        # No solution found
        print("No path found.")
        self.time = time.time() - self.time
        return False

    def algorithm_logic(self, search_alg):
        """Chooses a logic for a specified algorithm.
            :param search_alg: 'bfs', 'dfs', or 'a_star'"""
        print("Running {}\n".format(search_alg))
        if search_alg == 'bfs':
            self.bfs()
            return
        if search_alg == 'dfs':
            self.dfs()
            return
        if search_alg == 'astar':
            self.astar()
            return

    def heuristic_function(self, neighbors):
        """Returns a list of neighbors from lowest to highest.
            :param neighbors: List of neighbors
            :return: Lowest cost neighbor list
        """
        print("Heuristic information for {} neighbors".format(neighbors))
        lowest_cost = None
        lowest_cost_neighbor = None
        if isinstance(neighbors, tuple):
            print("Returning only one neighboor {}".format(neighbors))
            return neighbors
        for n in neighbors:
            current_cost = self.get_path_cost(n[0], n[1])
            print("Comparing cost:{} node:{} with cost:{} node:{}".format(
                lowest_cost, lowest_cost_neighbor, current_cost, n))
            try:
                if lowest_cost > current_cost:
                    lowest_cost = current_cost
                    lowest_cost_neighbor = n
                continue
            except TypeError:
                lowest_cost = current_cost
                lowest_cost_neighbor = n
        # Returns lowest cost neighbor
        print("Heuristic determined cost{}: node{}:".format(
            lowest_cost, lowest_cost_neighbor))
        return lowest_cost_neighbor

    def heuristic_function_as_list(self, neighbors):
        """Returns a list of neighbors ranked from lowest to highest.
            :param neighbors: Possible neighbors to be ranked."""
        print("Heuristic function list for {} neighbors".format(neighbors))
        ordered_list_by_cost = []
        ordered_list_by_node = []
        if isinstance(neighbors, tuple):
            print("Returning only one neighboor {}".format(neighbors))
            return neighbors
        for n in neighbors:
            current_cost = self.get_path_cost(n[0], n[1])
            try:
                # Saves the current cost as the lowest cost
                insort(ordered_list_by_cost, current_cost)
                idx = ordered_list_by_cost.index(current_cost)
                ordered_list_by_node.insert(idx, n)
            except TypeError:
                print("Error, break")
        print("list of costs:", ordered_list_by_cost)
        print("list of nodes:", ordered_list_by_node)
        return ordered_list_by_node

    def print_results(self):
        """Prints the result of the algorithm."""
        if self.finished:
            path_cost = "Path cost found is: {}".format(self.cost)
            number = "The number of nodes expanded: {}".format(
                len(self.parent))
            maximum = "Maximum number of nodes in memory: {}".format(
                self.max_nodes)
            runtime = "Runtime of the algorithm in seconds: {}".format(
                self.time)
            path = "The path sequence as (row, col): {}".format(self.path)
            result = "{}\n{}\n{}\n{}\n{}".format(
                path_cost, number, maximum, runtime, path)
            header = "-"*30 + "RESULTS" + "-"*30
            print(header)
            print(result)
            print('-'*68)
        else:
            print("The algorith did no finished.")


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
