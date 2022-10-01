// Hook up ACE editor to all textareas with data-editor attribute
$(function create_editor() {
    $('textarea[data-editor]').each(function () {
        var textarea = $(this);
        var editDiv = $('<div>', {
            position: 'absolute',
            width: textarea.width(),
            height: textarea.height(),
            'class': textarea.attr('class'),
            'id':'custom-editor'
        }).insertBefore(textarea);

        textarea.css('display', 'none'); // to avoid extra space below textarea
        ace.require("ace/ext/language_tools"); // language tools: brackets, tabs, indentations, etc
        var editor = ace.edit(editDiv[0]);

        var editor_mode = 'c_cpp';     

        editor.setOptions({
            enableLiveAutocompletion: true, 
            showGutter: true, 
            showLineNumbers: true,
            fontSize: 17,
            theme: 'ace/theme/xcode',
            mode: 'ace/mode/' + editor_mode,
            showPrintMargin: false,
        });

        editor.session.setValue(textarea.val());

        textarea.closest('form').submit(function () {
        textarea.val(editor.getSession().getValue());
        })
    });
});

// Hook up ACE editor to all textareas with data-editor attribute
function update_editor() {
    $('textarea[data-editor]').each(function () {
        console.log("changed!");
        var textarea = $(this);
        var editDiv = $("#custom-editor");
         
        ace.require("ace/ext/language_tools"); // language tools: brackets, tabs, indentations, etc
        var editor = ace.edit(editDiv[0]);

        var editor_mode = 'c_cpp'
        var option = $("#language").val();
        if(option == 'C' || option == 'C++') {
            editor_mode = 'c_cpp';
        }
        if(option == 'Java') {
            editor_mode = 'java';
        }
        if(option == 'Python2' || option == 'Python3') {
            editor_mode = 'python';
        }

        editor.setOptions({
            enableLiveAutocompletion: true, 
            showGutter: true, 
            showLineNumbers: true,
            fontSize: 17,
            theme: 'ace/theme/xcode',
            mode: 'ace/mode/' + editor_mode,
            showPrintMargin: false,
        });

        editor.session.setValue(textarea.val());

        textarea.closest('form').submit(function () {
        textarea.val(editor.getSession().getValue());
        })
    });
}