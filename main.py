# run_all.py
import os
from researcher.searcher import search
from researcher.fetcher import fetch_many
from synthesizer.synthesize import synthesize

def main():
    queries = [
        "RICE scoring model prioritization explanation",
        "Kano model prioritization explanation",
        "Differences between RICE and Kano models"
    ]
    # 1) Search
    all_urls = []
    for q in queries:
        urls = search(q, max_results=6)
        # basic filtering to prefer domain names and docs
        for u in urls:
            if u not in all_urls:
                all_urls.append(u)
        if len(all_urls) >= 12:
            break
    # choose top 6 candidate urls to fetch
    candidate_urls = all_urls[:8]
    print("Candidate URLs:", candidate_urls)

    # 2) Fetch
    fetched = fetch_many(candidate_urls, pause=1.2)
    if not fetched:
        raise RuntimeError("No articles fetched; check network/robots")

    # 3) Synthesize
    final = synthesize(fetched)

    # 4) Write final_answer.txt and also a JSON with sources
    with open("final_answer.txt", "w", encoding="utf-8") as f:
        f.write(final)

    print("Done: final_answer.txt created")

if __name__ == "__main__":
    main()
