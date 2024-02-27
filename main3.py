import argparse
import pathlib

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

def main():
    args = parse_arguments()
    files = get_files(args.path, args.depth)
    filtered_files = filter_files(files, args.exclude, args.include)
    for file in filtered_files:
        print(file)

if __name__ == "__main__":
    main()
