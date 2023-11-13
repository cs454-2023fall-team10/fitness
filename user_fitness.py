import utils
import numpy as np

def get_best_sentence(intent, choices) :
    scores = utils.sentence_similarity(intent, choices)
    top_result = np.argpartition(scores, range(1))[0:1]
    
    return top_result

def get_choices(d) :
    choices = []
    raw_choices = []
    try :
        raw_choices = d["buttons"]
        for button in raw_choices :
            choices.append(button["text"])
    except :
        pass
    
    return (raw_choices, choices)

def get_best_choice(intent, nodes, node) :
    raw_node = nodes[node]
    (raw_choices, choices) = get_choices(raw_node)
    if len(raw_choices) == 0 :
        return ""
    
    best_choice_idx = get_best_sentence(intent, choices)

    section_id = raw_choices[best_choice_idx]["nextSectionId"]

    return section_id

def get_path_length(intent, nodes, DEPTH_THRESHOLD) :
    root_node = nodes[0]
    count = 0
    curr_node = root_node["id"]

    while count < DEPTH_THRESHOLD :
        next_node = get_best_choice(intent, nodes, curr_node)
        if next_node == "" :
            break
        else :
            curr_node = next_node
            count += 1
    
    return (curr_node, count)

def user_fitness(DEPTH_THRESHOLD, )
