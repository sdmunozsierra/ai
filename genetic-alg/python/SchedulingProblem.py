"""SchedulingProblem implementation."""

import math
import javarandom as random
from Building import Building
from Room import Room
from Course import Course
from Schedule import Schedule

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

        print("Courses timeslotvalues and real value:")
        for idx, course in enumerate(self.courses):
            print("idx {}: {} -> {}".format(
                idx, course.timeSlotValues, course.value))

    def getEmptySchedule(self):
        tmp = Schedule()
        # print(self)
        # print("Schedule size: {}, {}".format(len(self.rooms), self.NUM_TIME_SLOTS))
        tmp.Schedule(len(self.rooms), self.NUM_TIME_SLOTS)

        # print("LEN ROOMS::")
        # print(len(self.rooms))
        # print(len(tmp.schedule))
        for i in range(len(self.rooms)):
            for j in range(self.NUM_TIME_SLOTS):
                # print("i {} j {}".format(i, j))
                tmp.schedule[i][j] = -1
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
                # print("S: s[i][j]: {}". format(s[i][j]))
                if (s[i][j] < 0 or s[i][j] > len(self.courses)):
                    continue

                # class that hase been scheduled more than once
                # print(assigned)
                # print(assigned[s[i][j]])
                if assigned[s[i][j]] > 0:
                    print("ERROR: Invalid schedule")
                    return float('-inf')

                assigned[s[i][j]] = assigned[s[i][j]] + 1
                # for val in assigned:
                #     print(val, end='')
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
                if c.timeSlotValues[j] <= 0:
                    continue

                # course was assigned to a room that is too small
                if c.enrolledStudents > r.capacity:
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
