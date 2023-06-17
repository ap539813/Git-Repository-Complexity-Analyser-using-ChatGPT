import requests
import os
import git

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
        # Assume repo name is last part of URL
        repo_name = repo_url.split('/')[-1]

        # Gather all file paths
        file_paths = []
        for root, dirs, files in os.walk(repo_name):
            for file in files:
                file_paths.append(os.path.join(root, file))

        # Preprocess files (simplified)
        preprocessed_files = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                    # Break down into smaller pieces if necessary
                    # Add your own logic here
                    preprocessed_files.append(content)
            except Exception as e:
                print(f"Couldn't process file {file_path}. Reason: {e}")
    except Exception as e:
        if 'exists and is not an empty directory.' in str(e):
            # Assume repo name is last part of URL
            repo_name = repo_url.split('/')[-1]
            print(os.listdir(repo_name))

            # Gather all file paths
            file_paths = []
            for file in os.listdir(repo_name):
                # print(file)
                # for file in files:
                if file[0] != '.':
                    file_paths.append(os.path.join(repo_name, file))

            # Preprocess files (simplified)
            preprocessed_files = {}
            for file_path in file_paths:
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        content = f.read()
                        # Break down into smaller pieces if necessary
                        # Add your own logic here
                        preprocessed_files[file_path.split('/')[1]] = content
                except Exception as e:
                    print(f"Couldn't process file {file_path}. Reason: {e}")
        else:
            preprocessed_files = [str(e)]
    return preprocessed_files

