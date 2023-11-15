import utils
import numpy as np

# nodes should be a dict of all existing nodes : {id: raw_node}
def get_best_sentence(intent, node) :
    ids = []
    choices = []

    for select in node.items() :
        ids.append(select[0])
        choices.append(select[1]['text'])

    scores = utils.sentence_similarity(intent, choices)
    top_result_idx = np.argpartition(scores, range(1))[0]

    return ids[top_result_idx]


def get_best_choice(intent, node) :
    if len(node) == 0 :
        return ""
    
    return get_best_sentence(intent, node)

def get_path_length(intent, graph, DEPTH_THRESHOLD) :
    curr_node_id = "A"
    count = 0

    while count < DEPTH_THRESHOLD :
        curr_node = graph[curr_node_id]
        next_node_id = get_best_choice(intent, curr_node)
        if next_node_id == "" :
            break
        else :
            curr_node_id = next_node_id
            count += 1
    
    return (curr_node_id, count)

def get_user_fitness(intent, graph, DEPTH_THRESHOLD, DISTANCE_THRESHOLD) :
    (final_node_id, path_length) = get_path_length(intent, graph, DEPTH_THRESHOLD)
    if (path_length >= DEPTH_THRESHOLD) :
        return -utils.inf
    
    # print("path_length: ", path_length)
    final_sentence = graph.nodes[final_node_id]["text"]
    # print(final_sentence)
    final_similarity = utils.sentence_similarity(intent, final_sentence)
    
    return (DEPTH_THRESHOLD - path_length) + (final_similarity - DISTANCE_THRESHOLD)

if __name__ == "__main__" :
    json_file = "lead-homepage.json"
    graph = utils.make_graph(json_file)
    intent = "가나다"
    DEPTH_THRESHOLD = 10
    DISTANCE_THRESHOLD = 0.5
    result = get_user_fitness(intent, graph, DEPTH_THRESHOLD, DISTANCE_THRESHOLD)
    print(result)