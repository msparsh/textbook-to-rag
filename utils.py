import re

from uuid import uuid4

from anytree import RenderTree, Node
from anytree.importer import JsonImporter
from anytree.exporter import JsonExporter


def generate_unique_id():
    return str(uuid4())


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", " ", text)
    return text


class TextTree:
    def read_tree_from_json(self, input_file):
        # Read the JSON data from the JSON FILE
        with open(input_file, "r") as f:
            json_data = f.read()

        # Deserialize the tree from JSON
        importer = JsonImporter()
        root = importer.import_(json_data)
        print("Read tree from JSON file.")
        return root

    def write_tree_into_json(self, root, output_file):
        # Serialize the tree to JSON
        exporter = JsonExporter(indent=2, sort_keys=False)
        json_data = exporter.export(root)

        # Save the JSON data to a file
        with open("out/hierarchy.json", "w") as f:
            f.write(json_data)
        print("Wrote tree to JSON file.")

    def print_tree(self, root):
        for pre, fill, node in RenderTree(root):
            # print(f"{pre}{node.name} (ID: {node.id})")
            print(f"{pre}{node.name}")

    def create_tree(self, chapters, sections, paragraphs, txt_file_name):
        root = Node(f"Textbook: {txt_file_name}", id=generate_unique_id())
        for i, _ in enumerate(chapters):
            chapter_node = Node(
                f"Chapter {i + 1}", parent=root, id=generate_unique_id()
            )
            for j, _ in enumerate(sections[i]):
                section_node = Node(
                    "Section", parent=chapter_node, id=generate_unique_id()
                )
                for k, para in enumerate(paragraphs[i][j]):
                    Node(f"{para}", parent=section_node, id=generate_unique_id())
        return root
