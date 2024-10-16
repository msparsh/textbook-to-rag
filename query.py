import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from anytree import PostOrderIter
from index_text_into_hierarchy import read_tree
from transformers import pipeline

# nltk.download("wordnet")
from nltk.corpus import wordnet

def expand_query(query):
    tokens = query.split()
    expanded_tokens = []
    for token in tokens:
        synonyms = set()
        for syn in wordnet.synsets(token):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        expanded_tokens.extend(list(synonyms) if synonyms else [token])
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


# Load and preprocess data
root = read_tree("out/hierarchy.json")
texts, leaf_nodes = extract_leaf_text_data(root)
processed_documents = preprocess_text(texts)

# Initialize BM25 and SentenceTransformer
bm25 = BM25Okapi(processed_documents)
model = SentenceTransformer('all-MiniLM-L6-v2')
paragraph_embeddings = model.encode(texts, convert_to_tensor=True)

# Define query and retrieve relevant sections
query = "What is recursion ?"
#expanded_query = expand_query(query)
retrieved = dense_retrieval(query, n_retrieved=8)

# Generate a coherent response using transformers
generator = pipeline("text-generation", model='gpt2')
response_input = retrieved[0]

# Generate response with adjusted token length
response =generator(response_input,  max_length = 500, min_length=150)
print(response[0]["generated_text"])

# Save results
with open("out/query_output.txt", "w") as file:
    file.write("\n\n".join(retrieved))

with open("out/generated_query_response.txt", "w") as file:
    file.write(response[0]["generated_text"])
