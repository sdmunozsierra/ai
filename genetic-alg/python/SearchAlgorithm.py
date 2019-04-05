"""SearchAlgorithm class implementation."""

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


    @staticmethod
    def simulated_annealing(problem, deadline):
        pass
