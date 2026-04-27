from .utils import cosine_similarity, normalize_text


class Cache:
    def __init__(self, embedding_model, storage, threshold=0.80):
        self.embedding_model = embedding_model
        self.storage = storage
        self.threshold = threshold

    def ask(self, query: str):
        query = normalize_text(query)
        embedding = self.embedding_model.encode(query)

        cached_entries = self.storage.get_all()
        for entry in cached_entries:
            similarity = cosine_similarity(embedding, entry["embedding"])
            if similarity >= self.threshold:
                return entry["response"]

        return None

    def save(self, query: str, response: str, expires_in=3600):
        query = normalize_text(query)
        embedding = self.embedding_model.encode(query)
        self.storage.save(query, embedding, response, expires_in)
