# Prompts
link_system = '''
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

brochure_system_prompt = '''
You are an assistant that analyses the contents of several relevant pages from a company website and creates a short brochure about the company
for prospective customers, investors and recruits. Respond in markdown without code blocks.
Include details of company culture, customer and careers/jobs if you have the information.
'''

def get_brochure_user_prompt(company_name, url, page_contents, truncated_limit=5_000):
    user_prompt = f'''
    You are looking at a company called: {company_name} ({url}).
    Here are the contents of its landing page and other relevant pages;
    use this information to build a short brochure of the company in markdown without code blocks.

    '''
    user_prompt += page_contents
    return user_prompt[:truncated_limit]

def user(url):
    user_prompt = f'''
    Here is the list of links on the website {url} - 
    Please decide which of these are relevant web links for a brochure about the company,
    respond with the full https URL in JSON format.
    Do not include Terms of Service, Privacy, email links.
    '''
    return user_prompt
