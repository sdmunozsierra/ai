import sys
import math
import time
import javarandom2 as random

class Building:
    def __init__(self):
        self.xCoord = None
        self.yCoord = None


class Room:
    def __init__(self):
        self.b = None
        self.capacity = None

class Course:
    def __init__(self):
        self.value = None
        self.preferredLocation = None
        self.timeSlotValues = None
        self.enrolledStudents = None

class Schedule:
    def __init__(self):
        self.schedule = None

    def Schedule(self, nRooms, nTimeSlots):
        self.schedule = [[0 for x in range(nRooms)] for y in range(nTimeSlots)]

class SchedulingProblem:

    def __init__(self):
        self.NUM_TIME_SLOTS = 10
        self.MAX_X_COORD = 10
        self.MAX_Y_COORD = 10
        self.DISTANCE_PENALTY = float(2.5)

        self.buildings = []
        self.rooms = []
        self.courses = []

        self.random = random.Random()

    def SchedulingProblem(self, seed):
        if (seed > 0):
            self.random.setSeed(seed)
        else:
            self.random = random.Random()

        self.buildings = []
        self.rooms = []
        self.courses = []

    def createRandomInstance(self, nBuildings, nRooms, nCourses):
        # create random buildings
        for building in range(nBuildings):
            tmp = Building()
            tmp.xCoord = self.random.nextDouble() * self.MAX_X_COORD
            tmp.yCoord = self.random.nextDouble() * self.MAX_Y_COORD
            print("x: {} y: {}".format(tmp.xCoord, tmp.yCoord))
            self.buildings.append(tmp)

        # create random rooms
        for room in range(nRooms):
            tmp = Room()
            bld = int(self.random.nextDouble() * nBuildings)
            print("bld: {}".format(bld))
            tmp.b = self.buildings[int(self.random.nextDouble() * nBuildings)]
            tmp.capacity = (int(self.random.nextDouble() * 70)) + 30
            self.rooms.append(tmp)

        # create random courses
        print(nCourses)
        for course in range(nCourses):
            tmp = Course()
            tmp.enrolledStudents = (int(self.random.nextDouble() * 70)) + 30
            tmp.preferredLocation = self.buildings[int(self.random.nextDouble() * nBuildings)]
            tmp.value = self.random.nextDouble() * 100
            tmp.timeSlotValues = [0] * self.NUM_TIME_SLOTS

            # debug
            # print("Num time slots: {}".format(self.NUM_TIME_SLOTS))
            # print(tmp.timeSlotValues)

            for j in range(self.NUM_TIME_SLOTS):
                if (self.random.nextDouble() < float(0.3)):
                    tmp.timeSlotValues[j] = 0
                else:
                    tmp.timeSlotValues[j] = int(self.random.nextDouble() * 10)
            self.courses.append(tmp)

        for course in self.courses:
            print(course.timeSlotValues)

    def getEmptySchedule(self):
        tmp = Schedule()
        print("Schedule size: {}, {}".format(len(self.rooms), self.NUM_TIME_SLOTS))
        tmp.Schedule(len(self.rooms), self.NUM_TIME_SLOTS)

        for idx in range(len(self.rooms)):
            for timeSlot in range(self.NUM_TIME_SLOTS):
                tmp.schedule[idx][timeSlot] = -1
        return tmp

    def evaluateSchedule(self, solutionSchedule):
        """ solutionSchedule is Schedule type."""
        s = solutionSchedule.schedule

        if (len(s) is not len(self.rooms)) or len(s[0]) is not self.NUM_TIME_SLOTS:
            print("ERROR: invalid schedule dimensions")
            return float('-inf')

        # check that all classes are assigned only once
        assigned = [0]*len(self.courses)
        for i in range(len(s)):
            for j in range(len(s[0])):

                # indicates an unassigned time slot
                print("S: s[i][j]: {}". format(s[i][j]))
                if (s[i][j] < 0 or s[i][j] > len(self.courses)):
                    continue

                # class that hase been scheduled more than once
                # print(assigned)
                # print(assigned[s[i][j]])
                if (assigned[s[i][j]] > 0):
                    print("ERROR: Invalid schedule")
                    return float('-inf')

                assigned[s[i][j]] = assigned[s[i][j]] + 1
                for val in assigned:
                    print(val, end='')
                # assigned[s[i][j]]+1

        value = float(0)

        for i in range(len(s)):
            for j in range(len(s[0])):

                # indicates an unassigned time slot
                if (s[i][j] < 0 or s[i][j] > len(self.courses)):
                    continue

                c = self.courses[s[i][j]]
                r = self.rooms[i]

                # course was not assigned to a feasible time slot
                if (c.timeSlotValues[j] <= 0):
                    continue

                # course was assigned to a room that is too small
                if (c.enrolledStudents > r.capacity):
                    continue

                # add in the value for the class
                value += c.value
                value += c.timeSlotValues[j]

                # calculate the distance penalty
                b1 = r.b
                b2 = c.preferredLocation
                xDist = (b1.xCoord - b2.xCoord) * (b1.xCoord - b2.xCoord)
                yDist = (b1.yCoord - b2.yCoord) * (b1.yCoord - b2.yCoord)
                dist = math.sqrt(xDist + yDist)

                value -= self.DISTANCE_PENALTY * dist

        return value

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
                if (scheduled):
                    break
                if (c.timeSlotValues[j] > 0):
                    for k in range(len(problem.rooms)):
                        if (solution.schedule[k][j] < 0):
                            solution.schedule[k][j] = i
                            scheduled = True
                            break
        print("solution:\n")
        print(solution.schedule)
        return solution

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
