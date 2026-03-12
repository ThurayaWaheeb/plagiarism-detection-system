from sentence_transformers import SentenceTransformer

# تحميل المودل مرة واحدة
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
)

def get_embedding(text):

    vector = model.encode(text)

    return vector.tolist()