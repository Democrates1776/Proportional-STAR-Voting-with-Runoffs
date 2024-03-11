import random

# Get user input for the number of groups and numbers per group
num_groups = int(input("Enter the number of voters: "))
num_per_group = int(input("Enter the number of candidates: "))

# Generate and print the groups of random numbers
for i in range(num_groups):
    group = "".join(str(random.randint(0, 5)) for _ in range(num_per_group))
    print(group, end=" ")
