import requests
import re

# MLB公式APIから詳細なデータを取得する関数
def get_stats(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}?hydrate=stats(group=[hitting,pitching],type=[season])"
    res = requests.get(url).json()
    player = res['people'][0]
    stats_list = player.get('stats', [])
    
    # 初期値の設定
    result = {
        "name": player['fullName'],
        "avg": ".000", "hr": "0", "rbi": "0", "sb": "0", "ops": ".000",
        "w": "0", "l": "0", "era": "0.00", "so": "0", "whip": "0.00",
        "has_pitching": False
    }
    
    for s in stats_list:
        if s['group']['displayName'] == 'hitting':
            h = s['splits'][0]['stat']
            result.update({
                "avg": h.get('avg', '.000'),
                "hr": h.get('homeRuns', 0),
                "rbi": h.get('rbi', 0),
                "sb": h.get('stolenBases', 0),
                "ops": h.get('ops', '.000')
            })
        if s['group']['displayName'] == 'pitching':
            p = s['splits'][0]['stat']
            result.update({
                "w": p.get('wins', 0),
                "l": p.get('losses', 0),
                "era": p.get('era', '0.00'),
                "so": p.get('strikeOuts', 0),
                "whip": p.get('whip', '0.00'),
                "has_pitching": True
            })
    return result

# 選手情報を取得
ohtani = get_stats(660271)
tucker = get_stats(663656)
pages = get_stats(681624)

# --- 表の組み立て ---
new_table = "### ⚾️ MLB My Focus Players (Auto-Updated)\n"

# 大谷選手 (二刀流テーブル)
new_table += f"#### 🦄 {ohtani['name']} (LAD #17)\n"
new_table += "| Role | Stats |\n| :--- | :--- |\n"
new_table += f"| **Hitting** | {ohtani['avg']} AVG / {ohtani['hr']} HR / {ohtani['rbi']} RBI / {ohtani['sb']} SB |\n"
new_table += f"| **Pitching** | {ohtani['w']}-{ohtani['l']} W-L / {ohtani['era']} ERA / {ohtani['so']} SO / {ohtani['whip']} WHIP |\n\n"

# カイル・タッカー (5列テーブル)
new_table += f"#### 🏹 {tucker['name']} (LAD #23)\n"
new_table += "| AVG | HR | RBI | SB | OPS |\n| :--- | :--- | :--- | :--- | :--- |\n"
new_table += f"| {tucker['avg']} | {tucker['hr']} | {tucker['rbi']} | {tucker['sb']} | {tucker['ops']} |\n\n"

# アンディ・パヘス (5列テーブル)
new_table += f"#### 🚀 {pages['name']} (LAD #44)\n"
new_table += "| AVG | HR | RBI | SB | OPS |\n| :--- | :--- | :--- | :--- | :--- |\n"
new_table += f"| {pages['avg']} | {pages['hr']} | {pages['rbi']} | {pages['sb']} | {pages['ops']} |\n\n"

# READMEを読み込んで置換
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"### ⚾️ MLB.*?\n---"
updated_content = re.sub(pattern, f"{new_table}---", content, flags=re.DOTALL)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated_content)
