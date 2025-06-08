from mistralai import Mistral
import os

api_key = os.getenv("MISTRAL_KEY")
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

def mistral_summarize(text):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": """Please summarize the submitted text. The text may come from several different sources covering the same
                story; please synthesize across the sources as best you can. Make your response as long as needed for an adequate
                level of detail, about the length of a typical article. Format it like an article with a title (markdown), 
                but avoid giant whitespace gaps between paragraphs.""",
            },
            {
                "role": "user",
                "content": text,
            },
        ],
    )
    return chat_response.choices[0].message.content