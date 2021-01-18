// input[type="radio"]を取得
const input = document.getElementsByTagName("input");

const radioList = [];
for (var i=0; i<input.length; i++) {
    var temp = input[i];
    if (temp.type === "radio") {
        var id    = temp.id;
        var temp2 = document.querySelector('label[for="' + id + '"]');
        var set = {
            radio: temp,
            label: temp2
        };
        radioList.push(set);
    }
}

radioList.forEach(function(e) {
    e.radio.addEventListener("click", function() {
        // 全てのラベルの.checkedクラスを外す
        for (var i=0; i<radioList.length; i++) {
            radioList[i].label.classList.remove("checked");
        }
        // .checkedクラスをつける
        e.label.classList.add("checked");
    });
});