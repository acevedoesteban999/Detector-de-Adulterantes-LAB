
const char styles_css[]=R"rawliteral(

    html, body {
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      text-align: center;
    }
    input{
       text-align: center;
    }
    label{
        font-size: 20px;
    }

    .button {
      display: inline-block;
      padding: 20px 40px;
      font-size: 24px;
      border-radius: 20px;
      text-decoration: none;
      background-color: #4CAF50;
      color: white;
      border: none;
      margin-top: 15px;
      margin-bottom: 15px;
    }
    .button1 {
      display: inline-block;
      padding: 10px 20px;
      font-size: 12px;
      border-radius: 10px;
      text-decoration: none;
      background-color: #4CAF50;
      color: white;
      border: none;
      margin-top: 5px;
      margin-bottom: 5px;
    }
    input[type="text"], input[type="password"] {
      padding: 10px;
      font-size: 16px;
      border-radius: 10px;
      border: 1px solid #ccc;
      margin-bottom: 10px;
    }
)rawliteral";
const char index_html[] = R"rawliteral(

<!-- github/Esteban1914  -->
<!DOCTYPE html>
<html lang="en">

<head>
    <link href="/styles.css" rel="stylesheet">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 </title>
</head>
<body>
    <a class="button" role="button" href="/predict">Predecir</a>
    <hr>
    <a class="button" role="button" href="/download">Actualizar Modelo</a>
</body>
</html>

)rawliteral";
const char download_html[] = R"rawliteral(

<!-- github/Esteban1914  -->
<!DOCTYPE HTML><html>
<head>
    <title>ESP Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <link href="/styles.css" rel="stylesheet">
    <style>
    </style>
</head>
<body>
    <h1>Descargar Modelo</h1>
    <div style="display: %DISPLAY%;color:%COLOR%" id="id_h">
            <h2 id="h5_h">%H5_DATA%</h2>
    </div>
    <div id="div_al">
        <h5>Modelo actual: <strong>%MODEL_NAME%</strong></h5>
        <label for="n_model">Modelo</label>
        <br>
        <input autocomplete="new-password" placeholder="Modelo" type="text" name="n_model" id="id_model" value="%MODEL_NAME%">
        <br>
        <label for="n_ssid">SSID</label>
        <br>
        <input autocomplete="new-password" placeholder="SSID Wifi" type="text" name="n_ssid" id="id_ssid" value="%SSID%">
        <br>
        <label for="n_pass">Password</label>
        <br>
        <input autocomplete="new-password" placeholder="Password Wifi" type="password" name="n_pass" id="id_pass" value="%PASS%">
        <br>
        <button class="button" onclick="Download()">Descargar</button>
        <br>
    </div>
    
    <a class="button1" role="button" href="/">Regresar</a>
</body>
<script>
    function Download()
    {   

        let  model=document.getElementById("id_model").value
        let ssid=document.getElementById("id_ssid").value
        let pass=document.getElementById("id_pass").value
        let d=document.getElementById("id_h");
        let h=document.getElementById("h5_h");
        d.style="display: none;"
        fetch("/post/download",
        {
            method: 'POST', 
            headers:{
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: "action=download&model="+String(model)+"&ssid="+String(ssid)+"&pass="+String(pass)
        })
        .then(res=> res.text()).then(data=>{ 
                document.getElementById("div_al").style="display: none;"
                d.style="";
                h.innerHTML=data;
                h.style="color: black;";
        });
    }
</script>
</html>

)rawliteral";

const char predict_html[] = R"rawliteral(

<!-- github/Esteban1914  -->
<!DOCTYPE HTML><html>
<head>
    <link href="/styles.css" rel="stylesheet">
    <title>ESP Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
    </style>
</head>
<body>
    <h2>Predecir Modelo</h2>
    <h5>Modelo actual: <strong>%MODEL_NAME%</strong><h5>
    <button class="button" onclick="Predict()">Predecir</button>
    <br>
    <div style="display: none;" id="id_h">
        <h2 id="h5_h"></h2>
    </div>
    <a class="button1" role="button" href="/">Regresar</a>
</body>
<script>
    function Predict()
    {   
        let d=document.getElementById("id_h");
        let h=document.getElementById("h5_h");
        d.style="display: none;"
        
        fetch("/post/predict",
        {
            method: 'POST', 
            headers:{
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: "action=predict"
        })
        .then(res=> res.text()).then(data=>{ 
            var params = new URLSearchParams(data);
            let state=params.get("state");
            if(state=="OK")
            {
                d.style="";
                h.innerHTML=params.get("predict_data");
                h.style="color: green;";
            }
            else if(state=="E1")
            {
                d.style="";
                h.innerHTML="Error al Conectar al Sensor"
                h.style="color: red;";
            }
            else if(state=="E2")
            {
                d.style="";
                h.innerHTML="Error al Leer Datos del Sensor"
                h.style="color: red;";
            }
            else if(state=="E3")
            {
                d.style="";
                h.innerHTML="Error al Cargar Modelo"
                h.style="color: red;";
            }
            else
            {
                d.style="";
                h.innerHTML="Error"
                h.style="color: red;";
            }
        });
    }
</script>
</html>

)rawliteral";