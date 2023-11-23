import json
import os
import networkx as nx
from models import *
from functions import model_name

# Sentencebert or OpenAI
if model_name == "sentence_bert" :
    model = BertEmbedding("jhgan/ko-sroberta-multitask")
elif model_name == "openai" :
    model = OpenAIEmbedding("text-embedding-ada-002")
else :
    print("Select appropriate model. Can fix in functions.py")
    exit(0)
    
def sentence_similarity(sentence1, sentences):
    if type(sentences) is list:
        results = []
        for sentence in sentences :
            results.append(model.sentence_similarity(sentence1, sentence))
        
        return results
    
    elif type(sentences) is str:
        return model.sentence_similarity(sentence1, sentences)
    
    else:
        print("should put sentence(s)")
        return 0


def make_graph(json_file):
    dir_path = os.getcwd()  # cs353-2023fall-team10/fitness
    # print(f"dir_path: {dir_path}")
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
            DG.add_edge(section["id"], button["nextSectionId"], text=button["text"])

    return DG


def load_intents(rel_file_path):
    intents = []
    try :
        with open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), rel_file_path)
        ) as f:
            for line in f:
                intents.append(line.rstrip())
    except :
        print("Wrong intent_file_path. Can change in functions.py")
        exit(0)

    return intents


# def get_all_nodes(json_file) :
#     nodes = {}
#     with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), json_file)) as f :
#         j = json.loads(f)
#         for section in j["sections"] :
#             section_id = section["id"]
#             nodes[section_id] = section

#         return nodes
