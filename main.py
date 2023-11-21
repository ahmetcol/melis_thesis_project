from consts import *
import pandas as pd

# Python program to print all paths from a source to destination.

from collections import defaultdict


# This class represents a directed graph
# using adjacency list representation
class Graph:

    def __init__(self, vertices):
        # No. of vertices
        self.V = vertices

        # default dictionary to store graph
        # self.graph = defaultdict(list)
        self.graph = duration_matrix

        self.all_paths = []

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    '''A recursive function to print all paths from 'u' to 'd'.
    visited[] keeps track of vertices in current path.
    path[] stores actual vertices and path_index is current
    index in path[]'''

    def printAllPathsUtil(self, u, d, visited, path):
        # Mark the current node as visited and store in path
        visited[u] = True
        path.append(u)

        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            self.all_paths.append(path.copy())
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i, dist in self.graph[u].items():
                if not dist:
                    continue
                if visited[i] == False:
                    self.printAllPathsUtil(i, d, visited, path)

        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u] = False

    # Prints all paths from 's' to 'd'
    def AllPaths(self, s, d):

        # Mark all the vertices as not visited
        # visited = [False] * (self.V)
        visited = {n: False for n in self.graph.keys()}
        # Create an array to store paths
        path = []

        # Call the recursive helper function to print all paths
        self.printAllPathsUtil(s, d, visited, path)
        return self.all_paths


def find_info_durations(path: list):
    info = 0
    time = 0
    for idx, node in enumerate(path):
        # Sum information amount for current node
        info += info_amounts.get(node, 0)

        # Add distance(duration) between prev. node and current node
        if not idx:
            prev_node = path[idx-1]
            time += duration_matrix[prev_node][node]

        # Check for if time is between time windows
        if node != "-1":  # The last node has not any time window
            if not (time_windows[node][0] <= time <= time_windows[node][-1]):
                return info, time, False

        # Add information duration
        time += info_durations.get(node, 0)
    return info, time, True


def main():
    df = pd.DataFrame({'path': pd.Series(dtype='object'),
                       'total_time': pd.Series(dtype='int'),
                       'info_amount': pd.Series(dtype='int')})
    nodes = list(duration_matrix.keys())
    graph = Graph(len(nodes))
    list_of_paths = graph.AllPaths(nodes[0], nodes[-1])
    # breakpoint()

    # Find time and information amount for each path and store them inside DataFrame
    for p in list_of_paths:
        info, time, is_applicable = find_info_durations(p)
        if is_applicable:
            df.loc[len(df.index)] = [p, time, info]

    # TODO: sıralama yaptırt

    print(df)


main()