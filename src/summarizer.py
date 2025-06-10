from mistralai import Mistral, SDKError
import os, time

api_key = os.getenv("MISTRAL_KEY")
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

def mistral_summarize(text):
    for i in range(5):
        try:
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
        except SDKError as e:
            if "capacity exceeded" in str(e).lower() or "status 429" in str(e).lower():
                wait = 2 ** i  # exponential backoff: 1s, 2s, 4s, etc.
                print(f"Mistral busy, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Mistral is still unavailable after multiple retries.")