from flask import Flask, request, render_template, Blueprint, jsonify
from pathlib import Path

app4 = Blueprint('get_json_list', __name__, template_folder='templates')

@app4.route('/get_json_list', methods=['POST'])
def get_json_list():
    # クエリパラメーターがある場合、skip
    #print(request.args.get('template'))
    if request.args.get('template') is not None:
        data = {}
        return render_template("home.html", data=data)
    filepath = Path("static/template_json")

    files = [f.name for f in filepath.iterdir() if f.is_file() and "テンプレート" in f.name] +  [f.name for f in filepath.iterdir() if f.is_file() and "テンプレート" not in f.name]
    data = [file.replace(".json", "") for file in files]

    return jsonify({"message": "JSON received", "data": data})  # レスポンスを返す

if __name__ == '__main__':
    app4.run(debug=True)