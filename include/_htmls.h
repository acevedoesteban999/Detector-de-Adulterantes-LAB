const char index_html[] = R"rawliteral(

<!-- github/Esteban1914  -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 </title>
</head>
<body>
    <a role="button" href="/predict">Predecir</a>

    <a role="button" href="/download">Actulizar Modelo</a>
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
    <style>
    </style>
</head>
<body>
    <h2>Descargar Modelo</h2>
    <input type="text" name="n_model" id="id_model">
    <label for="n_model">Modelo</label>
    <br>
    <input type="text" name="n_ssid" id="id_ssid">
    <label for="n_ssid">SSID</label>
    <br>
    <input type="password" name="n_pass" id="id_pass">
    <label for="n_pass">Password</label>
    <br>
    <button onclick="Download()">Descargar</button>
    <br>
    <div style="display: none;" id="id_h">
        <h5 id="h5_h"></h5>
    </div>
</body>
<script>
    function Download()
    {   
        let  model=document.getElementById("id_model").value
        let ssid=document.getElementById("id_ssid").value
        let pass=document.getElementById("id_pass").value
        fetch("/post/download",
        {
            method: 'POST', 
            headers:{
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: "action=download&model="+String(model)+"&ssid="+String(ssid)+"&pass="+String(pass)
        })
        .then(res=> res.text()).then(res=>{ 
            let d=document.getElementById("id_h");
            let h=document.getElementById("h5_h");
            console.log(res)
            if(res=="OK")
            {
                d.style="";
                h.innerHTML="Actualizado Modelo Correctamente"
                h.style="color: green;";
            }
            else if(res=="Error1")
            {
                d.style="";
                h.innerHTML="Error al Descargar Modelo"
                h.style="color: red;";
            }
            else if(res=="Error2")
            {
                d.style="";
                h.innerHTML="Error al Salvar Modelo en Memoria"
                h.style="color: red;";
            }
            else if(res=="Error3")
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

const char predict_html[] = R"rawliteral(

<!-- github/Esteban1914  -->
<!DOCTYPE HTML><html>
<head>
    <title>ESP Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
    </style>
</head>
<body>
    <h2>Predecir Modelo</h2>
    <button onclick="Predict()">Predecir</button>
    <br>
    <div style="display: none;" id="id_h">
        <h5 id="h5_h"></h5>
    </div>
</body>
<script>
    function Predict()
    {   
        fetch("/post/predict",
        {
            method: 'POST', 
            headers:{
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: "action=predict"
        })
        .then(res=> res.text()).then(res=>{ 
            let d=document.getElementById("id_h");
            let h=document.getElementById("h5_h");
            console.log(res)
            if(res=="OK")
            {
                d.style="";
                h.innerHTML="Actualizado Modelo Correctamente"
                h.style="color: green;";
            }
            else if(res=="Error1")
            {
                d.style="";
                h.innerHTML="Error al Descargar Modelo"
                h.style="color: red;";
            }
            else if(res=="Error2")
            {
                d.style="";
                h.innerHTML="Error al Salvar Modelo en Memoria"
                h.style="color: red;";
            }
            else if(res=="Error3")
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