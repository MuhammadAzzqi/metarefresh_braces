// var fs = require('fs');
// var path = require('path');
// var gui = require('nw.gui');



$(function() {
    var win = chrome.app.window.current();

    function checkForMode(filename) {
        var fileExt = filename.match(/\.[a-z]*/)[0];
        // alert(fileExt);
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
        var fileContents = fs.readFileSync(filepath, 'utf-8');

        var filename = path.basename(filepath);
        checkForMode(filename);
        $('.filename').text(filename);

        editor.setValue(fileContents);
    }

    function saveFile (filepath) {
        var filename = path.basename(filepath);
        checkForMode(filename);
        $('.filename').text(filename);

        fs.writeFileSync(filepath, editor.getValue(), 'utf-8');
    }


    $('#open').on('change', function() {
        openFile($(this).val());
    });

    $('#save').on('change', function() {
        saveFile($(this).val());
    });

    $(window).on('resize', function() {
        editor.setSize(win.getBounds().width, win.getBounds().height);
    });


    var editor = CodeMirror(document.body, {
        theme: 'monokai',
        lineNumbers: true,
        mode: 'javascript',
        extraKeys: {
            'Cmd-O': function() {
                // $('#open').trigger('click');
                chrome.fileSystem.chooseEntry({type: "openFile"}, function() {
                    debugger
                });
            },
            'Cmd-S': function() {
                // $('#save').trigger('click');
                chrome.fileSystem.chooseEntry({type: "saveFile"}, function() {

                });
            }
        }
    });
    editor.setSize(win.getBounds().width, win.getBounds().height);
});