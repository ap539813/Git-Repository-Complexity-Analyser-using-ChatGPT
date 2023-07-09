# Importing necessary modules for sending HTTP requests, handling operating system related tasks and dealing with git repositories
import requests
import os
import git
# json module for parsing and manipulating JSON data
import json
import time

# Function to filter out code files based on their extensions
def filter_code_files(file_paths):
    # List of code file extensions.
    code_file_extensions = ['.py', '.js', '.java', '.c', '.cpp', '.cs', '.go', '.rb', '.php', '.ipynb', '.md']

    # Filtering files with extensions matching with the extensions in the code_file_extensions list
    code_files = [file for file in file_paths if os.path.splitext(file)[1] in code_file_extensions]

    return code_files

# Function to extract Python code from a Jupyter notebook file
def extract_python_code_from_notebook(file_path):
    # Loading the notebook file content
    notebook = json.loads(file_path)

    python_code = ""
    # Looping through each cell in the notebook
    for cell in notebook['cells']:
        # Checking if the cell is a code cell
        if cell['cell_type'] == 'code':
            # Joining all the code in the cell and appending it to python_code
            python_code += ''.join(cell['source']) + '\n\n'
    return python_code

# Function to break a content into chunks of code without breaking individual tokens
def tokenize_and_chunk(content, max_tokens=1000):
    lines = content.split('\n')
    chunks = []
    current_chunk = ""
    current_token_count = 0

    # Going through each line of the content
    for line in lines:
        # Checking if the line is not a comment
        if not line.strip().startswith('#'):
            # Splitting line into tokens at whitespace
            line_tokens = line.split()
            # Checking if adding the current line's tokens does not exceed the max_tokens limit
            if current_token_count + len(line_tokens) <= max_tokens:
                current_chunk += line + "\n"
                current_token_count += len(line_tokens)
            else:
                # If adding the current line's tokens exceeds the max_tokens limit, add current chunk to chunks and start a new chunk
                chunks.append(current_chunk)
                current_chunk = line + "\n"
                current_token_count = len(line_tokens)

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


# Function to get a list of all the repositories of a GitHub user
def get_github_repos(user_url):
    # Extracting the username from the URL
    username = user_url.split('/')[-1]
    
    # Getting the GitHub API token from the environment variable
    git_api = os.getenv('GIT_API')
    
    # Checking if the API token is available
    if git_api is None:
        return ValueError("GitHub API token not found. Set the GIT_API environment variable.")
    
    # Replacing 'username' in the git_api URL with the actual username
    git_api = git_api.replace('username', username)
    
    # Sending a GET request to the GitHub API with authentication
    response = requests.get(git_api, headers={'Authorization': f'token {git_api}'})
    
    # Checking the rate limit status
    remaining_requests = int(response.headers.get('X-RateLimit-Remaining', 0))
    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
    
    if remaining_requests == 0:
        # Rate limit exceeded, wait until reset_time and then retry
        wait_time = reset_time - time.time() + 10  # Add an additional buffer of 10 seconds
        time.sleep(wait_time)
        return get_github_repos(user_url)
    
    # Parsing the JSON response
    repos = response.json()
    return repos


# Function to clone a GitHub repository and preprocess its files
def process_repository(repo_url):
    # Variable to hold preprocessed files
    preprocessed_files = {}

    # Try to clone the repo
    try:
        git.Git().clone(repo_url)
        repo_name = repo_url.split('/')[-1]
        # Gather all file paths in the repository
        file_paths = []
        for root, dirs, files in os.walk(repo_name):
            for file in files:
                file_paths.append(os.path.join(root, file))

        # Filter out code files
        file_paths = filter_code_files(file_paths)

        # Loop through each code file
        for file_path in file_paths:
            try:
                # Read the file content
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                    # If the file is a Jupyter notebook, extract Python code from it
                    if '.ipynb' in file_path:
                        content = extract_python_code_from_notebook(content)
                    # Break the content into chunks and add them to the preprocessed_files dictionary
                    preprocessed_files[file_path.split('/')[1]] = tokenize_and_chunk(content)
            except Exception as e:
                print(f"Couldn't process file {file_path}. Reason: {e}")

    except Exception as e:
        # If the repository is already cloned
        if 'exists and is not an empty directory.' in str(e):
            repo_name = repo_url.split('/')[-1]
            print(os.listdir(repo_name))

            # Gather all file paths in the repository
            file_paths = []
            for file in os.listdir(repo_name):
                # Ignore hidden files
                if file[0] != '.':
                    file_paths.append(os.path.join(repo_name, file))
            # Filter out code files
            file_paths = filter_code_files(file_paths)

            # Loop through each code file
            for file_path in file_paths:
                try:
                    # Read the file content
                    with open(file_path, 'r', errors='ignore') as f:
                        content = f.read()
                        # If the file is a Jupyter notebook, extract Python code from it
                        if '.ipynb' in file_path:
                            content = extract_python_code_from_notebook(content)
                        # Break the content into chunks and add them to the preprocessed_files dictionary
                        preprocessed_files[file_path.split('/')[1]] = tokenize_and_chunk(content)
                except Exception as e:
                    print(f"Couldn't process file {file_path}. Reason: {e}")
        else:
            preprocessed_files = {'error': str(e)}

    # Return the preprocessed files
    return preprocessed_files
