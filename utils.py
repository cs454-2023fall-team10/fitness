import json
import os
import networkx as nx

def sentence_similarity(sentence1, sentence2):
    import random
    # temporary value
    return random.random()

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
            DG.add_edge(section["id"], button["nextSectionId"])

    return DG
