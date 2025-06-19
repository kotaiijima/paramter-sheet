from flask import Flask, request, render_template, Blueprint, jsonify
from tkinter import filedialog
import tkinter
import json

app2 = Blueprint('submit_json', __name__, template_folder='templates')

@app2.route('/submit_json', methods=['GET'])
def submit_json():
    # ファイル保存ダイアログを表示（ファイル名も指定可能）
    root = tkinter.Tk()
    # topmost指定(最前面)
    root.attributes('-topmost', True)
    root.withdraw()
    root.lift()
    filepath = filedialog.askopenfilename(
        parent=root,
        filetypes=[("データファイル", "*.json")],
        title="アップロードするファイルを指定"
    )
    root.focus_force()

    if filepath:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        return render_template("home.html", data={}, message="アップロードをキャンセルしました。")
    
    print("Received JSON:", data)  # コンソールに出力

    return render_template("home.html", data=data)

if __name__ == '__main__':
    app2.run(debug=True)