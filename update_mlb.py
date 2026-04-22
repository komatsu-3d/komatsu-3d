import requests
import re

def get_stats():
    # 大谷選手のデータだけを取りに行きます
    url = "https://statsapi.mlb.com/api/v1/people/660271?hydrate=stats(group=[hitting],type=[season])"
    data = requests.get(url).json()
    s = data['people'][0]['stats'][0]['splits'][0]['stat']
    
    # 2026年最新の大谷さん
    return f"| Player | AVG | HR | RBI | **OPS** |\n| :--- | :--- | :--- | :--- | :--- |\n| **Shohei Ohtani** | {s['avg']} | {s['homeRuns']} | {s['rbi']} | **{s['ops']}** |"

def run():
    stats = get_stats()
    with open("README.md", "r", encoding="utf-8") as f:
        text = f.read()
    
    # の間を書き換え
    new_text = re.sub(r".*?", f"\n{stats}\n", text, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_text)

if __name__ == "__main__":
    run()
