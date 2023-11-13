inf = 10 ** 10

def sentence_similarity(sentence1, sentences) :
    import random

    # should be fixed
    if type(sentences) is list :
        # calculate all sentences
        return [random.random() for _ in range(len(sentences))]
    elif type(sentences) is str :
        # calculate one sentence
        return random.random()
    else :
        print("should put sentence(s)")
        return 0

def make_adjacency_graph(graph) :
    return

def make_graph(json_file) :
    return

def get_all_nodes(json_file) :
    import os, json
    nodes = {}
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), json_file)) as f :
        j = json.loads(f)
        for section in j["sections"] :
            section_id = section["id"]
            nodes[section_id] = section
        
        return nodes