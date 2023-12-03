# import admin_fitness
# import functions
# import log
# import user_fitness
# import utils

from . import admin_fitness, log, user_fitness, utils, functions


def fitness(graph, file_path):
    user_fitness_sum = 0

    DEPTH_THRESHOLD = admin_fitness.get_depth_threshold(graph)

    # admin_fitness_val = admin_fitness.get_admin_fitness(graph)

    # Just a list of intents
    # If some features are added in users in future, we need to fix this
    users = utils.load_intents(file_path)
    if len(users) == 0:
        raise ValueError("Give appropriate file path. Can fix in functions.py")

    for user in users:
        user_fitness_sum += user_fitness.get_user_fitness(
            user, graph, DEPTH_THRESHOLD, functions.DISTANCE_THRESHOLD
        )

    user_fitness_avg = user_fitness_sum / len(users)

    # log.debug("admin_fitness_val:", admin_fitness_val)
    # log.debug("user_fitness_avg:", user_fitness_avg)

    # alpha = functions.alpha
    # return float(alpha * user_fitness_avg + (1 - alpha) * admin_fitness_val)

    return float(user_fitness_avg)


def _log_fitness(graph_name):
    graph = utils.make_graph(f"{graph_name}.json")
    log.debug(f"Fitness of {graph_name}:", fitness(graph, graph_name))


if __name__ == "__main__":
    _log_fitness("kakaotalk-faq-231129")
    _log_fitness("kakaotalk-faq-231129-small")
    _log_fitness("kakaotalk-faq-231129-small-mingled-001")
    _log_fitness("kakaotalk-faq-231129-small-mingled-002")
    _log_fitness("kakaotalk-faq-231129-small-mingled-003")
