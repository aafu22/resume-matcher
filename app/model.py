from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        # ✅ smallest & fastest mini model
        _model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")
    return _model
