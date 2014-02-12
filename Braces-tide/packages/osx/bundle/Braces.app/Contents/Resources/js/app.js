var win = Ti.UI.currentWindow;
var fs = Ti.Filesystem;


$(function() {

    function checkForMode(filename) {
        var fileExt = filename.match(/\.[a-z]*/)[0];

        if(fileExt === '.js') {
            editor.setOption('mode', 'javascript');
        } else if(fileExt === '.css') {
            editor.setOption('mode', 'css');
        } else if(fileExt === '.html') {
            editor.setOption('mode', 'htmlmixed');
        } else {
            editor.setOption('mode', '');
        }
    }

    function openFile (filepath) {
        filepath = filepath[0];
        var file = fs.getFile(filepath);
        var fileContents = file.read().toString();

        var filename = filepath;
        checkForMode(filename);
        $('.filename').text(filename);

        editor.setValue(fileContents);
    }

    function saveFile (filepath) {
        filepath = filepath[0];
        var filename = filepath;
        checkForMode(filename);
        $('.filename').text(filename);

        var file = fs.getFile(filepath);
        file.write(editor.getValue());
        
    }


    $('#open').on('change', function() {
        console.log($(this).val());
        openFile($(this).val());
    });

    $('#save').on('change', function() {
        saveFile($(this).val());
    });

    $(window).on('resize', function() {
        editor.setSize(win.getWidth(), win.getHeight());
    });


    var editor = CodeMirror(document.body, {
        theme: 'monokai',
        lineNumbers: true,
        mode: 'javascript',
        extraKeys: {
            'Cmd-O': function() {
                // $('#open').trigger('click');
                win.openFileChooserDialog(openFile, {
                    multiple: false,
                    types: ['js', 'html', 'css']
                });
            },
            'Cmd-S': function() {
                win.openSaveAsDialog(saveFile);
            }
        }
    });

    editor.setSize(win.getWidth(), win.getHeight());
});