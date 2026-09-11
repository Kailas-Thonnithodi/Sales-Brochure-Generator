from dotenv import load_dotenv
from scraper import fetch_website_contents, fetch_website_links
from model_config import Gemini, Open
from IPython.display import display, update_display ,Markdown
from prompts import user, link_system, get_brochure_user_prompt, brochure_system_prompt
import json

# Functions
def get_links_user_prompt(url):
    '''
    Fetch all links which are based on the singular url presented.
    '''
    user_prompt = user(url)
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt

def select_relevant_links(url, model_class: Gemini | Open, system_prompt=link_system):
    '''
    After getting the urls, have an LLM filter out relevant links only. This will prune links which
    may seem unecessary based on the LLM's judgement. 
    '''
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

def fetch_page_and_all_relevant_links(url, model_class: Gemini | Open):
    '''
    After filtering out the links, extract all the content from the page. Ask the LLM to process and return the more relevant information
    from the filtered links. 
    '''
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_links(url, model_class)
    # the model is asked for "links", but be tolerant of casing drift
    links = relevant_links.get("links") or relevant_links.get("Links") or []
    result = f"## Landing Page\n\n{contents}\n\n## Relevant Links:\n"
    for link in links:
        result += f"\n\n### Link: {link['url']}\n"
        result += fetch_website_contents(link["url"])
    return result

def create_brochure(company_name, url, page_contents, model_class: Gemini | Open, streamed=True):
    '''
    Creates the markdown file which produces brochure for the company. As the LLM (after link extraction and information extrapolation),
    to generate a markdown formatted brochure based on the provided content. 
    '''
    response = model_class.wrapper.chat.completions.create(
        model=model_class.model_name,
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url, page_contents)}
        ],
        stream=streamed
    )

    if streamed == False:
        result = response.choices[0].message.content
        return result
    else:
        streamed_response = ''
        display_handle = display(Markdown(""),display_id=True)
        for chunk in response:
            streamed_response += chunk.choices[0].delta.content or ''
            update_display(Markdown(streamed_response), display_id=display_handle.display_id)

if __name__ == "__main__":

    load_dotenv(override=True)

    company = 'IntelliFlow'
    url = 'https://www.intelliflow.com.au/'

    # Models
    gemini_default_config = Gemini()
    openai_default_config = Open()

    page_contents = fetch_page_and_all_relevant_links(url, openai_default_config)
    brochure = create_brochure(company, url, page_contents, openai_default_config, streamed=False)