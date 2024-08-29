# Text Extraction, Indexing, and Retrieval System

This project is a Python-based system designed to extract text from PDF documents, organize the extracted text into a hierarchical structure (chapters, sections, paragraphs), and perform query-based retrieval on the organized text. The system uses various NLP techniques, including topic modeling and dense retrieval.

## Project Structure

- **extractor.py**: This script is responsible for extracting text from PDF files and saving the extracted content into a text file.
- **index_text_into_hierarchy.py**: This script takes the extracted text and organizes it into a hierarchical structure of chapters, sections, and paragraphs. It uses topic modeling (LDA) to detect topic changes and segment the text.
- **query.py**: This script allows users to query the hierarchical text data and retrieve the most relevant sections. It supports query expansion with synonyms and uses both BM25 and dense retrieval methods.

## Prerequisites

To run this project, you need to have the following Python packages installed:

- `PyMuPDF` (fitz)
- `PyPDF2`
- `nltk`
- `gensim`
- `anytree`
- `rank_bm25`
- `sentence_transformers`
- `numpy`

You can install these dependencies using pip:

```bash
pip install pymupdf PyPDF2 nltk gensim anytree rank_bm25 sentence_transformers numpy
```

Additionally, make sure to download the required NLTK data:

```python
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
```

## Usage

### 1. Extract Text from PDF

Use `extractor.py` to extract text from a PDF file. The extracted text is saved as a `.txt` file.

```bash
python extractor.py
```

### 2. Index Text into a Hierarchical Structure

Use `index_text_into_hierarchy.py` to segment the extracted text into chapters, sections, and paragraphs. The segmented text is organized into a tree structure and saved as a JSON file.

```bash
python index_text_into_hierarchy.py
```

### 3. Perform Query on the Text Data

Use `query.py` to perform a query on the hierarchical text data. The script will retrieve and print the most relevant sections based on the query, and save the results to a text file.

```bash
python query.py
```

## Example

An example of a typical workflow might look like this:

1. Extract text from the PDF `Introduction to Computation and Programming Using Python by John V. Guttag`.
2. Index the extracted text into a hierarchical structure.
3. Query the hierarchical structure for relevant information, such as "What is Python language?".

## License

This project is licensed under the MIT License.

## Acknowledgments

- The text processing and NLP techniques used in this project are based on libraries like NLTK, Gensim, and Sentence Transformers.
- The hierarchical indexing is made possible by the `anytree` library.
- Retrieval techniques are powered by `rank_bm25` and `sentence_transformers`.
