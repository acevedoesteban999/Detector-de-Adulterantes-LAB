function Predict()
{   
    let d=document.getElementById("id_h");
    let h=document.getElementById("h5_h");
    let h1=document.getElementById("h6_h");
    let sml=document.getElementById("_sml");
    let err_pred=document.getElementById("id_err_pred")
    let err_pred_mess=document.getElementById("id_err_pred_mess")
    d.style="display: none;"
    err_pred.style="display: none;"
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
        
        var values=params.get("list_data");
        values=values.split(",");
        update_chart(values);
        if(state=="OK")
        {
            d.style="";
            l=["100%","75%","50%","25%","0%"];
            let predict_class=params.get("predict_class")
            let predict_data=params.get("predict_data")
            h.innerHTML=l[parseInt(predict_class)];
            sml.innerHTML=predict_data+"%";
            if(predict_class=="0")
            {
                h.style="color: green;";
                h1.style="color: green;";
            }
            else if (predict_class=="1")
            {
                h.style="color: darkolivegreen;";
                h1.style="color: darkolivegreen;";
            }
            else if (predict_class=="2")
            {
                h.style="color: yellow;";
                h1.style="color: yellow;";
            }
            else if (predict_class=="3")
            {
                h.style="color: orange;";
                h1.style="color: orange;";
            }
            else
            {
                h.style="color: red;";
                h1.style="color: red;";
            }
        }
        else if(state=="E1")
        {
            err_pred.style="";
            err_pred_mess.innerHTML="Error al Conectar al Sensor"
        }
        else if(state=="E2")
        {
            err_pred.style="";
            err_pred_mess.innerHTML="Error al Leer Datos del Sensor"
        }
        else if(state=="E3")
        {
            err_pred.style="";
            err_pred_mess.innerHTML="Error al Cargar Modelo"
        }
        else
        {
            err_pred.style="";
            err_pred_mess.innerHTML="Error"
        }
    });
}
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
    .then(res=> res.text()).then(data=>{ 
            $('#UpdateModal').modal('hide');
            $('#ResetModal').modal('show'); 
    });   

}
function Configure()
{
    let ssid=document.getElementById("id_ap_ssid").value
    let pass=document.getElementById("id_ap_pass").value
    fetch("/post/config",
    {
        method: 'POST', 
        headers:{
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "action=config&ssid="+String(ssid)+"&pass="+String(pass)
    })
    .then(res=> res.text()).then(data=>{ 
        $('#ConfigModal').modal('hide');
        $('#ResetConfigModal').modal('show'); 
    });   

}
function Reset_Update()
{
    fetch("/post/reset_update",
    {
        method: 'POST', 
        headers:{
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });   

}
var myChart;
function update_chart(_data)
    {
        myChart.data.datasets[0].data=_data;
        myChart.update();
}
function init_chart()
{
    _labels=[410,435,460,485,510,535,560,585,601,645,680,705,730,760,810,860,900,940];
    //_data=values;
    const ctx = document.getElementById("Chart");
    ctx.height = 200;
    myChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: _labels,
            datasets: [
                {
                label: "Mustra",
                backgroundColor: "",
                tension: 0.1,
                borderColor: "",
                fill: false,
                data: []//[0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
                },
            ],
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
                y: {
                    stacked: true,
                    grid: {
                    display: true,
                    color: "rgba(255,99,132,0.2)"
                    }
                },
                x: {
                    grid: {
                    display: false
                    }
                }
                }
        },
    }); 
}
init_chart();