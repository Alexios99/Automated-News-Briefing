def human_screen_articles(all_articles):
    accepted = []
    print("\nBegin human screening:\n")

    for i, article in enumerate(all_articles):
        title = article.get("title", "No title")
        desc = article.get("description", "No description")
        url = article.get("url")

        print(f"\n[{i+1}/{len(all_articles)}]")
        print(f"Title: {title}")
        print(f"Description: {desc}")
        print(f"URL: {url}")

        choice = input("Accept this article? (y/n/exit): ").strip().lower()

        if choice == 'y':
            accepted.append(article)
        elif choice == 'exit':
            break
        else:
            print("Skipped.")

    return accepted
