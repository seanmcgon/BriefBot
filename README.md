# BriefBot 📰🤖

**Get a daily synthesized summary of top news across sources.**

BriefBot is a Python-based automation tool that pulls the day’s top headlines, categorizes them into major news topics (tech, politics, business, health, science, world), identifies clusters of articles covering the same story, and then synthesizes them into a coherent, long-form summary. Finally, it delivers these summaries directly to your inbox in a clean, styled HTML email.

It’s built for people who want to stay informed without drowning in dozens of articles. By pulling from multiple sources and distilling the essential information into readable summaries, BriefBot gives you a clear, unbiased snapshot of the day’s most important stories.

---

## ✨ Features

- 📡 Pulls from a wide set of **RSS feeds** across general and tech news  
- 🧠 Uses **zero-shot classification** to assign major news categories  
- 🔍 **Clusters articles** covering the same story for deeper understanding  
- 📝 Synthesizes **long-form summaries** using the **Mistral API**  
- 📬 Sends you a personalized, styled **daily email digest**  
- ⚙️ Fully automated via **GitHub Actions**

---

## 🛠 Tech Stack

- Python  
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)  
- [Mistral AI](https://mistral.ai/)  
- [Feedparser](https://pypi.org/project/feedparser/) (RSS parsing)  
- [Trafilatura](https://pypi.org/project/trafilatura/) (article text extraction)  
- Gmail SMTP (for email delivery)  
- GitHub Actions (for daily automation)

---

## 🚀 Getting Started

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/yourusername/briefbot.git
cd briefbot
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Set up your environment variables
Create a `.env` file in the root directory with the following secrets (or use GitHub repository secrets):

```ini
MISTRAL_KEY=your_mistral_api_key
EMAIL_PASSWORD=your_email_smtp_password
EMAIL=youremail@gmail.com
SENDER=BriefBot <youremail@gmail.com>
RECIPIENT=youremail@gmail.com
```

### 3. Run once manually

```bash
python main.py
```
Or let it run automatically every day using GitHub Actions (see `.github/workflows/daily.yml`).

---

## 📌 Notes & Limitations

- ⚠️ Mistral API limits (if using the free tier) may restrict how many summaries you can generate per day
- 📰 Article quality and coverage depends on the RSS feeds you choose
- 🤖 Clustering and classification use zero-shot models, which may not always be perfect
- 🔧 Currently optimized for general + tech news — easily tweakable for your own interests
- The process can be slow to run (~20 minutes), especially due to the zero-shot classification and clustering steps, which may impact performance and responsiveness
- During development and testing, you can speed up iterations by enabling JSON caching of intermediate results. To do this, set `USE_CACHE = True` in `main.py`.

---

## 🧠 Why It’s Useful

- 💤 No more doomscrolling — just one clean daily email with all the context you need
- 🗞️ Synthesized from multiple sources to reduce bias
- 📚 Prioritizes depth over brevity, for people who actually want to understand the news
- 🧩 Fully open-source and customizable

---

## 📄 License

MIT  
