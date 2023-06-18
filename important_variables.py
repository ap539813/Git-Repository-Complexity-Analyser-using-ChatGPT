import base64


git_api = "https://api.github.com/users/username/repos"

model_name = "gpt-3.5-turbo"


theme_image_name = 'git_bot_theme.png'
logo_image = 'git_bot_theme.png'

"""### gif from local file"""
file_ = open(theme_image_name, "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()


