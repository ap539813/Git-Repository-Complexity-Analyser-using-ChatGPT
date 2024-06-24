# Git Repository Complexity Analyser using ChatGPT

## Overview
The Git Repository Complexity Analyser is a tool that leverages ChatGPT to evaluate the complexity of code repositories on GitHub. The application helps in summarizing the overall logic, analyzing code complexity, and ranking repositories based on their technical challenges.

## Features
- **Repository Analysis:** Extracts and summarizes the overall logic of code repositories.
- **Complexity Assessment:** Analyzes space and time complexity of code.
- **Comparative Analysis:** Identifies and ranks repositories based on technical complexity.
- **User Interaction:** Provides a web interface for user inputs and results visualization.

## Getting Started

### Prerequisites
- Python 3.x
- Streamlit
- Git
- OpenAI API Key

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/ap539813/Git-Repository-Complexity-Analyser-using-ChatGPT
    cd Git-Repository-Complexity-Analyser-using-ChatGPT
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the OpenAI API key:
    ```sh
    export GIT_API=your_github_api_key
    ```

### Configuration
1. Update `secrets.json` with your GitHub credentials and other important variables:
    ```json
    {
        "git_api": "https://api.github.com/users/username/repos",
        "model_name": "gpt-3.5-turbo-16k",
        "style_css": "style.css",
        "logo_image": "git_bot_theme.png",
        "icon_logo": "app_logo.png"
    }
    ```

## File Structure
- **add_style.py:** Contains functions to apply custom CSS to the Streamlit app.
- **app.py:** Main entry point of the Streamlit application.
- **application_pages.py:** Handles the main logic for user interactions and displays.
- **important_variables.py:** Defines important constants and variables used across the application.
- **requirements.txt:** List of Python dependencies needed to run the scripts.
- **utils.py:** Contains utility functions for processing GitHub repositories.

## Running the Application
1. To start the application, run:
    ```sh
    streamlit run app.py
    ```
   The application will be available at `http://localhost:8501`.

## Usage
### Repository Analysis
1. **Input GitHub User ID:** Enter the GitHub username to fetch repositories.
2. **Select Repositories:** Choose repositories from the fetched list.
3. **Analyze:** Click the 'Analyze' button to start the complexity analysis.
4. **View Results:** The application will display a summary and complexity ranking of the selected repositories.

## Dependencies
- altair
- streamlit
- openai
- langchain

Check `requirements.txt` for the full list of dependencies.

## Contributing
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/fooBar`).
3. Commit your changes (`git commit -am 'Add some fooBar'`).
4. Push to the branch (`git push origin feature/fooBar`).
5. Create a new Pull Request.
