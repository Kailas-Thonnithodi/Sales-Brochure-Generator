import os
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display, update_display
from scraper import fetch_website_contents, fetch_website_links