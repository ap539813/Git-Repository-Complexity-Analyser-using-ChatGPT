# Importing necessary modules
import streamlit as st
from important_variables import logo_image
from langchain import PromptTemplate, LLMChain

# Importing utility functions for working with GitHub and preprocessing code repositories
from utils import get_github_repos, process_repository
from important_variables import git_api

# Function for the main application logic
def main():
    # Get user input for GitHub user ID
    username = st.text_input("Input Git Use Id:")
    if username != '':
        # Get the GitHub repositories of the user
        result = get_github_repos(username, git_api)
        # st.write(result)
        try:
            # Extract the URLs of the repositories
            repo_links = [git_repo['html_url'] for git_repo in result]
            # Extract the names of the repositories
            repo_names = [repo_link.split('/')[-1] for repo_link in repo_links]
            # Create a dictionary mapping repository names to URLs
            repo_to_link = {repo_names[i]:repo_links[i] for i in range(len(repo_names))}
            # Let the user select the repositories they want to analyse
            selected_repo_list = st.multiselect("Select the git repositories: ", options = repo_names, default = repo_names[:1])
            # User click the 'Analyse' button to start the analysis
            analyse_button = st.button('Analyse')
            repo_col, final_col = st.columns([6, 5])
            if analyse_button:
                conversation_history = ""
                # Loop through each selected repository
                for single_selected_repo in selected_repo_list:
                    selected_repo_url = repo_to_link[single_selected_repo]
                    git_repo = selected_repo_url.split('/')[-1]
                    # Preprocess the repository (clone it and tokenize the code files)
                    preprocessed_files = process_repository(selected_repo_url)
                    # Get the language model instance
                    llm = st.session_state['GPT']

                    # Template for summarising a repository
                    template_for_code = """
                    Code Files: {filenames} | Repository Name: {git_repository_name}

                    Instr:
                    1. Summarise the overall logic of the code.
                    2. Focus on code.
                    4. Write the answerd in report format with headings and subheadings with proper structure, the headings are as below use subheadings as needed.
                        a. Included Code Files
                        b. Code Summary
                        c. Space and Time Complexity

                    Answer:
                    """

                    # Create a PromptTemplate instance with the template and input variables
                    prompt_repo = PromptTemplate(
                        template = template_for_code,
                        input_variables=["filenames", "git_repository_name"]
                    )

                    # Create a LLMChain instance for generating the summary of the repository
                    llm_chain = LLMChain(prompt=prompt_repo, llm=llm)
                    code_summary = llm_chain.run(
                        git_repository_name = git_repo,
                        conversation_history = conversation_history,
                        filenames = preprocessed_files,
                    )

                    # Add the summary of the repository to the conversation history
                    conversation_history += f'REPOSITORY NAME:\n{username}/{git_repo}\n\nSUMMARY:\n{code_summary}'
                    # Display the repository name and summary
                    repo_i = repo_col.expander(f'Description of: {git_repo}')
                    repo_i.markdown(f'### REPOSITORY NAME: {username}/{git_repo}')
                    repo_i.markdown(f'{code_summary}', unsafe_allow_html = True)

                # Template for comparing repositories and identifying the most complex one
                template_for_final = """
                Conversation history: {conversation_history} | 

                Question:
                Which code repository among {selected_repo_list} has the most technically complex and challenging.

                Instructions:
                Refer to the Conversation history. Give answer in two sections with following headings and required subheadings:
                    1. Most Complex code Repository: 
                    2. Explanation
                Provide output in html format
                """

                # Create a PromptTemplate instance with the template and input variables
                prompt_final = PromptTemplate(
                    template = template_for_final,
                    input_variables=["conversation_history", "selected_repo_list"]
                )

                # Create a LLMChain instance for generating the final answer
                llm_chain = LLMChain(prompt=prompt_final, llm=llm)
                final_answer = llm_chain.run(
                    conversation_history = conversation_history,
                    selected_repo_list = selected_repo_list
                )

                # Display the final result
                final_col.markdown('### Final Result')
                final_col.markdown(final_answer, unsafe_allow_html = True)

        except Exception as e:
            # In case of any exceptions, display them to the user
            st.write(e)


# Function for displaying the homepage
def homepage():
    # Display the logo image
    home_image = st.image(logo_image)

    _, c2, _ = st.columns([2,1,2])
    c2.markdown('') 
    c2.markdown('')
    # Button to go to the main application
    continue_forward = c2.button('Get In >>>', use_container_width=True)

    # Update the session state to indicate that the homepage has been displayed
    st.session_state['home_page'] = False

    # Go to the main application if the 'Get In' button was clicked
    if continue_forward:
        print('going to the application!!')
        home_image.empty()
        main()
