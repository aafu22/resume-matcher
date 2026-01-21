from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        # ✅ smaller model -> less RAM (good for Render free tier)
        _model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    return _model
