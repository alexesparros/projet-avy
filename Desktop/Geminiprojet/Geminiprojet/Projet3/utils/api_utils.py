import google.generativeai as genai
import requests

def configure_gemini(api_key):
    genai.configure(api_key=api_key)

def generate_gemini_content(prompt, model_name='models/gemini-1.5-flash-latest', stream=False):
    model = genai.GenerativeModel(model_name)
    if stream:
        return model.generate_content(prompt, stream=True)
    else:
        return model.generate_content(prompt)

def get_rawg_games(api_key, start_date, end_date, page_size=7):
    url = (
        f"https://api.rawg.io/api/games?dates={start_date},{end_date}&ordering=-released&page_size={page_size}&key={api_key}"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    return resp.json().get("results", []) 