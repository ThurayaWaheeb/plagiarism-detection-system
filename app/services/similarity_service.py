from sentence_transformers import SentenceTransformer, util
import torch
from collections import Counter


# تحميل الموديل مرة واحدة فقط
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')


def check_similarity(student_chunks, db_chunks, db_metadata):

    db_embeddings = model.encode(db_chunks, convert_to_tensor=True)

    THRESHOLD = 0.70
    doc_matches = Counter()
    detailed_report = []

    for s_chunk in student_chunks:

        s_emb = model.encode(s_chunk, convert_to_tensor=True)

        search_results = util.semantic_search(s_emb, db_embeddings, top_k=1)[0]

        best_match = search_results[0]
        score = best_match['score']

        if score >= THRESHOLD:

            matched_db_index = best_match['corpus_id']
            matched_project = db_metadata[matched_db_index]

            doc_matches[matched_project["id"]] += 1

            detailed_report.append({
                "student_text": s_chunk,
                "original_text": db_chunks[matched_db_index],
                "score": float(score),
                "project_title": matched_project["title"]
            })

    return doc_matches, detailed_report