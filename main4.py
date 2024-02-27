import argparse
import dataclasses
import pathlib
import sys

import spacy

COMPLETE_LIST_FILE = "complete-list.txt"

nlp = spacy.load("en_core_web_sm")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Recursively walk through a directory and gather absolute paths of files"
    )
    parser.add_argument("--path", type=str, default=".", help="Path to the directory")
    parser.add_argument("--depth", type=int, help="Maximum depth for recursive walking")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Strings to exclude from file paths",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Strings to include in file paths",
    )
    return parser.parse_args()


def search_for_person_filetypes(file_paths):
    result_paths = []
    for file_path in file_paths:
        with open(file_path, "r") as file:
            content = file.read()
            if "filetype: person" in content:
                result_paths.append(file_path)
    return result_paths


def get_files(path, max_depth=None, current_depth=0):
    files = []
    for file_path in pathlib.Path(path).iterdir():
        if file_path.is_file():
            files.append(file_path.absolute())
        elif file_path.is_dir() and (max_depth is None or current_depth < max_depth):
            files.extend(get_files(file_path, max_depth, current_depth + 1))
    return files


def filter_files(files, exclusions, inclusions):
    filtered_files = []
    for file_path in files:
        path_str = str(file_path)
        if any(exclusion in path_str for exclusion in exclusions):
            continue
        if not inclusions or any(inclusion in path_str for inclusion in inclusions):
            filtered_files.append(file_path)
    return filtered_files


@dataclasses.dataclass
class FilePersons:
    file_name: str
    persons: list


def find_persons(text):
    max_text_length = 1_000_000
    max_text_length = 5_000
    if len(text) > max_text_length:
        # print warning to stderr
        print(
            f"Warning: text is too long, only the first {max_text_length} characters will be processed.",
            file=sys.stderr,
        )
        text = text[:max_text_length]
    doc = nlp(text)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return persons


def find_persons_in_files(file_paths):
    file_persons_list = []
    for file_path in file_paths:
        print(f"{file_path}")
        path = pathlib.Path(file_path)
        if not path.exists():
            print(f"File '{file_path}' does not exist.")
        else:
            with path.open("r") as file:
                text = file.read()
                persons = find_persons(text)
                file_persons = FilePersons(file_name=file_path, persons=persons)
                file_persons_list.append(file_persons)
    return file_persons_list


def append_to_completed_paths(file_paths):
    with open(COMPLETE_LIST_FILE, "a") as completed_file:
        for file_path in file_paths:
            completed_file.write(str(file_path) + "\n")


if __name__ == "__main__":
    args = parse_arguments()
    # Load already processed paths
    try:
        with open(COMPLETE_LIST_FILE, "r") as completed_file:
            completed_paths = completed_file.read().splitlines()
    except FileNotFoundError:
        completed_paths = []

    files = get_files(args.path, args.depth)
    # Filter out already processed files
    files = [file_path for file_path in files if file_path not in completed_paths]

    filtered_files = filter_files(files, args.exclude, args.include)
    filtered_files = list(set(filtered_files) - set(completed_paths))
    z = search_for_person_filetypes(filtered_files)
    filtered_files = list(set(filtered_files) - set(z))

    file_paths = filtered_files

    print(f"Completed paths length: {len(completed_paths)}")
    print(f"Files length: {len(file_paths)}")

    file_persons_list = find_persons_in_files(file_paths)

    for file_persons in file_persons_list:
        if file_persons.persons:
            r = ", ".join(file_persons.persons)
            r = r.replace("\n", " ")
            y = r[:100]
            print(f"{file_persons.file_name}: {y}")

    # Append new paths to complete-list.txt
    append_to_completed_paths(file_paths)
