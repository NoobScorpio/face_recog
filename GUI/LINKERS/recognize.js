
function recognize(){   
    document.getElementById("startBtn").style.backgroundColor = "grey";
    document.getElementById("startBtn").disabled = true;
    var {PythonShell}=require('python-shell');

    console.log(PythonShell);
    clickStart();
        PythonShell.run('../ENGINE/predict.py', null, function (err) {
        if (err) console.log(err);
        console.log('finished');
        document.getElementById("startBtn").style.backgroundColor = "rgb(69, 194, 69)";
        document.getElementById("startBtn").disabled = false;
        // document.getElementById("take").value="Save";
        });
        
}
function killRecognize(){
    console.log("INSIDE KILL")
    var {PythonShell}=require('python-shell');
    pythonShell.childProcess.kill('SIGINT')
}
function clickStart(){
    setTimeout(function(){
        setInterval(function(){
            fetch('../ENGINE/models/checkin.txt')
            .then(response => response.text())
            .then(data => {
                var res=data.split('/');
                //console.log(res);
                cont=document.getElementById('checklist');
                cont.innerHTML=""
                //cont.innerHTML+=res
                for(i=0;i<res.length;i++){
                    cont.innerHTML+='<p>'+res[i]+'</p>'
                }
            });
        }, 3000);
    },10000);

}