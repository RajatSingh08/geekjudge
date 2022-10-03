// Hook up ACE editor to all textareas with data-editor attribute
$(function create_editor() {
    $('textarea[data-editor]').each(function () {
        var textarea = $(this);
        var theme = textarea.data('editor');
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
            enableBasicAutocompletion: true,
            enableSnippets: true,
            enableLiveAutocompletion: true, 
            showGutter: true, 
            showLineNumbers: true,
            fontSize: 17,
            theme: 'ace/theme/' + theme,
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
    var editDiv = $("#custom-editor");
    var editor = ace.edit(editDiv[0]);
    var editor_mode = 'c_cpp'
    var editor_option = $("#language").val();
    if(editor_option == 'C' || editor_option == 'C++') editor_mode = 'c_cpp';
    if(editor_option == 'Java') editor_mode = 'java';
    if(editor_option == 'Python2' || editor_option == 'Python3') editor_mode = 'python';

    editor.setOptions({
        mode: 'ace/mode/' + editor_mode,
    });
}

// Hook up ACE editor to all textareas with data-editor attribute
function update_theme() {
    var editDiv = $("#custom-editor");
    var editor = ace.edit(editDiv[0]);
    var theme = $("#theme").val();
    
    editor.setOptions({
        theme: 'ace/theme/' + theme,
    });
}