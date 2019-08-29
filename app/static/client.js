var el = x => document.getElementById(x);

function showPicker() {
  el("file-input").click();
}

function showPicked(input) {
  el("upload-label").innerHTML = input.files[0].name;
  var reader = new FileReader();
  reader.onload = function(e) {
    el("image-picked").src = e.target.result;
    el("image-picked").className = "";
  };
  reader.readAsDataURL(input.files[0]);
}

function analyze() {

  el("analyze-button").innerHTML = "Analyzing...";
  var xhr = new XMLHttpRequest();
  var loc = window.location;
  xhr.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`,true);
  xhr.onerror = function() {
    alert(xhr.responseText);
  };
  xhr.onload = function(e) {

    if (this.readyState === 4) {
      var response = JSON.parse(e.target.responseText);
      el("result1").innerHTML = `${response["result1"]}`;
      el("result2").innerHTML = `${response["result2"]}`;
    }
    el("analyze-button").innerHTML = "Analyze";
  };


  var theValue = document.getElementById("uniqueID").value;
  
  console.log(theValue)
  var fileData = new FormData();
  fileData.append("thevalue", theValue);
  xhr.send(fileData);

}
