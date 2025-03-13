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
        url = f"https://jisho.org/api/v1/search/words?keyword={word}"
        response = requests.get(url)
        
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
                        if 'parts_of_speech' in sense:
                            pos = f"[{', '.join(sense['parts_of_speech'])}] " if sense['parts_of_speech'] else ""
                        else:
                            pos = ""
                        defs = ', '.join(sense['english_definitions'])
                        japanese_defs.append(f"{pos}{defs}")
                        if len(japanese_defs) >= 2:  # 最大2つの意味まで
                            break
                    result['japanese'] = '\n'.join(japanese_defs)
                
                return result
            return {"error": "意味が見つかりませんでした。"}
        return {"error": f"Error: {response.status_code} - {response.text}"}
    except (KeyError, IndexError):
        return {"error": "解析エラー：データ構造が異なります"}
    except Exception as e:
        return {"error": f"予期せぬエラー: {str(e)}"}

# GUI設定
root = tk.Tk()
root.title('CursorLex')
root.geometry('400x500')

button = tk.Button(root, text='クリップボードから取得', command=get_text_from_clipboard)
button.pack(pady=20)

result_label = tk.Label(root, text='ここに結果が表示されます', wraplength=350, justify='left')
result_label.pack(pady=10, padx=20)

root.mainloop()

