import tkinter as tk
import pyperclip
import requests

def get_text_from_clipboard():
    try:
        text = pyperclip.paste().strip()
        print(f"Received text: {text}")
        result = get_word_meaning(text)
        print(f"Result: {result}")
        
        if "error" in result:
            display_text = result["error"]
        else:
            display_text = f"【英語の意味】\n{result['english']}\n\n"
            display_text += f"【読み方】\n{result['reading']}\n\n"
            display_text += f"【詳細な意味】\n{result['japanese']}"
        
        result_label.config(text=display_text)
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

def get_word_meaning(word):
    try:
        url = "https://jisho.org/api/v1/search/words"
        # use params so the query is properly encoded
        response = requests.get(url, params={"keyword": word}, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                word_data = data['data'][0]
                result = {}
                
                # 英語の意味を取得
                if word_data.get('senses'):
                    english_defs = word_data['senses'][0].get('english_definitions', [])
                    result['english'] = english_defs[0] if english_defs else "No English definition found"
                
                # 読み方を取得
                if word_data.get('japanese'):
                    reading = word_data['japanese'][0].get('reading', '')
                    result['reading'] = reading if reading else word_data['japanese'][0].get('word', '')
                
                # 日本語の意味を取得
                if word_data.get('senses'):
                    japanese_defs = []
                    for sense in word_data['senses']:
                        # 品詞情報の取得
                        if 'parts_of_speech' in sense:
                            pos = f"[{', '.join(sense['parts_of_speech'])}] " if sense['parts_of_speech'] else ""
                        else:
                            pos = ""
                        
                        # 英語の意味
                        eng_defs = ', '.join(sense['english_definitions'])
                        
                        # 日本語の意味（日本語訳の辞書）
                        jp_translations = {
                            'noun': '名詞',
                            'verb': '動詞',
                            'adjective': '形容詞',
                            'adverb': '副詞',
                            'particle': '助詞',
                            'interjection': '感嘆詞',
                            'pronoun': '代名詞',
                            'conjunction': '接続詞',
                            'counter': '助数詞',
                            'suffix': '接尾辞',
                            'prefix': '接頭辞',
                            'expression': '表現',
                            'na-adjective': 'な形容詞',
                            'i-adjective': 'い形容詞',
                            'suru verb': 'する動詞',
                            'auxiliary': '助動詞',
                            'proper noun': '固有名詞',
                        }
                        
                        # 品詞の日本語表示
                        jp_pos = pos
                        for eng, jp in jp_translations.items():
                            jp_pos = jp_pos.replace(eng, jp)
                        
                        # 意味の追加（英語と日本語）
                        entry = f"{jp_pos}{eng_defs}"
                        
                        # 日本語の意味を追加
                        if 'japanese_definitions' in sense:
                            jp_meaning = ', '.join(sense['japanese_definitions'])
                            entry += f"\n→ {jp_meaning}"
                        elif 'japanese_definitions' not in sense and 'english_definitions' in sense:
                            # 一般的な日本語訳を提供
                            translations = {
                                'to ': 'する、',  # 動詞の基本形
                                'the ': '',      # 冠詞は省略
                                'a ': '',        # 冠詞は省略
                                'an ': '',       # 冠詞は省略
                            }
                            jp_meaning = eng_defs.lower()
                            for eng, jp in translations.items():
                                jp_meaning = jp_meaning.replace(eng, jp)
                            entry += f"\n→ {jp_meaning}"
                        
                        japanese_defs.append(entry)
                        if len(japanese_defs) >= 2:  # 最大2つの意味まで
                            break
                    result['japanese'] = '\n\n'.join(japanese_defs)
                
                return result
            return {"error": "意味が見つかりませんでした。"}
        return {"error": f"Error: {response.status_code} - {response.text}"}
    except (KeyError, IndexError):
        return {"error": "解析エラー：データ構造が異なります"}
    except Exception as e:
        return {"error": f"予期せぬエラー: {str(e)}"}

if __name__ == "__main__":
    # GUI設定
    root = tk.Tk()
    root.title('CursorLex')
    root.geometry('400x500')

    button = tk.Button(root, text='クリップボードから取得', command=get_text_from_clipboard)
    button.pack(pady=20)

    result_label = tk.Label(root, text='ここに結果が表示されます', wraplength=350, justify='left')
    result_label.pack(pady=10, padx=20)

    root.mainloop()
