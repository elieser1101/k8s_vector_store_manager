import os
import pathlib

def get_recursive_files_paths(directory):
    desktop = pathlib.Path(directory)
    desktop.rglob("*")
    result = list(desktop.rglob("*.md"))
    print(len(result))
    print(result[0])
    return result


def load_kubernetes_docs(directory):
    files_paths = get_recursive_files_paths(directory)
    documents = []
    
    for filename in files_paths:
        if filename.is_file():
            print(f'Reading: {filename}')
            with open(filename, "r", encoding="utf-8") as file:
                documents.append(file.read())
    print("Document count") 
    print(len(documents))
    return documents