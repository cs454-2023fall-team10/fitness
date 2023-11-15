import json
import os
import networkx as nx



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

def make_graph(json_file):
    dir_path = os.getcwd() # cs353-2023fall-team10/fitness
    print(f"dir_path: {dir_path}")
    os.chdir("../chatbot-dataset/examples")
    file_path = os.getcwd() + f"/{json_file}"

    with open(file_path, "r") as file:
        data = json.load(file)["sections"]

    
    DG = nx.DiGraph()

    for section in data:
        DG.add_node(section["id"])
        DG.nodes[section["id"]]["text"] = f"\"{section['text']}\""
    
    for section in data:
        if section["type"] == "stop":
            continue
        for button in section["buttons"]:
            DG.add_edge(section["id"], button["nextSectionId"], text = button["text"])

    return DG

def load_intents(rel_file_path) :
    intents = []
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), rel_file_path)) as f :
        for line in f :
            intents.append(line.rstrip())
    
    return intents

# def get_all_nodes(json_file) :
#     nodes = {}
#     with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), json_file)) as f :
#         j = json.loads(f)
#         for section in j["sections"] :
#             section_id = section["id"]
#             nodes[section_id] = section
        
#         return nodes
