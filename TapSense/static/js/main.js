'use strict';

var prev_time = null;
var timestamps = [];
var keys = [];
var error_count = 0;
var x = "0";

function getTime(event) {
    const time = new Date();
    var cur = time.getTime();
    if (prev_time !== null) {
        timestamps.push(cur - prev_time);
    }
    document.getElementById("time").innerHTML = "経過時間(ミリ秒): " + timestamps;
    prev_time = cur;

    keys.push(event.key)
    // document.getElementById("keys").innerHTML = "入力キー: " + keys;
    
    if (event.key == "Backspace") {
        error_count++;
    }
    document.getElementById("count").innerHTML = "エラー回数: " + error_count;
}



const btn = document.getElementById('btn');
btn.addEventListener('click', () => {
    // $.ajax({
    //     type: 'POST',
    //     url: '/success',
    //     data:JSON.stringify({
    //         'timestamps': list,
    //         'error_count': error_count
    //     }),
    //     contentType: 'application/json',
    //     success: function(response){
    //         console.log(response);
    //     },
    //     error: function(error){
    //         console.log(error);
    //     }
    // })
    var name = document.getElementById("name").value;
    var sentence = document.getElementById("sentence").textContent;
    var sentence_length = sentence.length
    var joy_sadness = document.getElementById("joy_sadness").value;
    var anger_fear = document.getElementById("anger_fear").value;
    var trust_disgust = document.getElementById("trust_disgust").value;
    var interest_distraction = document.getElementById("interest_distraction").value;
    var impression_pessimism = document.getElementById("impression_pessimism").value;
    console.log(sentence_length);
    console.log(joy_sadness);
    var xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open("post", "/add_data", false);
    var data = {
        'timestamps': timestamps,
        'keys': keys,
        'error_count': error_count,
        'name': name,
        'sentence_length': sentence_length,
        'joy_sadness': parseInt(joy_sadness),
        'anger_fear': parseInt(anger_fear),
        'trust_disgust': parseInt(trust_disgust),
        'interest_distraction': parseInt(interest_distraction),
        'impression_pessimism': parseInt(impression_pessimism)
    };
    xmlHttpRequest.setRequestHeader("Content-Type", "application/json");
    xmlHttpRequest.send(JSON.stringify(data))
    alert("データが送信されました。")
});
