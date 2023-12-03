from . import utils, user_fitness, admin_fitness, functions
import importlib

def fitness(graph, file_path):
    importlib.reload(functions)
    # nodes = graph.nodes
    user_fitness_sum = 0

    DEPTH_THRESHOLD = admin_fitness.get_depth_threshold(graph)
    
    # Sometimes, transformation graph can be empty
    # In this case, return immediately
    if DEPTH_THRESHOLD == -2**31 :
        return -2**31

    admin_fitness_val = admin_fitness.get_admin_fitness(graph)

    # Just a list of intents
    # If some features are added in users in future, we need to fix this
    users = utils.load_intents(file_path)
    if len(users) == 0 :
        print("Give appropriate file path. Can fix in functions.py")
        return -2**31
    
    for user in users:
        user_fitness_sum += user_fitness.get_user_fitness(
            user, graph, DEPTH_THRESHOLD, functions.DISTANCE_THRESHOLD
        )

    user_fitness_avg = user_fitness_sum / len(users)

    alpha = functions.alpha
    print("User fitness: {}, Admin fitness: {}, alpha: {}".format(user_fitness_avg, admin_fitness_val, alpha))
    return float(alpha * user_fitness_avg + (1 - alpha) * admin_fitness_val)


if __name__ == "__main__":
    json_file = "general-homepage.json"
    graph = utils.make_graph(json_file)
    # print(graph.nodes["A"]["text"])
    # print(graph["A"])

    fitness_val = fitness(graph)
    print(fitness_val)
