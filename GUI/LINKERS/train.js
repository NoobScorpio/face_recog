function takePic(){
    console.log("INSIDE TAKE PICS");
    var name=document.getElementById("name").value;
    var design=document.getElementById("design").value;

    if (name=="" && design==""){
        alert("ENTER NAME AND DESIGNATION")
    }
    else{
        var {PythonShell}=require('python-shell');
        // var path=require('path');
        document.getElementById("take").value="Hold on...";
    
        document.getElementById("name").value="";
        document.getElementById("design").value="";
    
        var opts={
            args:[name,design]
        };
    
        console.log(PythonShell);
    
            PythonShell.run('../ENGINE/take-pics.py', opts, function (err) {
            if (err) throw err;
            console.log('finished');
            document.getElementById("take").value="Take Photos";
            });
    
    }
 
}

function trainFace(){
    
    document.getElementById('save').value="Hang on...";
    var {PythonShell}=require('python-shell');

    console.log(PythonShell);

        PythonShell.run('../ENGINE/train.py', null, function (err) {
        if (err) throw err;
        console.log('finished');
        document.getElementById("take").value="Save";
        });

}