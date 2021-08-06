PD_API_URL = "http://localhost:8082"


function settings_clicked() {
  document.getElementById("settings-layout").style.display = "block";
  document.getElementById("analytics-layout").style.display = "none";
}

function analytics_clicked() {
  document.getElementById("settings-layout").style.display = "none";
  document.getElementById("analytics-layout").style.display = "block";
}

function submite_score_form() {
  close_alert()
  let score_form = document.forms["score_form"];
  score_coefficient = score_form["score_coefficient_input"].value
  score_period = score_form["score_period_input"].value
  max_order_score = score_form["max_order_score_input"].value
  let data = [score_coefficient ? `score_coefficient=${score_coefficient}` : "", score_period ? `score_period=${score_period}` : "" , max_order_score ? `max_order_score=${max_order_score}` : ""]
  data = data.filter(x => x != "").join("&")
  console.log(data)
  var request = {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
    body: data
  };
  fetch(PD_API_URL + "/score-parameters", request).then(function (response) {
    stat = response.status
    if (stat == 200) {
      // location.replace(url)
      elem = document.getElementById("success_alert")
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      console.log("parameters changed")
    score_form.reset()
    } else {
      elem = document.getElementById("danger_alert") 
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      err_elem = document.getElementById("error_message").innerHTML = response.statusText
      console.log(response.statusText)
    }
  }).catch(function (error) {
    console.log("Error: " + error);
  })
}

function close_alert() {
  document.getElementById("danger_alert").style.opacity = "0";
  document.getElementById("danger_alert").style.visibility = "hidden";
  document.getElementById("success_alert").style.opacity = "0";
  document.getElementById("success_alert").style.visibility = "hidden";
}
