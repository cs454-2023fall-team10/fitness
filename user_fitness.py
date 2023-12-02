from . import utils
import numpy as np
from . import functions


# nodes should be a dict of all existing nodes : {id: raw_node}
# def get_best_sentence(intent, choices, similarity_threshold):
#     ids = []
#     texts = []

#     for select in choices.items():
#         ids.append(select[0])
#         texts.append(select[1]["text"])

#     scores = utils.sentence_similarity(intent, texts)
#     top_result_idx = np.argsort(scores)[::-1][0]

#     # if top result if below threshold, we should stop searching
#     return "Exit" if scores[top_result_idx] < similarity_threshold else ids[top_result_idx]


# def get_best_choice(intent, choices, similarity_threshold):
#     if len(choices) == 0:
#         # Reached at the bottom, stop searching
#         return "Leaf"

#     return get_best_sentence(intent, choices, similarity_threshold)

def calculate_choices(intent, choices) :
    ids = []
    texts = []

    for select in choices.items():
        ids.append(select[0])
        texts.append(select[1]["text"])

    return ids, texts, utils.sentence_similarity(intent, texts)

def get_path(intent, graph, DEPTH_THRESHOLD, DISTANCE_THRESHOLD):
    curr_node_id = "A" # initial node
    path = []
    current_depth = 0
    penalty = 0

    while current_depth < DEPTH_THRESHOLD:
        path.append(curr_node_id)
        choices = graph[curr_node_id] # choices from current node

        # ids : Next node's id,
        # texts : Choice's texts, 
        # similarities : Choice's similarities
        ids, texts, similarities = calculate_choices(intent, choices)
        similarity_threshold = functions.get_similarity_threshold(DEPTH_THRESHOLD, DISTANCE_THRESHOLD, current_depth)  

        # If similarities are empty : nothing to calculate(= Leaf node)
        if not similarities :
            next_node_id = "Leaf"
        else : 
            top_result_idx = np.argsort(similarities)[::-1][0]
            next_node_id = "Exit" if similarities[top_result_idx] < similarity_threshold else ids[top_result_idx]

        if next_node_id == "Leaf": # Reached at bottom
            break
        elif next_node_id == "Exit" : # Search stopped, should give penalty
            penalty = functions.similarity_penalty(similarities, similarity_threshold)
            break
        else: # move to next node
            curr_node_id = next_node_id
            current_depth += 1

    return (curr_node_id, path, penalty)


def get_user_fitness(intent, graph, DEPTH_THRESHOLD, DISTANCE_THRESHOLD):
    (final_node_id, path, penalty) = get_path(intent, graph, DEPTH_THRESHOLD, DISTANCE_THRESHOLD)

    # print(path, DEPTH_THRESHOLD)

    if len(path) >= DEPTH_THRESHOLD :
        penalty -= functions.depth_penalty(DEPTH_THRESHOLD)

    final_sentence = graph.nodes[final_node_id]["text"]
    final_similarity = utils.sentence_similarity(intent, final_sentence)

    return functions.get_user_fitness(DEPTH_THRESHOLD, DISTANCE_THRESHOLD, len(path), final_similarity, penalty)


# if __name__ == "__main__":
#     # for test only
#     json_file = "lead-homepage.json"
#     graph = utils.make_graph(json_file)
#     intents = utils.load_intents("../embedding-metrics/examples/gpt-4-1106-preview/jobs-homepage")
#     intent = "가나다"
#     DEPTH_THRESHOLD = 10
#     DISTANCE_THRESHOLD = 0.6
#     result = get_user_fitness(intent, graph, DEPTH_THRESHOLD, DISTANCE_THRESHOLD)
#     print(result)
