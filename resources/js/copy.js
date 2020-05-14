var u = navigator.userAgent;

function copy(value, alert = false) {
    var input = document.createElement("textarea");
    input.value = value;
    document.body.appendChild(input);
    if (u.match(/(iPhone|iPod|iPad);?/i)) {
        var range = document.createRange();
        range.selectNode(input);
        window.getSelection().addRange(range);
        var successful = document.execCommand('copy');
        window.getSelection().removeAllRanges();
    } else {
        input.setSelectionRange(0, input.value.length);
        input.select();
        document.execCommand("Copy"); // 执行浏览器复制命令
        var successful = document.execCommand('copy');
    }
    document.body.removeChild(input);
    if (alert) {
        iframe = document.createElement('IFRAME');
        iframe.style.display = 'none';
        iframe.setAttribute('src', 'data:text/plain,');
        document.documentElement.appendChild(iframe);
        window.frames[0].window.alert('复制成功');
        iframe.parentNode.removeChild(iframe);
    }
}