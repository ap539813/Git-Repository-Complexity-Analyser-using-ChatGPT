import streamlit as st
from important_variables import logo_image


from utils import get_github_repos, clone_and_preprocess
from important_variables import git_api


def main():
    username = st.text_input("Input Git Use Id:")
    result = get_github_repos(username, git_api)
    try:
        repo_links = [git_repo['html_url'] for git_repo in result]
        # st.write(repo_links)
        selected_url = st.selectbox("Select the git repo: ", options = repo_links)
        preprocessed_files = clone_and_preprocess(selected_url)
        st.write(preprocessed_files)
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


