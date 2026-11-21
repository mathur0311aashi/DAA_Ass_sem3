
# INTELLIGENT TASK SCHEDULING AND RESOURCE ALLOCATION

# Step 1: Creating the task dataset

import time

tasks = [
    {"id": "T1", "start": 1, "finish": 3, "priority": 5},
    {"id": "T2", "start": 2, "finish": 5, "priority": 8},
    {"id": "T3", "start": 4, "finish": 6, "priority": 6},
    {"id": "T4", "start": 6, "finish": 8, "priority": 10},
    {"id": "T5", "start": 5, "finish": 9, "priority": 7},
    {"id": "T6", "start": 8, "finish": 10, "priority": 9},
    {"id": "T7", "start": 3, "finish": 7, "priority": 12},
    {"id": "T8", "start": 9, "finish": 11, "priority": 4},
    {"id": "T9", "start": 10, "finish": 13, "priority": 11},
    {"id": "T10", "start": 11, "finish": 14, "priority": 6},
    {"id": "T11", "start": 13, "finish": 15, "priority": 8},
    {"id": "T12", "start": 14, "finish": 17, "priority": 13},
    {"id": "T13", "start": 16, "finish": 19, "priority": 7},
    {"id": "T14", "start": 18, "finish": 20, "priority": 10},
    {"id": "T15", "start": 19, "finish": 22, "priority": 15}
]

# Step 2: Defining available resources

resources = ["Resource 1", "Resource 2", "Resource 3"]


# Step 3: Displaying all tasks

print("=" * 65)
print("       INTELLIGENT TASK SCHEDULING SYSTEM")
print("=" * 65)

print("\nAVAILABLE TASKS")
print("-" * 65)

print(f"{'Task ID':<12}{'Start':<12}{'Finish':<12}{'Priority':<12}")
print("-" * 65)

for task in tasks:
    print(f"{task['id']:<12}{task['start']:<12}{task['finish']:<12}{task['priority']:<12}")

print("\nAVAILABLE RESOURCES")
print("-" * 30)

for resource in resources:
    print(resource)

print("\nTotal Tasks:", len(tasks))
print("Total Resources:", len(resources))



# STEP 3: GREEDY ALGORITHM - ACTIVITY SELECTION

def greedy_scheduling(tasks):

    # Step 1: Sort tasks according to finishing time
    sorted_tasks = sorted(tasks, key=lambda x: x["finish"])

    # Step 2: Create an empty list for selected tasks
    selected_tasks = []

    # Step 3: Select the first task
    selected_tasks.append(sorted_tasks[0])

    # Store the finish time of the first selected task
    last_finish_time = sorted_tasks[0]["finish"]

    # Step 4: Check the remaining tasks
    for task in sorted_tasks[1:]:

        # Check whether the current task is compatible
        if task["start"] >= last_finish_time:

            # Select the task
            selected_tasks.append(task)

            # Update the last finish time
            last_finish_time = task["finish"]

    return selected_tasks


# STEP 3: DISPLAY GREEDY SCHEDULING RESULTS

greedy_result = greedy_scheduling(tasks)

print("\n" + "=" * 65)
print("             GREEDY ALGORITHM - ACTIVITY SELECTION")
print("=" * 65)

print(f"{'Task ID':<12}{'Start':<12}{'Finish':<12}{'Priority':<12}")
print("-" * 65)

for task in greedy_result:
    print(f"{task['id']:<12}{task['start']:<12}{task['finish']:<12}{task['priority']:<12}")

print("-" * 65)

print("Total Selected Tasks:", len(greedy_result))
print("Total Priority:", sum(task["priority"] for task in greedy_result))




# STEP 4: DYNAMIC PROGRAMMING - WEIGHTED INTERVAL SCHEDULING

from bisect import bisect_right


def dp_scheduling(tasks):

    # Step 1: Sort tasks according to finishing time
    sorted_tasks = sorted(tasks, key=lambda x: x["finish"])

    n = len(sorted_tasks)

    # Store all finishing times
    finish_times = [task["finish"] for task in sorted_tasks]

    # Step 2: Find the previous compatible task for each task
    compatible = []

    for i in range(n):
        count = bisect_right(finish_times, sorted_tasks[i]["start"], 0, i)
        compatible.append(count)

    # Step 3: Create a DP table
    dp = [0] * (n + 1)

    # Step 4: Calculate maximum priority
    for i in range(1, n + 1):

        task = sorted_tasks[i - 1]

        # Option 1: Include current task
        include = task["priority"] + dp[compatible[i - 1]]

        # Option 2: Exclude current task
        exclude = dp[i - 1]

        # Store the maximum result
        dp[i] = max(include, exclude)

    # Step 5: Reconstruct the selected tasks
    selected_tasks = []
    i = n

    while i > 0:

        task = sorted_tasks[i - 1]

        include = task["priority"] + dp[compatible[i - 1]]
        exclude = dp[i - 1]

        if include > exclude:
            selected_tasks.append(task)
            i = compatible[i - 1]

        else:
            i -= 1

    # Reverse to get chronological order
    selected_tasks.reverse()

    return selected_tasks, dp


# STEP 4: DISPLAY DP RESULTS

dp_result, dp_table = dp_scheduling(tasks)

print("\n" + "=" * 65)
print("       DYNAMIC PROGRAMMING - WEIGHTED INTERVAL SCHEDULING")
print("=" * 65)

print(f"{'Task ID':<12}{'Start':<12}{'Finish':<12}{'Priority':<12}")
print("-" * 65)

for task in dp_result:
    print(f"{task['id']:<12}{task['start']:<12}{task['finish']:<12}{task['priority']:<12}")

print("-" * 65)

print("Total Selected Tasks:", len(dp_result))
print("Maximum Total Priority:", dp_table[-1])

print("\nDP TABLE")
print("-" * 40)

for i, value in enumerate(dp_table):
    print(f"DP[{i}] = {value}")





# STEP 5: RESOURCE ALLOCATION - INTERVAL PARTITIONING

def allocate_resources(tasks, resources):

    # Step 1: Sort tasks by their start time
    sorted_tasks = sorted(tasks, key=lambda x: x["start"])

    # Step 2: Store the last finishing time of each resource
    resource_end_times = [0] * len(resources)

    # Step 3: Create a dictionary to store allocated tasks
    allocation = {resource: [] for resource in resources}

    # Step 4: Assign tasks to available resources
    unallocated_tasks = []

    for task in sorted_tasks:

        # Find resources that are free before this task starts
        available_resources = [
            i for i in range(len(resources))
            if resource_end_times[i] <= task["start"]
        ]

        if available_resources:

            # Choose the available resource that becomes free earliest
            best_resource = min(
                available_resources,
                key=lambda i: resource_end_times[i]
            )

            # Assign the task
            resource = resources[best_resource]
            allocation[resource].append(task)

            # Update the resource's finishing time
            resource_end_times[best_resource] = task["finish"]

        else:
            # No resource is available
            unallocated_tasks.append(task)

    return allocation, unallocated_tasks


# STEP 5: DISPLAY RESOURCE ALLOCATION RESULTS

allocation, unallocated_tasks = allocate_resources(tasks, resources)

print("\n" + "=" * 65)
print("                RESOURCE ALLOCATION RESULTS")
print("=" * 65)

for resource, assigned_tasks in allocation.items():

    print("\n" + resource)
    print("-" * 40)

    for task in assigned_tasks:
        print(
            f"{task['id']} | "
            f"Start: {task['start']} | "
            f"Finish: {task['finish']}"
        )

    busy_time = sum(
        task["finish"] - task["start"]
        for task in assigned_tasks
    )

    print("Total Busy Time:", busy_time)

# Display unallocated tasks
print("\nUNALLOCATED TASKS:")

if unallocated_tasks:
    for task in unallocated_tasks:
        print(task["id"])
else:
    print("None")

# Calculate overall resource utilization
total_busy_time = sum(
    task["finish"] - task["start"]
    for task in tasks
)

total_duration = (
    max(task["finish"] for task in tasks)
    - min(task["start"] for task in tasks)
)

total_available_time = len(resources) * total_duration

utilization = (total_busy_time / total_available_time) * 100

print("\n" + "-" * 40)
print("Total Tasks:", len(tasks))
print("Allocated Tasks:", len(tasks) - len(unallocated_tasks))
print("Available Resources:", len(resources))
print("Total Busy Time:", total_busy_time)
print("Total Available Resource Time:", total_available_time)
print(f"Resource Utilization: {utilization:.2f}%")




# STEP 7: PERFORMANCE COMPARISON

def compare_performance(tasks):

    repetitions = 1000

    # Measure Greedy execution time
    start_time = time.perf_counter()

    for _ in range(repetitions):
        greedy_scheduling(tasks)

    greedy_time = time.perf_counter() - start_time

    # Measure DP execution time
    start_time = time.perf_counter()

    for _ in range(repetitions):
        dp_scheduling(tasks)

    dp_time = time.perf_counter() - start_time

    # Calculate average time in milliseconds
    greedy_average = (greedy_time / repetitions) * 1000
    dp_average = (dp_time / repetitions) * 1000

    print("\n5. PERFORMANCE COMPARISON")
    print("-" * 50)

    print("Greedy Average Time:", round(greedy_average, 6), "ms")
    print("DP Average Time:", round(dp_average, 6), "ms")

    print("\nTIME COMPLEXITY")
    print("Greedy: O(n log n)")
    print("Dynamic Programming: O(n log n)")

    print("\nSPACE COMPLEXITY")
    print("Greedy: O(n)")
    print("Dynamic Programming: O(n)")

    if greedy_average < dp_average:
        print("\nGreedy was faster in this test.")
    elif dp_average < greedy_average:
        print("\nDynamic Programming was faster in this test.")
    else:
        print("\nBoth algorithms took approximately equal time.")






# STEP 8: GREEDY VS DP COMPARISON

test_tasks = [
    {"id": "A", "start": 1, "finish": 2, "priority": 2},
    {"id": "B", "start": 2, "finish": 3, "priority": 2},
    {"id": "C", "start": 3, "finish": 4, "priority": 2},
    {"id": "D", "start": 1, "finish": 4, "priority": 20}
]

print("\nGREEDY VS DP COMPARISON")
print("=" * 50)

greedy_result = greedy_scheduling(test_tasks)
dp_result, dp_table = dp_scheduling(test_tasks)

print("\nGreedy Selected Tasks:")
for task in greedy_result:
    print(task["id"])

print("Number of Tasks:", len(greedy_result))
print("Total Priority:",
      sum(task["priority"] for task in greedy_result))

print("\nDP Selected Tasks:")
for task in dp_result:
    print(task["id"])

print("Number of Tasks:", len(dp_result))
print("Maximum Total Priority:", dp_table[-1])