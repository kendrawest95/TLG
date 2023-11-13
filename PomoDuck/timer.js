$(document).ready(function () {
  $("#startButton").on("click", function () {
      var workDuration = $("input[name='timer']:checked").val();
      var breakDuration = (workDuration === '25') ? '5' : '10';
      // Make an AJAX request to start the timer
      $.ajax({
          type: "GET",
          url: `/start_timer/${workDuration}/${breakDuration}`,
          success: function (response) {
              startCountdown(workDuration * 60); // Pass the total seconds for countdown
              alert(response.message);
          },
          error: function(error) {
            console.error("error", error);
          }
      });
  });
});

function startCountdown(totalSeconds) {
  var display = document.getElementById("timerDisplay");
  var minutes, seconds;

  var countdown = setInterval(function () {
      minutes = Math.floor(totalSeconds / 60);
      seconds = totalSeconds % 60;

      // Display the formatted time
      display.innerHTML = pad(minutes) + ":" + pad(seconds);

      // Check if countdown is complete
      if (totalSeconds <= 0) {
          clearInterval(countdown);
          display.innerHTML = "00:00"; // Optional: Show 00:00 when the countdown is complete
      } else {
          totalSeconds--;
      }
  }, 1000);
}

function pad(number) {
  return (number < 10 ? "0" : "") + number;
}
