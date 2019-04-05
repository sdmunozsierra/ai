import sys
import time
import math
from Building import Building, Course, Room, Schedule, SchedulingProblem


class SearchAlgorithm:

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
        # print("solution:\n")
        # for row in solution.schedule:
        #     for val in row:
        #         print(val, end=' ')
        #     print()
        return solution


    @staticmethod
    def sa(A, problem, deadline):
        def update_temperature(T, k):
            return T - 0.1

        def make_move(x, A, T):
            rand = problem.random.nextInt(len(A))
            print("rand", rand)
            print(A[rand].value)
            print(A[x].value)
            delta = A[rand].value - A[x].value

            if delta < 0:
                return rand
            else:
                prob = math.exp(-delta / T)
                if problem.random.nextDouble() < prob:
                    return rand
                else:
                    return x


        # P = problem
        # A = problem.courses
        # A = problem
        print(A)
        L = len(A)
        x0 = problem.random.nextInt(L)
        T = 1000.
        K = 1

        x = x0
        x_best = x0
        # history = [(x_best, A[x_best])]  # Indices of best cases

        while T > 1e-3:
            x = make_move(x, A, T)
            # print("x location:", x)
            if(A[x].value > A[x_best].value):
                print("x_best: ", x_best)
                print("x: ", x)
                x_best = x
                # history.append((x_best, A[x_best]))
            T = update_temperature(T, K)
            K += 1

        print("iterations:", K)
        # print("history: ", history)
        # return x, x_best, x0, history
        return x, x_best, x0

def main():
    nBuildings = 100
    nRooms = 100
    nCourses = 100
    TIME_LIMIT_SECONDS = 60
    algorithm = 0
    seed = 2

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
        # CODE TO TEST SA HERE
        LIMIT = 1000
        def get_neighbors(i, L):
            print("i:", i)
            print("L:", L)
            assert L > 1 and i >= 0 and i < L
            if i == 0:
                return [1]
            elif i == L - 1:
                return [L - 2]
            else:
                return [i - 1, i + 1]

        def isminima_local(p, A):
            print("p:", p)
            return all(A[p].value < A[i].value for i in get_neighbors(p, len(A)))

        def ismaxima_local(p, A):
            print("p:", p)
            return all(A[p].value > A[i].value for i in get_neighbors(p, len(A)))

        def func(x):
            return math.sin((2*math.pi / LIMIT) * x) + 0.001 * test1.random.nextDouble()

        def initialize(L):
            return map(func, range(L))

        def reorder_as_courses_local_maxima(problem, local_maxima):
            """Reorders the problem's courses indices towards local_maxima.
            moves maximum values to the front of the list.
            Moves minimum values to the end of the list and
            :problem: SchedulingProblem to be reordered.
            :param local_maxima: tuple list contaning indices for local maximum values found.
            :returns: SchedulingProblem with best indices first and worst last.
            """
            # Debugging
            print("Local maxima:")
            for idx, course in local_maxima:
                print("idx: {}, value: {}".format(idx, course.value))
            print("Moving maxima")
            old_values = [course.value for course in problem.courses]
            for idx, course in local_maxima:
                problem.courses.pop(idx)
                problem.courses.insert(0, course)
            new_values = [course.value for course in problem.courses]
            print(old_values)
            print(new_values)
            return problem  # Returns problem with local maxima on the front

        def reorder_as_courses_global_maxima(problem, global_maxima):
            """Reorder the problem's courses indices towars global_maxima.
            :problem: SchedulingProblem to be reordered.
            :param global_maxima: tuple contaning index and course for global maxima.
            :returns: SchedulingProblem with global maxima on the front.
            """
            idx, course = global_maxima
            problem.courses.pop(idx)
            problem.courses.insert(0, course)
            return problem

        def reorder_problem_courses(problem, local_minima, local_maxima, history_maxima):
            """Reorders the problem's courses indices.
            Moves minimum values to the end of the list and
            moves maximum values to the front of the list.
            :problem: SchedulingProblem to be reordered.
            :param local_minima: list containing indices for local maximum values found.
            :param history_maxima: list contaning indices for global maximum values found.
            :returns: SchedulingProblem with best indices first and worst last.
            """
            # Debugging
            print("Local mininima:")
            for idx, course in local_minima:
                print("idx: {}, value: {}".format(idx, course.value))
            print("Local maxima:")
            for idx, course in local_maxima:
                print("idx: {}, value: {}".format(idx, course.value))
            print("Global maxima:")
            for idx, course in history_maxima:
                print("idx: {}, value: {}".format(idx, course.value))

            # Move indices from local maxima to the front of the list
            print("Moving maxima")
            old_values = [course.value for course in problem.courses]
            for idx, course in local_maxima:
                problem.courses.pop(idx)
                problem.courses.insert(0, course)
            new_values = [course.value for course in problem.courses]
            print(old_values)
            print(new_values)

            # Move indices from local minima to the front of the list
            print("Moving minima")
            print(len(local_minima))
            old_values = [course.value for course in problem.courses]
            for idx, course in local_minima:
                problem.courses.pop(idx-1)
                problem.courses.append(course)
            new_values = [course.value for course in problem.courses]
            print(old_values)
            print(new_values)

        def simulated_annealing(problem):
            A = initialize(LIMIT)
            A = problem.courses
            print("A:", A)

            local_minima = []
            for i in range(len(A)):
                if(isminima_local(i, A)):
                    local_minima.append([i, A[i]])

            local_maxima = []
            for i in range(len(A)):
                if(ismaxima_local(i, A)):
                    local_maxima.append([i, A[i]])

            print("local minima:")
            for idx, course in local_minima:
                print("{}->{}".format(idx, course.value))

            print("local maxima:")
            for idx, course in local_maxima:
                print("{}->{}".format(idx, course.value))

            x = 0
            y = A[x].value
            for xi, yi in enumerate(A):
                print("xi", xi)
                print("yi", yi)

                if yi.value < y:
                    x = xi
                    y = yi.value
            global_minimum = x

            # Reorder the problem using local maxima

            print("number of local minima: %d" % (len(local_minima)))
            print("global minimum @%d = %0.3f" % (global_minimum, A[global_minimum].value))

            problem = reorder_as_courses_local_maxima(problem, local_maxima)
            A = problem.courses
            x, x_best, x0 = search.sa(A, problem, TIME_LIMIT_SECONDS)
            print("Solution is @%d = %1.3f" % (x, A[x].value))
            print("Best solution is @%d = %0.3f" % (x_best, A[x_best].value))
            print("Start solution is @%d = %0.3f" % (x0, A[x0].value))

            # Update global maxima
            problem = reorder_as_courses_global_maxima(problem, (x_best, A[x_best]))
            print(problem.getEmptySchedule())
            return problem


    test1 = simulated_annealing(test1)  # Updates problem's indices
    solution = search.naiveBaseline(test1, deadline)

    #     solution = search.sa(test1, deadline)
    #     print("DONE!")
    #
    # else:
    #     print("ERROR: Given algorithm number does not exist!")
    #     exit(1)
    #
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
