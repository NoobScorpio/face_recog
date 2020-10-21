
var message="";
var names="";
function GetFileInfo () {

    var fileInput =  document.getElementById("FileInput").files;
        console.log(fileInput);
            for (var i = 0; i < fileInput.length; i++) {
                var file = fileInput[i]['path'];
                var name = fileInput[i]['name'];
                console.log(file)
                if(i==fileInput.length-1){
                    message=message+file
                    names=names+name
                }else{
                    message=message+file+","
                    names=names+name+","
                }
            }  
            console.log(message)
            console.log(names)
      
    document.getElementById("title").innerText="Selected Files"
  }
  //ENND
function upload(){
    
    var name=document.getElementById('name').value;
    var design=document.getElementById('design').value;
    
    if( name=="" && design==""){
        alert("ENTER NAME AND DESIGNATION");
        return false;
    }
    else{
        const fs = require('fs')
        const textFileName = 'picsData.txt';
        const namesFile='picsNames.txt';
    
        if (message !== null) {
    
            fs.writeFile( textFileName, message, (msg)=>{
                console.log("MADE")
            })
    
            fs.writeFile( namesFile, names, (msg)=>{
                console.log("MADE")
            })
          }
        
          var {PythonShell}=require('python-shell');
    
          console.log(PythonShell);
        
          
            var opts={
            args:[name,design]
            };
    
              PythonShell.run('../ENGINE/upload.py', opts, function (err) {
              if (err) throw err;
              console.log('finished');
              document.getElementById("take").value="Save";
              });
    
    
            return false;
    }
    
}