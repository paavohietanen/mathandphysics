from random import randint


def binary_search(array, target, iteration):
    left = 0
    right = len(array) - 1
    print("RIGHT:", right, "TARGET:", target)
    if left <= right:
        mid_floored = left + right // 2
        print("WHILE ON TEST:", mid_floored)
        print("ARRAY IS", array)
        if array[mid_floored] == target:
            return True, iteration
        elif array[mid_floored] < target:
            print("SO CLIPPING LEFT", array[mid_floored + 1:])
            return binary_search(array[mid_floored + 1:], target, iteration + 1)
        elif array[mid_floored] > target:
            print("SO CLIPPING RIGHT", array[:mid_floored - 1])
            return binary_search(array[:mid_floored - 1], target, iteration + 1)
    else:
        return False, iteration

array_size = 10000
trials = 30
sum_of_iters = 0
no_of_fails = 0

for i in range(0, trials):
    array = []
    for j in range(0, array_size):
        array.append(randint(0, array_size))
    array.sort()
    target = array[randint(0, array_size - 1)]
    result, iterations = binary_search(array, target, 1)
    print("Result is", result, "with", iterations, "iterations\n\n")
    if result:
        sum_of_iters += iterations
    else:
        no_of_fails += 1

print("Average iterations for finding the answer:", sum_of_iters / trials)
print("Number of fails:", no_of_fails)