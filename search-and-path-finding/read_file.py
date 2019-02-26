# Read a map file.txt
from collections import deque


class ReadMap:
    """Read a map class."""

    def __init__(self, filename):
        """Initialize."""
        self.filename = filename
        self.dimensions = None
        self.starting_loc = None
        self.goal_loc = None
        self.map = []

    def read_filemap(self):
        """Read a map file."""
        # Check that the extension is .txt
        if not self.filename.lower().endswith(('.txt')):
            print("File not recognized")

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
        """Prints the information extracted from the map file."""
        d = "Dimensions: {}".format(self.dimensions)
        lo = "Starting Location: {}\nGoal Location: {}".format(
            self.starting_loc, self.goal_loc)
        m = "Map: {}".format(self.map)
        print(d, lo, m)


class Node():
    """Create a node class."""

    def __init__(self, map):
        """Creates a node map from a map_list from a file."""
        self.map = map
        self.grid = map.map
        self.visited = []  # Visited nodes
        self.queue = None  # Nodes to visit
        self.cost = 0
        self.max_nodes = 0
        self.finished = False

    def get_path_cost(self, x, y):
        """Return the path cost of moving to x, y"""
        try:
            cost = self.grid[x][y]
            print("Cost of this path is:", cost)
            return cost
        except IndexError:
            print("Out of bounds.")
            return None

    def expand_neighboors(self, x, y):
        """Return valid neighbors to visit (if they haven't been visited)."""
        print("generating neighboors of:", x, y)
        possible_neighboors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        print("possible neighboors:", possible_neighboors)
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
            print("Valid neighboors:", valid_neighboors)
            return valid_neighboors
        return None

    def is_goal(self, x, y):
        """Check if the current path is the goal."""
        try:
            goal = (x, y) == self.map.goal_loc
            print("Is goal: {} current {} vs {}".format(
                goal, (x, y), self.map.goal_loc))
            return goal
        except IndexError:
            print("It is not goal", x, y)
            return False

    def bfs(self):
        """Run BFS."""
        print("Starting bfs")
        self.queue = deque([self.map.starting_loc])
        max = len(self.queue)
        print("queue:", self.queue)
        while self.queue:
            # Check for current nodes in memory
            if max < len(self.queue):
                max = len(self.queue)
            x, y = self.queue.popleft()
            self.visited.append((x, y))
            print("visited:", self.visited)
            # Check for a goal
            if self.is_goal(x, y):
                self.cost = self.cost + self.get_path_cost(x, y)
                print("Finished with cost:", self.cost)
                self.finished = True
                self.max_nodes = max
                return self.visited
            neighboors = self.expand_neighboors(x, y)
            if neighboors:
                for n in neighboors:
                    self.queue.append(n)
                    self.cost = self.cost + self.get_path_cost(x, y)
        print("There is no solution")
        return None

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

# MAIN
# Read a map
map = ReadMap("map1.txt")
map.read_filemap()
map.print_map_info()

# Create a node class
node = Node(map)
# node.bfs(map.map, map.starting_loc)
# node.get_path_cost(5, 0)
node.expand_neighboors(1, 1)
node.is_goal(4, 3)
node.bfs()
node.print_results()
