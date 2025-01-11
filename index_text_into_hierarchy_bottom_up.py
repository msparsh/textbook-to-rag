import nltk
from nltk.tokenize import sent_tokenize

from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.utils import simple_preprocess

from utils import TextTree, clean_text

# Download the tokenizer models
nltk.download("punkt")


def split_into_hierarchy(sentences):
    def get_topics(sentences, num_topics=4, passes=15):
        processed_sentences = [simple_preprocess(sentence) for sentence in sentences]
        dictionary = Dictionary(processed_sentences)
        corpus = [dictionary.doc2bow(sentence) for sentence in processed_sentences]
        lda_model = LdaModel(
            corpus, num_topics=num_topics, id2word=dictionary, passes=passes
        )
        sentence_topics = [lda_model.get_document_topics(bow) for bow in corpus]

        return sentence_topics

    def dominant_topic(topics):
        return max(topics, key=lambda x: x[1])[0]

    def detect_topic_changes(topic_distributions, threshold=0.2):
        changes = []
        print(topic_distributions[0])
        for i in range(1, len(topic_distributions)):
            # Check if the most probable topic changes significantly
            current_dominant = max(topic_distributions[i], key=lambda x: x[1])
            previous_dominant = max(topic_distributions[i - 1], key=lambda x: x[1])
            if (
                current_dominant[0] != previous_dominant[0]
                and abs(current_dominant[1] - previous_dominant[1]) > threshold
            ):
                changes.append(1)
            else:
                changes.append(0)
        return [0] + changes

    def segment_text(sentences, topic_changes):
        segments = []
        current_segment = []

        for sentence, change in zip(sentences, topic_changes):
            if change and current_segment:
                segments.append(" ".join(current_segment))
                current_segment = []
            current_segment.append(sentence)
        if current_segment:
            segments.append(" ".join(current_segment))

        return segments

    dominant_topics = detect_topic_changes(get_topics(sentences, num_topics=32))
    paragraphs = segment_text(sentences, dominant_topics)

    dominant_topics = detect_topic_changes(get_topics(paragraphs, num_topics=4))
    sections = segment_text(paragraphs, dominant_topics)

    dominant_topics = detect_topic_changes(get_topics(sections, num_topics=2))
    chapters = segment_text(sections, dominant_topics)

    return chapters, sections, paragraphs


def text_to_tree(txt_file_name):
    try:
        with open(txt_file_name, "r") as file:
            text = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("Error: File '{txt_file_name}' not found.")
    if text == "":
        raise ValueError("Expected non-empty text file!")

    text = clean_text(text)
    sentences = sent_tokenize(text)
    chapters, sections, paragraphs = split_into_hierarchy(sentences)

    # tree = TextTree()
    # root = tree.create_tree(chapters, sections, paragraphs, txt_file_name)
    # # Print the tree using RenderTree
    # tree.print_tree(root)
    # tree.write_tree_into_json(root, txt_file_name)
    # return root

    print(len(paragraphs), len(sections), len(chapters))


if __name__ == "__main__":
    text_to_tree("out/textfile.txt")
