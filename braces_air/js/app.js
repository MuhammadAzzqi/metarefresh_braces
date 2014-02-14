var braces;

var handle_save = function() {
  var f_name = prompt("Enter File Name: Saved in Documents");
  var code_str = document.querySelector("#braces_editor")

  var code_str = braces.getValue();
  var myFile = air.File.documentsDirectory.resolvePath(f_name); 
  var myFileStream = new air.FileStream(); 
  myFileStream.open(myFile, air.FileMode.WRITE); 
  myFileStream.writeMultiByte(code_str, 'utf-8');

}

var handle_open = function() {
  var f_name = prompt("Enter File Name: looks in Documents");

  var myFile = air.File.documentsDirectory.resolvePath(f_name); 
  var myFileStream = new air.FileStream(); 
  myFileStream.addEventListener(air.Event.COMPLETE, completeHandler); 
  myFileStream.openAsync(myFile, air.FileMode.READ); 
  var code_str = ""; 
       
  function completeHandler(event) {
    code_str = myFileStream.readMultiByte(myFileStream.bytesAvailable, "iso-8859-1"); 
    braces.setValue(code_str);
  }
  
}

var setup_braces = function() {
  var editor_div = document.querySelector("#braces_editor");
  braces = CodeMirror.fromTextArea(editor_div, {
    mode:  "javascript",
    theme: "monokai",
    lineNumbers: true
  });

  var save_btn = document.querySelector("#save_btn");
  save_btn.addEventListener('click', handle_save, false);

  var open_btn = document.querySelector("#open_btn");
  open_btn.addEventListener('click', handle_open, false);
}

var app_load = function() { 
  setup_braces();
} 