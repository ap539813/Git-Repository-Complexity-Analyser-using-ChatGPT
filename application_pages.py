import streamlit as st
from important_variables import logo_image
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain


from utils import get_github_repos, clone_and_preprocess
from important_variables import git_api


def main():
    username = st.text_input("Input Git Use Id:")
    if username != '':
        result = get_github_repos(username, git_api)
        try:
            repo_links = [git_repo['html_url'] for git_repo in result]
            # st.write(repo_links)
            repo_names = [repo_link.split('/')[-1] for repo_link in repo_links]
            repo_to_link = {repo_names[i]:repo_links[i] for i in range(len(repo_names))}
            # st.write(repo_links)
            selected_urls = st.multiselect("Select the git repositories: ", options = repo_names, default = repo_names[:1])
            analyse_button = st.button('Analyse')
            if analyse_button:
                conversation_history = ""
                for selected_url_val in selected_urls:
                    selected_url = repo_to_link[selected_url_val]
                    git_repo = selected_url.split('/')[-1]
                    preprocessed_files = clone_and_preprocess(selected_url)
                    # st.write(preprocessed_files)
                    llm = st.session_state['GPT']

                    template_for_code = """
                    Code Files: {filenames} | Repository Name: {git_repository_name}

                    Instr:
                    1. Summarise the overall logic of the code.
                    2. Focus on code.
                    3. Consider:
                        a. Time complexity.
                        b. Space complexity.

                    Answer:
                    """

                    prompt_repo = PromptTemplate(
                        template = template_for_code,
                        input_variables=["filenames", "git_repository_name"]
                    )

                    llm_chain = LLMChain(prompt=prompt_repo, llm=llm)
                    answer_repo = llm_chain.run(
                        # model = model_name,
                        # context = 'We need to analyse the complexisy of the code in the mentioned repository',
                        git_repository_name = git_repo,
                        conversation_history = conversation_history,
                        filenames = preprocessed_files,
                    )
                    # st.write(git_repo)
                    # st.write(answer_repo)

                    conversation_history += f'REPOSITORY NAME:\n{username}/{git_repo}\n\nSUMMARY:\n{answer_repo}'
                    # st.write(f'REPOSITORY NAME:\n{git_repo}\n{conversation_history}')
                    st.markdown(f'### REPOSITORY NAME: {username}/{git_repo}')
                    st.write(f'SUMMARY:\n{answer_repo}')


                template_for_final = """
                Conversation history: {conversation_history} | 

                Question:
                Which code repository among {selected_urls} has the most technically complex and challenging.

                Instructions:
                Refer to the Conversation history. Give answer in two sections with following headings:
                    1. Most Complex code Repository: 
                    2. A proper explanation on why do you think so
                """

                prompt_final = PromptTemplate(
                    template = template_for_final,
                    input_variables=["conversation_history", "selected_urls"]
                )
                llm_chain = LLMChain(prompt=prompt_final, llm=llm)
                final_answer = llm_chain.run(
                    conversation_history = conversation_history,
                    selected_urls = selected_urls
                )

                st.markdown('### Final Result')
                st.markdown(final_answer)
            

        except Exception as e:
            st.write(e)


def homepage():
    home_image = st.image(logo_image)

    c1, c2, c3 = st.columns([2,1,2])
    c2.markdown('') 
    c2.markdown('')
    continue_forward = c2.button('Get In >>>')

    st.session_state['home_page'] = False
    

    if continue_forward:
        print('going to the application!!')
        home_image.empty()
        main()


