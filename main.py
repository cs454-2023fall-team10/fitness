import utils, user_fitness, admin_fitness

def fitness(graph, users) :
    json_file_name = "a.json"
    nodes = utils.get_all_nodes(json_file_name)
    user_fitness_sum = 0
    
    DEPTH_THRESHOLD = 10 # admin_fitness.function()
    DISTANCE_THRESHOLD = 0
    alpha = 0.5

    admin_fitness = admin_fitness.admin_fitness()
    for user in users :
        user_fitness_sum += user_fitness.user_fitness(user.intent, nodes, DEPTH_THRESHOLD, DISTANCE_THRESHOLD)
    
    user_fitness_avg = user_fitness_sum / len(users)
    
    return alpha * user_fitness_avg + (1 - alpha) * admin_fitness
