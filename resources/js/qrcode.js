updateQrCode = function () {
    var options = {
        render: "image", //image  canvas div
        ecLevel: "H", //识别度 L low 7% ,M 15% , Q 25%, H 30%
        minVersion: parseInt(10, 10),
        color: "#2a1212", //二维码黑色小块颜色
        bgColor: "#fff", //背景颜色
        text: $("#text").val(), //二维码内容
        size: parseInt(300, 10),//二维码大小 100-1000
        radius: parseInt(50, 10) * 0.01,  //格子圆角程度0-50
        quiet: parseInt(1, 10), //1-4
        mode: parseInt(4, 10), //0仅二维码 1文字二维码 2独占一行文字二维码3图片二维码4行内图片二维码
        label: "牛奶视频",
        labelsize: parseInt(14, 10) * 0.01,
        fontname: "22px",
        fontcolor: "#2274e5", //文字logo颜色
        image: $("#imgLogo")[0], //图片logo对象
        imagesize: parseInt(18, 10) * 0.01
    };

    $("#qrcode").qrcode(options);
};
update = function () {
    updateQrCode();
};
window.onload = function () {
    update();
};