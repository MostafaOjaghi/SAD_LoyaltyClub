function settings_clicked(){
  document.getElementById("settings-layout").style.display = "block";
  document.getElementById("analytics-layout").style.display = "none";
}

function analytics_clicked(){
  document.getElementById("settings-layout").style.display = "none";
  document.getElementById("analytics-layout").style.display = "block";
}