import requests
import re

# MLB公式APIからデータを取得する関数（簡略版）
def get_stats(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}?hydrate=stats(group=[hitting,pitching],type=[season])"
    res = requests.get(url).json()
    player = res['people'][0]
    stats_list = player.get('stats', [])
    
    result = {"name": player['fullName'], "hitting": "---", "pitching": "---"}
    for s in stats_list:
        if s['group']['displayName'] == 'hitting':
            h = s['splits'][0]['stat']
            result['hitting'] = f"{h['avg']} / {h['homeRuns']} HR / {h['rbi']} RBI"
        if s['group']['displayName'] == 'pitching':
            p = s['splits'][0]['stat']
            result['pitching'] = f"{p['wins']}-{p['losses']} / {p['era']} ERA / {p['strikeOuts']} SO"
    return result

# 選手ID (大谷, タッカー, パヘス)
players = [get_stats(660271), get_stats(663656), get_stats(681624)]

# READMEを読み込んで書き換える
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

new_table = "### ⚾️ MLB My Focus Players (Auto-Updated)\n"
for p in players:
    new_table += f"#### {p['name']}\n- **Hitting**: {p['hitting']}\n"
    if p['pitching'] != "---":
        new_table += f"- **Pitching**: {p['pitching']}\n"

# README内の特定のエリア（もしあれば）を置換するか、最後に追加する
# 今回はシンプルに、特定の目印の間を書き換える方式にします
marker_start = "### ⚾️ MLB"
marker_end = "---"
pattern = f"{marker_start}.*?{marker_end}"
updated_content = re.sub(pattern, f"{new_table}\n{marker_end}", content, flags=re.DOTALL)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated_content)
