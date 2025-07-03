    window.onload = function() {

        if (Object.keys(json_data).length) {
            uploadJson();
        } else {
            const params = new URLSearchParams(window.location.search);
            const template = params.get("template");
            console.log(template);
            if (template) {
                document.getElementById('template').value = template;
                fetch(`static/template_json/${template}.json`)
                .then(response => response.json())
                .then(data => {
                    json_data = data;
                    uploadJson();
                });
  }

        }
    }

    function confirmAndSubmit() {
        if (check_item() == true) {
            let result = confirm("この内容で送信しますか？");
            if (result) {
                sendData();
            } else {
                alert("送信をキャンセルしました。");
            }
        }
    }
    
    function uploadJson() {
        let first_frame_check = false;
        const slider_row = new Map;
        for (const frame_key in json_data) {
            if (frame_key == "title") {
                document.getElementById("title").value = json_data[frame_key];
            } else {
                if (first_frame_check == true) addFrame();
                else first_frame_check = true;
                document.getElementById(`item[${frame_num}][0]`).value = frame_key;
                for (const item of json_data[frame_key]) {
                    for (const [key, value] of Object.entries(item)) {
                        if (key != "row") {
                            addItem();
                            console.log(key, value);
                            document.getElementById(`item[${frame_num}][${item_num}]`).value = key;
                            document.getElementById(`value[${frame_num}][${item_num}]`).value = value;
                        } else {slider_row.set(frame_num, Number(value));}
                    }
                }
            }
        }
        for (const [key, value] of slider_row) {
            document.getElementById(`slider_item${key}`).value = value;
        }   
    }

    async function sendData() {
        let frame_name = "";
        let item_name = "";
        // 未入力の場合不具合が起こるため、一意に値を入れる
        let blank_num = 0;

        function blank_count() {
            return blank_num += 1;
        }
        
  const form = document.getElementById("to_json");
  const data = new FormData(form);
console.log(Object.fromEntries(data.entries()));
  // FormDataをJSONに変換
  const jsonData = {};
  for (const [key, value] of data.entries()) {
    if(key.endsWith("[0]")) {
        frame_name = value || `未入力${blank_count()}`;
        jsonData[frame_name] = [];
        const current_frame_num = Number(key.charAt(key.length - 5));
        const slider_cnt = document.getElementById(`slider_item${current_frame_num}`).value;
        console.log(slider_cnt);
        jsonData[frame_name].push({ ["column"]: slider_cnt });
    } else {
        //項目名、値を識別、入力
        if(key.startsWith("item")) {
            item_name = value || `未入力${blank_count()}`;
        } else if(key.startsWith("value")) {
            jsonData[frame_name].push({ [item_name]: value || `未入力${blank_count()}`});
        } else if(key.startsWith("title")) {
            jsonData["title"] = value;
        }
    }
  }
  console.log(jsonData)
  const jsonString = JSON.stringify(jsonData);
  console.log(jsonString)
  // POSTリクエストの送信
  try {
    const response = await fetch('/receive_json', { // FlaskのAPIエンドポイント
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: jsonString
    });
    const result = await response.json(); // レスポンスのJSONを解析
    console.log(result); 
    alert("excelを保存しました。")
  } catch (error) {
    console.error('Error:', error);
  }
}


    function selectedTemplate() {
        // 画面をリロードしつつ、選択されたテンプレート名をURLに渡す
        const selected_template = document.getElementById("template").value;
        location.href = `?template=${selected_template}`;
        }