import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, util

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download("wordnet")
from nltk.corpus import wordnet

from anytree import PostOrderIter

from index_text_into_hierarchy import read_tree


def expand_query(query):
    # Tokenize the query
    tokens = query.split()

    # Expand tokens with synonyms
    expanded_tokens = []
    for token in tokens:
        synonyms = set()
        for syn in wordnet.synsets(token):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        expanded_tokens.extend(list(synonyms) if synonyms else [token])

    # Combine expanded tokens into a new query
    expanded_query = " OR ".join(expanded_tokens)
    return expanded_query


def extract_leaf_text_data(root):
    text_data = []
    leaf_nodes = []
    for node in PostOrderIter(root):
        if node.is_leaf:
            text_data.append(node.name)
            leaf_nodes.append(node)
    return text_data, leaf_nodes


def preprocess_text(documents):
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()

    processed_documents = []
    for doc in documents:
        tokens = word_tokenize(doc.lower())
        tokens = [ps.stem(word) for word in tokens if word.isalnum() and word not in stop_words]
        processed_documents.append(tokens)
    return processed_documents


def dense_retrieval(query, n_retrieved=3):
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, paragraph_embeddings)[0]
    top_k_indices = np.argsort(scores.numpy())[-n_retrieved:][::-1]
    return [texts[i] for i in top_k_indices]


root = read_tree("Introduction to Computation and Programming Using Python by John V. Guttag (z-lib.org).pdf.txt.json")
texts, leaf_nodes = extract_leaf_text_data(root)
processed_documents = preprocess_text(texts)

query = "what is python language"
expanded_query = query

# Create BM25 index
bm25 = BM25Okapi(processed_documents)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Compute paragraph embeddings
paragraph_embeddings = model.encode(texts, convert_to_tensor=True)

# Retrieve
print("Dense Retrieval Results:")
retrieved = dense_retrieval(query, 10)
for para in retrieved:
    print(para)

with open("query_output.txt", "w") as file:
    file.write("\n\n".join(retrieved))