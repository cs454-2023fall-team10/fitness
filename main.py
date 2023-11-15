import utils, user_fitness, admin_fitness

def fitness(graph, users) :
    # nodes = graph.nodes
    user_fitness_sum = 0
    
    DEPTH_THRESHOLD = admin_fitness.get_depth_threshold(graph)
    DISTANCE_THRESHOLD = 0
    alpha = 0.5

    admin_fitness_val = admin_fitness.get_admin_fitness()
    for user in users :
        user_fitness_sum += user_fitness.get_user_fitness(user.intent, graph, DEPTH_THRESHOLD, DISTANCE_THRESHOLD)
    
    user_fitness_avg = user_fitness_sum / len(users)
    
    return alpha * user_fitness_avg + (1 - alpha) * admin_fitness_val


if __name__ == "__main__" :
    json_file = "jobs-homepage.json"
    graph = utils.make_graph(json_file)
    print(graph.nodes["A"]["text"])
    print(graph["A"])
    # users = ["AAA"]

    # fitness_val = fitness(graph, users)
    # print(fitness_val)