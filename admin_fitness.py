import math

INF = 2**31

def get_admin_fitness(graph):
    num_of_nodes = len(graph.nodes)
    num_of_edges = len(graph.edges)
    optimal_degrees = math.round(num_of_edges/num_of_nodes)
    max_degrees = 2*optimal_degrees

    sum_of_diffs = 0

    for node in graph.nodes:
        if (len(graph[node])) > max_degrees:
            return -INF
        sum_of_diffs += abs(optimal_degrees - len(graph[node]))
    
    fitness = 1 - sum_of_diffs/num_of_edges

    return fitness

def get_depth_threshold(graph):
    num_of_nodes = len(graph.nodes)
    num_of_edges = len(graph.edges)
    optimal_degrees = round(num_of_edges/num_of_nodes)
    
    return math.log(num_of_nodes, optimal_degrees)