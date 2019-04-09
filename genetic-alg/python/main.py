import sys
import time
from SchedulingProblem import SchedulingProblem
from SearchAlgorithm import SearchAlgorithm, SimulatedAnnealing

def main():
    nBuildings = 0
    nRooms = 0
    nCourses = 0
    TIME_LIMIT_SECONDS = 0
    algorithm = 0
    seed = 0

    try:
        nBuildings = int(sys.argv[1])
        nRooms = int(sys.argv[2])
        nCourses = int(sys.argv[3])
        TIME_LIMIT_SECONDS = int(sys.argv[4])
        algorithm = int(sys.argv[5])
        seed = int(sys.argv[6])
    except IndexError:
        print("ERROR: Incorrect number of arguments (should have six).")
        exit(1)
    except ValueError:
        print("Number format exception reading arguments")
        exit(1)

    print("Number of Buildings: " + str(nBuildings))
    print("Number of Rooms: " + str(nRooms))
    print("Number of Courses: " + str(nCourses))
    print("Time limit (s): " + str(TIME_LIMIT_SECONDS))
    print("Algorithm number: " + str(algorithm))
    print("Random seed: " + str(seed))

    test1 = SchedulingProblem()
    test1.SchedulingProblem(seed)
    test1.createRandomInstance(nBuildings, nRooms, nCourses)

    search = SearchAlgorithm()

    def current_milli_time():
        return int(round(time.time() * 1000))

    deadline = current_milli_time() + (1000 * TIME_LIMIT_SECONDS)

    # Add your seach algorithms here, each with a unique number
    solution = None
    if (algorithm == 0):
        solution = search.naiveBaseline(test1, deadline)
    elif (algorithm == 1):
        solution = search.greedy(test1, deadline)
    elif (algorithm == 2):
        # Create a SimulatedAnnealing algorithm for value
        pre_solution = SimulatedAnnealing(test1, deadline)
        pre_solution.set_heuristic("Value")  # Add heuristic
        pre_solution.set_limit(10000)  # Add value
        pre_solution = pre_solution.start_simulated_annealing()
        solution = search.naiveBaseline(pre_solution, deadline)
    elif (algorithm == 3):
        # Create a SimulatedAnnealing algorithm for distance
        dis_pre_solution = SimulatedAnnealing(test1, deadline)
        dis_pre_solution.set_heuristic("Distance")  # Add heuristic
        dis_pre_solution.set_limit(10000)  # Add value
        dis_pre_solution = dis_pre_solution.start_simulated_annealing()
        solution = search.naiveBaseline(dis_pre_solution, deadline)
    elif (algorithm == 4):
        # Create a SimulatedAnnealing algorithm for value and distance
        dis_pre_solution = SimulatedAnnealing(test1, deadline)
        dis_pre_solution.set_heuristic("Distance")  # Add heuristic
        dis_pre_solution.set_limit(10000)  # Add value
        dis_pre_solution = dis_pre_solution.start_simulated_annealing()

        pre_solution = SimulatedAnnealing(dis_pre_solution, deadline)
        pre_solution.set_heuristic("Value")  # Add heuristic
        pre_solution.set_limit(10000)  # Add value
        pre_solution = pre_solution.start_simulated_annealing()
        solution = search.naiveBaseline(pre_solution, deadline)

    else:
        print("ERROR: Given algorithm number does not exist!")
        exit(1)

    print("Deadline: " + str(deadline))
    print("Current: " + str(current_milli_time()))
    print("Time remaining: " + str(deadline - current_milli_time()))
    if (current_milli_time() > deadline):
        print("EXCEEDED DEADLINE")

    score = test1.evaluateSchedule(solution)
    print()
    print("Score: " + str(score))
    print()

main()
