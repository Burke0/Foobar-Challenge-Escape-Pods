from collections import deque

# A function to perform breadth-first search (BFS) to find a path from source s to sink t
# and update the parent array to keep track of the path
# graph: the graph represented as an adjacency matrix
# s: the source node
# t: the sink node
# parent: an array to keep track of the path
def bfs(graph, s, t, parent):
    n = len(graph)
    visited = [False] * n
    queue = deque()
    queue.append(s)
    visited[s] = True
    parent[s] = -1

    # perform BFS until there are no more nodes in the queue
    while queue:
        u = queue.popleft()
        # iterate through all the adjacent nodes of u
        for v, capacity in enumerate(graph[u]):
            if visited[v] == False and capacity > 0:
                # if v is not visited and there is available capacity between u and v,
                # add v to the queue, mark it as visited, and update the parent array
                queue.append(v)
                visited[v] = True
                parent[v] = u

                # if we have found the sink node t, we can terminate the search and return True
                if v == t:
                    return True

    # if we have not found the sink node t, return False
    return False

# A function to find the maximum flow in the given graph using the Ford-Fulkerson algorithm
# graph: the graph represented as an adjacency matrix
# s: the source node
# t: the sink node
def max_flow(graph, s, t):
    n = len(graph)
    parent = [-1] * n  # initialize the parent array to all -1s
    max_flow = 0

    # repeatedly find a path from source to sink using BFS and update the flow
    while bfs(graph, s, t, parent):
        # find the minimum capacity in the path found by BFS
        path_flow = float("Inf")
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            v = u

        # update the flow by subtracting the path flow from forward edges
        # and adding the path flow to backward edges
        v = t
        while v != s:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = u

        # add the path flow to the total maximum flow
        max_flow += path_flow

    # return the maximum flow found
    return max_flow

# A function to find the maximum flow that can be sent from the entrances to the exits
# entrances: a list of entrance nodes
# exits: a list of exit nodes
# path: the graph represented as an adjacency matrix
def solution(entrances, exits, path):
    n = len(path)
    # create a new graph with two additional nodes, one as source and one as sink
    graph = [[0] * (n + 2) for _ in range(n + 2)]

    # copy the values from the given graph into the new graph
    for i in range(n):
        for j in range(n):
            graph[i][j] = path[i][j]

    # set the capacities of the edges from source to entrance nodes to infinity
    for i in entrances:
        graph[n][i] = float("Inf")

    # set the capacities of the edges from exit nodes to sink to infinity
    for i in exits:
        graph[i][n + 1] = float("Inf")

    return max_flow(graph, n, n + 1)