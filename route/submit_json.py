from flask import Flask, request, render_template, Blueprint, jsonify
from tkinter import filedialog
import tkinter
import json

app2 = Blueprint('submit_json', __name__, template_folder='templates')

@app2.route('/submit_json', methods=['POST', 'GET'])
def submit_json():

    print(request.args.get('template'))
    if request.args.get('template') is not None:
        data = {}
        return render_template("home.html", data=data)
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
        return jsonify({"status": "cancel", "data": {}})  # レスポンスを返す

    print("Received JSON:", data)  # コンソールに出力

    #return render_template("home.html", data=data)
    return jsonify({"status": "ok", "data": data})  # レスポンスを返す

if __name__ == '__main__':
    app2.run(debug=True)