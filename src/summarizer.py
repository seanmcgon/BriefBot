from mistralai import Mistral, SDKError
import os, time
from datetime import date

api_key = os.getenv("MISTRAL_KEY")
# model = "mistral-large-latest"
client = Mistral(api_key=api_key)
models = ["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest"]

def mistral_summarize(text):
    for model in models:
        for i in range(10):
            try:
                chat_response = client.chat.complete(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": f"""Please summarize the submitted text. The text may come from several different sources covering the same
                            story; please synthesize across the sources as best you can. Make your response as long as needed for an adequate
                            level of detail, about the length of a typical article. Format it (using markdown) like an article with a title. Do not, 
                            under any circumstances, apply your own knowledge to the summaries, as it is often outdated - today's date is 
                            {date.today()}. Your output should be based exclusively on the articles' text. I repeat: DO NOT use any outside 
                            information, ever; pure summaries only.""",
                        },
                        {
                            "role": "user",
                            "content": text,
                        },
                    ],
                )
                print("Summarized using " + model)
                return chat_response.choices[0].message.content
            except SDKError as e:
                if (
                    "capacity exceeded" in str(e).lower()
                    or "status 429" in str(e).lower()
                ):
                    wait = 2**i  # exponential backoff: 1s, 2s, 4s, etc.
                    print(f"Mistral busy, retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise
    raise RuntimeError("Mistral is still unavailable after multiple retries.")
