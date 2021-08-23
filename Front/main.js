var PD_API_URL = "http://localhost:8082"
var focused_add_rank = null
var focused_update_rank = null

window.onload = function () {
  points = []
  fetch("http://127.0.0.1:8082/annual-income").then(
    res => {
      res.json().then(
        data => {
          console.log(data);
          if (data.length > 0) {

            var temp = "";
            data.forEach((itemData) => {
              points.push({ x: new Date(Date.parse(itemData.date)), y: itemData.sale });
            });
          }

          var chart = new CanvasJS.Chart("chartContainer_1",
            {
              title: {
                text: "income - per month"
              },
              data: [
                {
                  type: "line",
                  dataPoints: points
                }
              ]
            });

          chart.render();
        }
      )
    })

  order_points = [[], [], []]
  fetch("http://127.0.0.1:8082/number-of-orders").then(
    res => {
      res.json().then(
        data => {
          console.log(data);
          data[0].forEach((itemData) => {
            order_points[0].push({ x: itemData.my_number, y: itemData.counter });
          });
          data[1].forEach((itemData) => {
            order_points[1].push({ x: itemData.my_number, y: itemData.counter });
          });
          data[2].forEach((itemData) => {
            order_points[2].push({ x: itemData.my_number, y: itemData.counter });
          });
          console.log("number of orders", order_points);

          var chart = new CanvasJS.Chart("chartContainer_2",
            {
              title: {
                text: "number of customers - per number of orders"
              },
              data: [
                {
                  type: "line",
                  dataPoints: order_points[0]
                },
                {
                  type: "line",
                  dataPoints: order_points[1]
                },{
                  type: "line",
                  dataPoints: order_points[2]
                },
              ]
            });

          chart.render();
        }
      )
    })

  reload_ranks_table()

}

function reload_ranks_table() {
  var request = {
    method: 'GET',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }
  };
  fetch(PD_API_URL + "/rank", request).then(function (response) {
    stat = response.status
    if (stat == 200) {
      response.text().then(function (res) {
        ranks = JSON.parse(res)
        replace_ranks(ranks)
      })
    } else {
      elem = document.getElementById("danger_alert")
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      document.getElementById("error_message").innerHTML = response.statusText
      console.log(response.statusText)
    }
  }).catch(function (error) {
    console.log("Error: " + error);
  })

}

function replace_ranks(ranks) {
  ranks_table_html = ""
  Object.keys(ranks).forEach(function (key) {
    ranks_table_html += `<tr>
    <td>${key}</td>
    <td>${ranks[key]["off"] * 100}%</td>
    <td>${ranks[key]["rank range"][0]}-${ranks[key]["rank range"][1]}</td>
    <td>${ranks[key]["monthly limit"]}</td>
    <td>${ranks[key]["free shipping"]}</td>
    <td><button type="button" class="close" aria-label="Close" data-toggle="modal"
                  data-target="#deleteRankModal"
                  onclick="focused_add_rank = this.parentElement.parentElement.firstElementChild.innerHTML"><span
                    aria-hidden="true">&times;</span></button></td>
    <td><i class="fa fa-edit" data-toggle="modal" data-target="#updateRankModal"
      onclick="focused_update_rank = this.parentElement.parentElement.firstElementChild.innerHTML"></i>
    </td>
  </tr>`
  })
  document.getElementById("ranks-table-content").innerHTML = ranks_table_html
}

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
  let data = [score_coefficient ? `score_coefficient=${score_coefficient}` : "", score_period ? `score_period=${score_period}` : "", max_order_score ? `max_order_score=${max_order_score}` : ""]
  data = data.filter(x => x != "").join("&")
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
      document.getElementById("success_message").innerHTML = "parameters changes successfuly."
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      console.log("parameters changed")
      score_form.reset()

    } else {
      elem = document.getElementById("danger_alert")
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      document.getElementById("error_message").innerHTML = response.statusText
      console.log(response.statusText)
    }
  }).catch(function (error) {
    console.log("Error: " + error);
  })
}

function submite_birthday_form() {
  close_alert()
  let birthday_form = document.forms["birthday_form"];
  birthday_off = birthday_form["birthday_off_input"].value
  birthday_off_limit = birthday_form["birthday_off_limit_input"].value
  let data = [birthday_off ? `birthday_off=${birthday_off}` : "", birthday_off_limit ? `birthday_off_limit=${birthday_off_limit}` : ""]
  data = data.filter(x => x != "").join("&")
  var request = {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
    body: data
  };
  fetch(PD_API_URL + "/birthday-parameters", request).then(function (response) {
    stat = response.status
    if (stat == 200) {
      // location.replace(url)
      elem = document.getElementById("success_alert")
      document.getElementById("success_message").innerHTML = "parameters changes successfuly."
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      console.log("parameters changed")
      birthday_form.reset()

    } else {
      elem = document.getElementById("danger_alert")
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      document.getElementById("error_message").innerHTML = response.statusText
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

function submite_add_rank_form() {
  close_alert()

  let add_rank_form = document.forms["add_rank_form"];
  rank_name = add_rank_form["rank_name_input"].value
  off = add_rank_form["off_input"].value
  monthly_limit = add_rank_form["monthly_limit_input"].value
  rank_range_max = add_rank_form["rank_range_max_input"].value
  rank_range_min = add_rank_form["rank_range_min_input"].value
  free_shipping = add_rank_form["free_shipping_input"].checked
  if (!rank_name || !off || !monthly_limit || !rank_range_max || !rank_range_min) {
    elem = document.getElementById("danger_alert")
    elem.style.opacity = "1";
    elem.style.visibility = "visible";
    document.getElementById("error_message").innerHTML = "fill all fields"
    return
  }

  let data = [`name=${rank_name}`, `off=${off}`, `monthly_limit=${monthly_limit}`, `rank_range=${rank_range_min}_${rank_range_max}`,
  free_shipping ? `free_shipping=true` : `free_shipping=false`]
  data = data.filter(x => x != "").join("&")
  var request = {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
    body: data
  };
  fetch(PD_API_URL + "/rank", request).then(function (response) {
    stat = response.status
    if (stat == 200) {
      // location.replace(url)
      elem = document.getElementById("success_alert")
      document.getElementById("success_message").innerHTML = "rank added successfuly."
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      console.log("rank added successfuly.")
      add_rank_form.reset()
      reload_ranks_table()

    } else {
      elem = document.getElementById("danger_alert")
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      document.getElementById("error_message").innerHTML = response.statusText
      console.log(response.statusText)
    }
  }).catch(function (error) {
    console.log("Error: " + error);
  })
}

function delete_rank() {
  close_alert()
  let data = `name=${focused_add_rank}`
  var request = {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8;' },
    body: data
  };
  fetch(PD_API_URL + "/rank", request).then(function (response) {
    stat = response.status
    if (stat == 200) {
      // location.replace(url)
      elem = document.getElementById("success_alert")
      document.getElementById("success_message").innerHTML = "rank deleted successfuly."
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      console.log("rank deleted successfuly.")
      reload_ranks_table()

    } else {
      elem = document.getElementById("danger_alert")
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      document.getElementById("error_message").innerHTML = response.statusText
      console.log(response.statusText)
    }
  }).catch(function (error) {
    console.log("Error: " + error);
  })
}

function update_rank() {
  let update_rank_form = document.forms["update_rank_form"];
  rank_name = focused_update_rank
  off = update_rank_form["update_off_input"].value
  monthly_limit = update_rank_form["update_monthly_limit_input"].value
  rank_range_max = update_rank_form["update_rank_range_max_input"].value
  rank_range_min = update_rank_form["update_rank_range_min_input"].value
  free_shipping = update_rank_form["update_free_shipping_input"].checked
  if (!rank_name && !off && !monthly_limit && !rank_range_max && !rank_range_min) {
    elem = document.getElementById("danger_alert")
    elem.style.opacity = "1";
    elem.style.visibility = "visible";
    document.getElementById("error_message").innerHTML = "no field to update"
    return
  }
  if ((rank_range_max && !rank_range_min) || (!rank_range_max && rank_range_min)){
    elem = document.getElementById("danger_alert")
    elem.style.opacity = "1";
    elem.style.visibility = "visible";
    document.getElementById("error_message").innerHTML = "can't fill just one rank range field"
    return
  }
  let data = [`name=${rank_name}`, off ? `off=${off}` : "", monthly_limit ? `monthly_limit=${monthly_limit}` : "", 
              rank_range_min&&rank_range_max ? `rank_range=${rank_range_min}_${rank_range_max}` : "", free_shipping ? `free_shipping=true` : `free_shipping=false`]
  data = data.filter(x => x != "").join("&")
  console.log(data)  
  var request = {
    method: 'PUT',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
    body: data
  };
  fetch(PD_API_URL + "/rank", request).then(function (response) {
    stat = response.status
    if (stat == 200) {
      // location.replace(url)
      elem = document.getElementById("success_alert")
      document.getElementById("success_message").innerHTML = "rank updated successfuly."
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      console.log("rank updated successfuly.")
      update_rank_form.reset()
      reload_ranks_table()

    } else {
      elem = document.getElementById("danger_alert")
      elem.style.opacity = "1";
      elem.style.visibility = "visible";
      document.getElementById("error_message").innerHTML = response.statusText
      console.log(response.statusText)
    }
  }).catch(function (error) {
    console.log("Error: " + error);
  })
}