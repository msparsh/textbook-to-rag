import re
import nltk
from nltk.tokenize import sent_tokenize
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.utils import simple_preprocess

from anytree import Node, RenderTree
from uuid import uuid4

# Download the tokenizer models
nltk.download('punkt')


def generate_unique_id():
    return str(uuid4())


def print_tree(root):
    for pre, fill, node in RenderTree(root):
        print(f"{pre}{node.name} (ID: {node.id})")


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", " ", text)
    return text


def split_into_hierarchy(sentences, min_len_chapters=15000, min_len_sections=7500, min_len_paragraphs=1500):
    # Preprocess sentences
    processed_sentences = [simple_preprocess(sentence) for sentence in sentences]

    # Create a dictionary and corpus for LDA
    dictionary = Dictionary(processed_sentences)
    corpus = [dictionary.doc2bow(sentence) for sentence in processed_sentences]

    # Train an LDA model
    lda_model = LdaModel(corpus, num_topics=8, id2word=dictionary, passes=12)

    # Get the topic distribution for each sentence
    sentence_topics = [lda_model.get_document_topics(bow) for bow in corpus]

    # Helper function to find the dominant topic
    def dominant_topic(topics):
        return max(topics, key=lambda x: x[1])[0]

    # Find dominant topic for each sentence
    dominant_topics = [dominant_topic(topics) for topics in sentence_topics]

    # Detect topic changes for each level
    def detect_topic_changes(topics):
        return [0] + [1 if topics[i] != topics[i - 1] else 0 for i in range(1, len(topics))]

    # Segment text based on topic changes and minimum length for each level
    def segment_text(sentences, min_len):
        topic_changes = detect_topic_changes(dominant_topics)
        segments = []
        current_segment = []

        for sentence, change in zip(sentences, topic_changes):
            if (change and current_segment) and len(" ".join(current_segment)) >= min_len:
                segments.append(" ".join(current_segment))
                current_segment = []
            current_segment.append(sentence)
        if current_segment:
            segments.append(" ".join(current_segment))

        return segments

    # Segment into chapters, sections, and paragraphs
    chapters = segment_text(sentences, min_len_chapters)
    sections = [segment_text(sent_tokenize(chap), min_len_sections) for chap in chapters]
    paragraphs = [[segment_text(sent_tokenize(sec), min_len_paragraphs) for sec in section] for section in sections]

    return chapters, sections, paragraphs


def text_to_tree(txt_file_name, n_chapters=15, n_sections=5, n_paragraphs=7):
    n_chapters = 15
    n_sections = 5
    n_paragraphs = 7

    try:
        with open(txt_file_name, "r") as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{txt_file_name}' not found.")
        exit()

    text = clean_text(text)

    min_len_chapters = int(len(text) / n_chapters)
    min_len_sections = int(min_len_chapters / n_sections)
    min_len_paragraphs = int(min_len_sections / n_paragraphs)

    sentences = sent_tokenize(text)
    chapters, sections, paragraphs = split_into_hierarchy(sentences, min_len_chapters, min_len_sections,
                                                          min_len_paragraphs)

    root = Node("Textbook", id=generate_unique_id())

    # Create the tree
    for i, _ in enumerate(chapters):
        chapter_node = Node(f"Chapter {i + 1}", parent=root, id=generate_unique_id())
        for j, _ in enumerate(sections[i]):
            section_node = Node(f"Section {j + 1}", parent=chapter_node, id=generate_unique_id())
            for k, para in enumerate(paragraphs[i][j]):
                Node(f"Paragraph {k + 1}: {para}", parent=section_node, id=generate_unique_id())

    # Print the tree using RenderTree
    print_tree(root)
    return root


if __name__ == "__main__":
    text_to_tree("PrinciplesofFinance-WEB.pdf.txt")
