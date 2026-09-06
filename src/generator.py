from dotenv import load_dotenv
from scraper import fetch_website_contents, fetch_website_links
from model_config import Gemini, Open
import json

# Prompts
link_system_prompt = '''
You are provided with a list of links on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://fullurl/goes/here/"},
        {"type": "careers page", "url": "https://another.full.url/goes/here/"}
    ]
}
'''

# Functions
def get_links_user_prompt(url):
    user_prompt = f'''
    Here is the list of links on the website {url} - 
    Please decide which of these are relevant web links for a brochure about the company,
    respond with the full https URL in JSON format.
    Do not include Terms of Service, Privacy, email links.
    '''
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt

def select_relevant_links(url, model_class: Gemini|Open, system_prompt=link_system_prompt):
    response = model_class.wrapper.chat.completions.create(
        model=model_class.model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_links_user_prompt(url)}
        ],
        response_format={"type": "json_object"},
    )
    result = response.choices[0].message.content
    return json.loads(result)

if __name__ == "__main__":

    load_dotenv(override=True)

    # Models
    gemini_default_config = Gemini()
    openai_default_config = Open()

    print(select_relevant_links('https://anthropic.com', openai_default_config))