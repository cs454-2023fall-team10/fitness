import numpy as np

class BertEmbedding:
    def __init__(self, model_name):
        """
        Load BERT model.
        """
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(model_name)
        self._embedding_cache = {}

    def embedding(self, sentence):
        """
        Return embedding of given sentence.
        """
        if sentence not in self._embedding_cache:
            self._embedding_cache[sentence] = self._model.encode(sentence)
        return self._embedding_cache[sentence]

    def sentence_similarity(self, s1, s2):
        """
        Evaluates similarity of two setences.
        """
        from sentence_transformers import util

        s1_embedding = self.embedding(s1)
        s2_embedding = self.embedding(s2)

        return util.pytorch_cos_sim(s1_embedding, s2_embedding)[0][0]
    
class OpenAIEmbedding:
    def __init__(self, model_name):
        """
        Load OpenAI model.
        """
        from openai import OpenAI

        self._client = OpenAI()
        self.model_name = model_name
        self._embedding_cache = {}

    def embedding(self, sentence):
        """
        Return embedding of given sentence.
        """
        if sentence not in self._embedding_cache:
            response = self._client.embeddings.create(
                input=[sentence], model=self.model_name
            )
            self._embedding_cache[sentence] = response.data[0].embedding
        return self._embedding_cache[sentence]

    def sentence_similarity(self, s1, s2):
        """
        Evaluates similarity of two setences.
        """
        s1_embedding = self.embedding(s1)
        s2_embedding = self.embedding(s2)

        return np.dot(s1_embedding, s2_embedding) / (
            np.linalg.norm(s1_embedding) * np.linalg.norm(s2_embedding)
        )