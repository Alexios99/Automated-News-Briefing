import google.generativeai as genai
from typing import Dict, Tuple


def configure_model(api_key: str):
    """Configures Gemini API and returns the model + chat session."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        chat = model.start_chat()
        return model, chat
    except Exception as e:
        raise RuntimeError(f"Failed to configure Gemini model: {e}")


def generate_summary(model, article_text: str) -> str:
    """
    Sends a prompt to Gemini to summarise a sustainable finance news article.
    Returns raw string (with bullet summary, Topic, Mentioned Companies).
    """
    prompt = (
        "Act as a financial analyst. Summarise the following news article in three key bullet points, "
        "focusing on its importance to institutional investors in the sustainable finance sector.\n\n"
        "After the summary, add a 'Topic:' line and categorize the article into one of the following: "
        "'Regulatory & Policy', 'Corporate Action', 'Market Trends', 'New Technology', or 'General News'.\n"
        "At the very end, add a 'Mentioned Companies:' line and list any public companies mentioned in the article. Double check this, companies will most likely be mentioned "
        "If none, write 'None only for mentioned comapnies, make sure there is a topic'.\n"
        "Also in terms of formating do not have an introduction like 'here is the summary' just start with bullet points"
        f"{article_text}"
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response.parts else "[Error: Empty response from Gemini]"
    except Exception as e:
        return f"[Error generating summary: {str(e)}]"


def generate_intro(model, summaries, topics=None, sentiment_stats=None):
    """
    Generate an introductory paragraph for the SAFL weekly briefing using Gemini.
    Do not mention sentiment in the intro, regardless of arguments passed.
    """
    system_prompt = (
        "You are a financial analyst writing for a weekly institutional newsletter focused on sustainable finance. "
        "Your job is to write the introductory paragraph for this week's 5-article summary briefing. "
        "Keep the tone professional and concise, written for an audience of institutional investors. "
        "Highlight any emerging trends, policy changes, or corporate developments, and include a brief forward-looking insight. "
        "You are writing on behalf of a specialist in green and blue economy capital raising. "
        "Do not have any intro or outro like 'here is the intro' just start with the intro."
    )

    joined_summaries = "\n- " + "\n- ".join(summaries)

    prompt = (
        f"Here are the summaries of this week's top 5 articles:\n{joined_summaries}\n\n"
        "Write a one-paragraph introduction for a professional briefing. "
        "Do not have any intro or outro like 'here is the intro' just start with the overall summary"
    )

    response = model.generate_content([system_prompt, prompt])
    return response.text.strip()
