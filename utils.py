import json
import os
import networkx as nx
import random

# import functions
# import models

from . import functions, models

_cache = {}


def _cached(func):
    def wrapper(*args):
        if args not in _cache:
            _cache[args] = func(*args)
        return _cache[args]

    return wrapper


# Sentencebert or OpenAI
if functions.model_name == "sentence_bert":
    model = models.BertEmbedding("jhgan/ko-sroberta-multitask")
elif functions.model_name == "openai":
    model = models.OpenAIEmbedding("text-embedding-ada-002")
else:
    print("Select appropriate model. Can fix in functions.py")
    exit(0)


def _sentence_similarity(sentence1, sentence2):
    return model.sentence_similarity(sentence1, sentence2)


_sentence_similarity_cached = _cached(_sentence_similarity)


def sentence_similarity(sentence1, sentences):
    if type(sentences) is list:
        results = []
        for sentence in sentences:
            results.append(_sentence_similarity_cached(sentence1, sentence))

        return results

    elif type(sentences) is str:
        return _sentence_similarity_cached(sentence1, sentences)

    else:
        print("should put sentence(s)")
        return 0


def make_graph(json_file):
    with open(
        os.path.join(os.getcwd(), "chatbot-dataset/examples", json_file), "r"
    ) as file:
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


def _load_intents(file_path):
    intents = []
    try:
        with open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"./chatbot-dataset/intents/gpt-4-1106-preview/{file_path}",
            )
        ) as f:
            for line in f:
                intents.append(line.rstrip())
    except:
        print(f"Intent for {file_path} does not exist.")
        exit(0)

    return intents
    # return random.sample(intents, min(100, len(intents)))


load_intents = _cached(_load_intents)

# def get_all_nodes(json_file) :
#     nodes = {}
#     with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), json_file)) as f :
#         j = json.loads(f)
#         for section in j["sections"] :
#             section_id = section["id"]
#             nodes[section_id] = section

#         return nodes
