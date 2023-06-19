import requests
import os
import git

import json

def filter_code_files(file_paths):
    # List of code file extensions.
    code_file_extensions = ['.py', '.js', '.java', '.c', '.cpp', '.cs', '.go', '.rb', '.php', '.ipynb', '.md']

    code_files = [file for file in file_paths if os.path.splitext(file)[1] in code_file_extensions]

    return code_files

def extract_python_code_from_notebook(file_path):
    notebook = json.loads(file_path)

    python_code = ""
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            python_code += ''.join(cell['source']) + '\n\n'

    return python_code

def tokenize_and_chunk(content, max_tokens=1000):
    lines = content.split('\n')
    chunks = []
    current_chunk = ""
    current_token_count = 0

    for line in lines:
        if not line.strip().startswith('#'):
            line_tokens = line.split()  # split line into tokens at whitespace
            if current_token_count + len(line_tokens) <= max_tokens:
                current_chunk += line + "\n"
                current_token_count += len(line_tokens)
            else:
                chunks.append(current_chunk)
                current_chunk = line + "\n"
                current_token_count = len(line_tokens)

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def get_github_repos(user_url, git_api):
    username = user_url.split('/')[-1]
    git_api = git_api.replace('username', username)
    response = requests.get(git_api)
    repos = response.json()
    return repos


def clone_and_preprocess(repo_url):
    # Clone the repo
    try:
        git.Git().clone(repo_url)
        repo_name = repo_url.split('/')[-1]
        # Gather all file paths
        file_paths = []
        for root, dirs, files in os.walk(repo_name):
            for file in files:
                file_paths.append(os.path.join(root, file))

        file_paths = filter_code_files(file_paths)

        preprocessed_files = {}
        for file_path in file_paths:
            try:
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                    if '.ipynb' in file_path:
                        content = extract_python_code_from_notebook(content)
                    # Break down into smaller pieces if necessary
                    preprocessed_files[file_path.split('/')[1]] = tokenize_and_chunk(content)
            except Exception as e:
                print(f"Couldn't process file {file_path}. Reason: {e}")
    except Exception as e:
        if 'exists and is not an empty directory.' in str(e):
            repo_name = repo_url.split('/')[-1]
            print(os.listdir(repo_name))

            # Gather all file paths
            file_paths = []
            for file in os.listdir(repo_name):
                # print(file)
                # for file in files:
                if file[0] != '.':
                    file_paths.append(os.path.join(repo_name, file))
            file_paths = filter_code_files(file_paths)

            preprocessed_files = {}
            for file_path in file_paths:
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        content = f.read()
                        if '.ipynb' in file_path:
                            content = extract_python_code_from_notebook(content)
                        # Break down into smaller pieces if necessary
                        preprocessed_files[file_path.split('/')[1]] = tokenize_and_chunk(content)
                except Exception as e:
                    print(f"Couldn't process file {file_path}. Reason: {e}")
        else:
            preprocessed_files = {'error': str(e)}
    return preprocessed_files