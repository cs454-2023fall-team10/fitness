import utils
import numpy as np

INF = 2**31


# nodes should be a dict of all existing nodes : {id: raw_node}
def get_best_sentence(intent, node, similarity_threshold):
    ids = []
    choices = []

    for select in node.items():
        ids.append(select[0])
        choices.append(select[1]["text"])

    scores = utils.sentence_similarity(intent, choices)
    top_result_idx = np.argpartition(scores, range(1))[0]

    # print(scores[top_result_idx], similarity_threshold)

    return "Exit" if scores[top_result_idx] < similarity_threshold else ids[top_result_idx]


def get_best_choice(intent, node, similarity_threshold):
    if len(node) == 0:
        return ""

    return get_best_sentence(intent, node, similarity_threshold)


def get_path_length(intent, graph, DEPTH_THRESHOLD, DISTANCE_THRESHOLD):
    curr_node_id = "A"
    count = 0
    threshold = False
    while count < DEPTH_THRESHOLD:
        curr_node = graph[curr_node_id]
        similarity_threshold = (DISTANCE_THRESHOLD / DEPTH_THRESHOLD) * count
        next_node_id = get_best_choice(intent, curr_node, similarity_threshold)

        if next_node_id == "":
            break
        elif next_node_id == "Exit" :
            threshold = True
            break
        else:
            curr_node_id = next_node_id
            count += 1

    return (curr_node_id, count, threshold)


def get_user_fitness(intent, graph, DEPTH_THRESHOLD, DISTANCE_THRESHOLD):
    (final_node_id, path_length, threshold) = get_path_length(intent, graph, DEPTH_THRESHOLD, DISTANCE_THRESHOLD)

    if path_length >= DEPTH_THRESHOLD or threshold:
        return -INF

    # print("path_length: ", path_length)
    final_sentence = graph.nodes[final_node_id]["text"]
    # print(final_sentence)
    final_similarity = utils.sentence_similarity(intent, final_sentence)

    return (DEPTH_THRESHOLD - path_length) + final_similarity


if __name__ == "__main__":
    # for test only
    json_file = "lead-homepage.json"
    graph = utils.make_graph(json_file)
    intents = utils.load_intents("../embedding-metrics/examples/jobs-homepage")
    intent = "가나다"
    DEPTH_THRESHOLD = 10
    DISTANCE_THRESHOLD = 0.6
    result = get_user_fitness(intent, graph, DEPTH_THRESHOLD, DISTANCE_THRESHOLD)
    print(result)
