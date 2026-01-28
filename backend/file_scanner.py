import os

def scan_folders(folder_paths, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = [".txt", ".pdf", ".docx"]

    files_index = []

    for folder in folder_paths:
        for root, _, files in os.walk(folder):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in allowed_extensions:
                    files_index.append({
                        "file_name": file,
                        "file_path": os.path.join(root, file),
                        "extension": ext
                    })

    return files_index


def find_file_by_name(files_index, query):
    query = query.lower()
    results = []

    for file in files_index:
        if query in file["file_name"].lower():
            results.append(file)

    return results
