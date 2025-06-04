from src.summarizer import get_daily_summary

def main():
    summary = get_daily_summary()
    print("📰 Your one thing today:\n")
    print(summary)

if __name__ == "__main__":
    main()