from flask import Flask, request, render_template, Blueprint, jsonify
import json
import os
import pyautogui
import time
import threading
import pygetwindow
from multiprocessing import Process, Queue

app3 = Blueprint('save_json', __name__, template_folder='templates')

def show_dialog_and_save(data, queue):
    import tkinter
    from tkinter import simpledialog, messagebox
    # Tkinter GUI処理とファイル保存処理をここにまとめる

    filepath = "static/template_json"

    #テキストダイアログを表示
    root = tkinter.Tk()
    root.withdraw()  # メインウィンドウを非表示にする

    class CustomDialog(simpledialog.Dialog):
        def body(self, master):
            self.geometry("400x100")  # ← サイズ指定（幅x高さ）
            self.entry = tkinter.Entry(master, width=50)
            self.entry.grid(row=0, column=0, sticky="w")

            # 薄い固定テキスト（末尾に表示）
            self.hint = tkinter.Label(master, text=" .json", fg="gray", font=("Arial", 10))
            self.hint.grid(row=0, column=1, sticky="w")

            return self.entry  # 初期フォーカス

        def apply(self):
            self.result = self.entry.get()

    def push_key():
        time.sleep(1.5)
        window = pygetwindow.getActiveWindow()
        print(window.title)
        if window.title != "テンプレート名の入力":
            pyautogui.hotkey('alt', 'shift', 'tab')


    #キー入力処理を別スレッドで開始
    threading.Thread(target=push_key, daemon=True).start()
    
    dialog = CustomDialog(root, title="テンプレート名の入力")

    if dialog.result:
        print("入力されたテキスト:", dialog.result)
        filename = f"{filepath}/{dialog.result}.json"
        if os.path.exists(filename):
            confirm = messagebox.askyesno(
                title="確認",
                message=f"'{filename}' は既に存在します。\n上書きしますか？"
            )
            if not confirm:
                print("上書き取消")
                queue.put({"message": "Save canceled", "data": {}})  # レスポンスを返す
                return
        try:           
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"JSONファイル '{filepath}/{dialog.result}.json' を作成しました。")
            queue.put({"message": "json saved", "data": data})  # レスポンスを返す
        except Exception as e:
            print(f"JSONファイルの作成に失敗しました: {e}")
            queue.put({"message": "Save eliminated", "data": {e}})  # レスポンスを返す
    else:
        data = {}
        queue.put({"message": "Save canceled", "data": {}})  # レスポンスを返す
    root.destroy()

@app3.route('/save_json', methods=['POST'])
def save_json():
    data = request.get_json()  # JSONデータを取得

    # クエリパラメーターがある場合、skip
    print(request.args.get('template'))
    if request.args.get('template') is not None:
        return render_template("home.html", data=data)
    
    queue = Queue()
    p = Process(target=show_dialog_and_save, args=(data,queue))
    p.start()
    p.join()

    result = queue.get()
    print(result)
    return jsonify(result)  # レスポンスを返す

if __name__ == '__main__':
    app3.run(debug=True)