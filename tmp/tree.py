from bigtree import Node
import numpy as np

def calculate_partition_cost_with_unique_ancestors(partition_nodes):
    """Calculate the cost of a partition with unique ancestor costs using bigtree nodes."""
    unique_ancestors = {}
    
    # Collect all unique ancestors in this partition
    for leaf in partition_nodes:
        # Traverse ancestors and add costs to unique_ancestors
        for ancestor in leaf.ancestors:
            if ancestor.name not in unique_ancestors:
                unique_ancestors[ancestor.name] = ancestor.cost
    
    # The partition cost is the sum of unique ancestor costs
    return sum(unique_ancestors.values())

def max_partition_size(partition_nodes):
    """Define a function that returns the maximum allowed partition size based on partition cost."""
    # Example rule: if partition cost exceeds 40, limit max size to 1, otherwise allow up to 2 leaves
    unique_ancestors = {}
    
    # Collect all unique ancestors in this partition
    for leaf in partition_nodes:
        # Traverse ancestors and add costs to unique_ancestors
        for ancestor in leaf.ancestors:
            if ancestor.name not in unique_ancestors:
                unique_ancestors[ancestor.name] = ancestor.cost
    
    max_size = 1
    for i in unique_ancestors.values():
        max_size += 0.2 * np.log(i)
    max_size = np.floor(max_size)
    print([a.name for a in partition_nodes], max_size)
    return max_size

def minimize_partition_cost_with_dynamic_max_size(leaves):
    n = len(leaves)
    dp = [float('inf')] * (n + 1)  # Initialize DP array with infinity
    dp[0] = 0  # Base case: no cost for zero leaves

    # For each leaf position, compute minimum partition cost up to that point
    for i in range(1, n + 1):
        # Try to form partitions of variable size up to the max allowed size
        for k in range(1, i + 1):  # k can vary up to `i` as max size is dynamically set
            if i - k >= 0:
                # Calculate the partition cost and dynamically determine max partition size
                partition = leaves[i - k:i]
                partition_cost = calculate_partition_cost_with_unique_ancestors(partition)
                max_size = max_partition_size(partition)
                
                # Only proceed if the partition size `k` is within the allowed max size
                if k <= max_size:
                    dp[i] = min(dp[i], dp[i - k] + partition_cost)

    # Reconstruct partitions from dp array
    i = n
    partitions = []
    while i > 0:
        # Find the best partition size `k` that was used to minimize cost at `dp[i]`
        for k in range(1, i + 1):
            if i - k >= 0:
                partition = leaves[i - k:i]
                partition_cost = calculate_partition_cost_with_unique_ancestors(partition)
                max_size = max_partition_size(partition)
                
                if k <= max_size and dp[i] == dp[i - k] + partition_cost:
                    partitions.append(leaves[i - k:i])
                    i -= k
                    break

    partitions.reverse()  # To get the partitions in left-to-right order
    return dp[n], partitions

# Example tree setup using bigtree
# Define nodes with ancestor costs

root = Node("root", cost=25)
c = Node("C", cost=5, parent=root)
d = Node("D", cost=0, parent=c)
e = Node("E", cost=0, parent=c)
f = Node("F", cost=15, parent=root)
g = Node("G", cost=0, parent=f)
h = Node("H", cost=0, parent=f)
i = Node("I", cost=0, parent=root)

# Leaves
leaves = [d, e, g, h, i]

# Run the algorithm
min_cost, partitions = minimize_partition_cost_with_dynamic_max_size(leaves)

print("Minimum Cost:", min_cost)
print("Partitions:")
for partition in partitions:
    print([leaf.name for leaf in partition])

root.show(attr_list=["cost"])