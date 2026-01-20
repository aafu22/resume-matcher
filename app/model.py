from sentence_transformers import SentenceTransformer

# Load model ONCE at startup
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_model():
    return model
