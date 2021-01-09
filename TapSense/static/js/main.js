'use strict';

var prev_time = null;
var list = [];
var error_count = 0;
var x = "0";

function getTime(event) {
    const time = new Date();
    var cur = time.getTime();
    if (prev_time !== null) {
        list.push(cur - prev_time);
    }
    document.getElementById("time").innerHTML = "経過時間(ミリ秒): " + list;
    prev_time = cur;
    
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
    var xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open("post", "/add_data", false);
    var data = {
        'timestamps': list,
        'error_count': error_count
    };
    xmlHttpRequest.setRequestHeader("Content-Type", "application/json");
    xmlHttpRequest.send(JSON.stringify(data))
});
