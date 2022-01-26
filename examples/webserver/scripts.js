/*! JavaScript for GPS Server Demo */

var gInterval = 5000; // 5 seconds
var gTimer = 0;
var FIXDESC = ["No Fix", "2D", "3D"];

// Refresh web page
function refreshPage(obj) {
    "use strict";

    document.getElementById('date').innerHTML = obj.date;
    document.getElementById('time').innerHTML = obj.time;
    document.getElementById('latitude').innerHTML = obj.latitude;
    document.getElementById('longitude').innerHTML = obj.longitude;
    document.getElementById('elevation').innerHTML = obj.elevation;
    document.getElementById('speed').innerHTML = obj.speed;
    document.getElementById('track').innerHTML = obj.track;
    document.getElementById('siv').innerHTML = obj.siv;
    document.getElementById('pdop').innerHTML = obj.pdop;
    document.getElementById('hdop').innerHTML = obj.hdop;
    document.getElementById('vdop').innerHTML = obj.vdop;
    document.getElementById('fix').innerHTML = FIXDESC[obj.fix - 1];

}

// Execute REST GET request to retrieve latest gps data
function getGPS() {
    "use strict";

    var obj;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/gps');
    xhr.onload = function () {
        if (xhr.status === 200) {
            obj = JSON.parse(xhr.responseText);
            refreshPage(obj);
        }
        else {
            alert('Request failed.  Returned status of ' + xhr.status);
        }
    };
    xhr.send();

}

// Set interval timer for GET request
function setTimer() {
    "use strict";

    clearInterval(gTimer);
    gTimer = setInterval("getGPS()", gInterval);
}

// Functions to call when body first loaded
function start() {
    "use strict";

    getGPS();
    setTimer();

}
