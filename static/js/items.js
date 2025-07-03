    function addItem() {
        item_num += 1;
        
        const item_group = document.getElementById(`form-wrapper${frame_num}`);
        
        const group = document.createElement("div");
        group.className = "form-group";
        group.id = `items[${frame_num}][${item_num}]`;

        const label1 = document.createElement("label");
        label1.textContent = "項目 :";
        label1.htmlFor = `item[${frame_num}][${item_num}]`;
        
        const input1 = document.createElement("input");
        input1.type = "text";
        input1.id = `item[${frame_num}][${item_num}]`;
        input1.name = `items[${frame_num}][${item_num}]`;
         
        const label2 = document.createElement("label");
        label2.textContent = "値 :";
        label2.htmlFor = `value[${frame_num}][${item_num}]`;
        
        const input2 = document.createElement("input");
        input2.type = "text";
        input2.id = `value[${frame_num}][${item_num}]`;
        input2.name = `value[${frame_num}][${item_num}]`;
       
        group.appendChild(label1);
        group.appendChild(input1);
        group.appendChild(label2);
        group.appendChild(input2);
        item_group.appendChild(group);

        const element = document.getElementById(`items[${frame_num}][${item_num}]`);
        element.style.marginLeft = `${style_position}px`;

        for (let i = 0; i <= frame_num; i++) {
            const slider_item = document.getElementById(`slider_item${i}`);
            slider_item.max = Number(slider_item.max) + 1;
            const current_slider = document.getElementById(`sliderGroup${i}`).offsetHeight;
            slider_item.style.height = current_slider + "px";
        };
    }

    function addFrame() {
        item_num = 0;
        style_position += 0;
        const item_bef = document.getElementById(`form-wrapper${frame_num}`);
        frame_num += 1;

        //枠毎にdivを作成、入れ子の仕組み
        const sliderGroup = document.createElement("div");
        sliderGroup.className = 'slider';
        sliderGroup.id = `sliderGroup${frame_num}`;
        const slider = document.createElement("input");
        slider.type = "range";
        slider.id = `slider_item${frame_num}`;
        slider.min = 0;
        slider.max = 1;
        slider.step = 1;
        slider.value = 1;
        sliderGroup.appendChild(slider);
        item_bef.appendChild(sliderGroup);

        //アイテムグループを作成
        const itemGroup = document.createElement("div");
        itemGroup.className = 'form-wrapper';
        itemGroup.id = `form-wrapper${frame_num}`;
        sliderGroup.appendChild(itemGroup);
        
        const group = document.createElement("div");
        group.className = "form-group";
        group.id = `items[${frame_num}][${item_num}]`;

        const label = document.createElement("label");
        label.textContent = `枠 ${frame_num + 1} :`;
        label.htmlFor = `item[${frame_num}][${item_num}]`;
        label.style.marginRight = "3px";

        const input = document.createElement("input");
        input.type = "text";
        input.id = `item[${frame_num}][${item_num}]`;
        input.name = `items[${frame_num}][${item_num}]`;

        group.appendChild(label);
        group.appendChild(input);
        itemGroup.appendChild(group);

        const element = document.getElementById(`items[${frame_num}][${item_num}]`);
        element.style.marginLeft = `${style_position}px`;

        for (let i = 0; i < frame_num; i++) {
            const slider_item = document.getElementById(`slider_item${i}`);
            console.log(slider_item.max);
            slider_item.max = Number(slider_item.max) + 1;
            const current_slider = document.getElementById(`sliderGroup${i}`).offsetHeight;
            slider_item.style.height = current_slider + "px";
        };
    }

    function check_item() {
        title = document.getElementById('title').value;
        if (title != "") return true; 
        else {  
            alert("タイトルが入力されていません。");
            return false;
        }
    }