document.addEventListener("DOMContentLoaded", function() {
    const questLang = document.querySelector(".quest-lang");
    const editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
        lineNumbers: true,
        mode: questLang.innerHTML.toLowerCase().trim(),
        theme: 'dracula',
        tabSize: 4,
        indentUnit: 4,
        indentWithTabs: false,
        matchBrackets: true,
        autoCloseBrackets: true,
        autoCloseTags: true,
        styleActiveLine: true,
        lineWrapping: true,
        viewportMargin: Infinity,
    });
    window.codeEditor = editor;
});