from mistralai import Mistral

api_key = "vNb4NbpiEo7HEB4tOSVWI84hy7j63voW"
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
                level of detail, about the length of a typical article, and format it like an article with a title.""",
            },
            {
                "role": "user",
                "content": text,
            },
        ],
    )
    return chat_response.choices[0].message.content