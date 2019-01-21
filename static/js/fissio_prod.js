var countDownDate = new Date("Sep 30, 2018 12:00:00").getTime();
var x = setInterval(updateCountdown, 1000);
updateCountdown();

function updateCountdown() {
    var now = new Date().getTime();
    var distance = countDownDate - now;

    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("countdown").innerHTML = days + "d " + pad(hours) + "h "
    + pad(minutes) + "m " + pad(seconds) + "s ";

    if (distance < 0) {
        clearInterval(x);
        document.getElementById("countdown").innerHTML = "TÄNÄÄN";
    }
}

function pad(num) {
    var s = num+"";
    while (s.length < 2) s = "0" + s;
    return s;
}

$("#register-button").click(function() {
    $("#register-form").removeClass("hidden");
    $("#content").addClass("hidden");
    $("#bgimg").addClass("hidden");
});