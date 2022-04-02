//生成从minNum到maxNum的随机数
function randomNum(minNum, maxNum) {
  switch (arguments.length) {
    case 1:
      return parseInt(Math.random() * minNum + 1, 10);
      break;
    case 2:
      return parseInt(Math.random() * (maxNum - minNum + 1) + minNum, 10);
      break;
    default:
      return 0;
      break;
  }
}
function randompic() {
  var num = randomNum(0, 512);
  var path = "../static/resource/pic/result(" + num + ").png";
  var tep = document.getElementById("headpic");
  console.log(num);
  console.log(path);
  tep["src"] = path;
}

// 上传图片
$("#picfile").change(function () {
  var filePath = $(this).val();
  let fr = new FileReader(); //创建new FileReader()对象
  let imgObj = this.files[0]; //获取图片
  fr.readAsDataURL(imgObj); //将图片读取为DataURL
  if (
    filePath.indexOf("jpg") != -1 ||
    filePath.indexOf("JPG") != -1 ||
    filePath.indexOf("PNG") != -1 ||
    filePath.indexOf("png") != -1
  ) {
    fr.onload = function () {
      $(".setselfmsg .userpic img").attr("src", this.result);
    };
  } else {
    confirm("您未上传文件，或者您上传文件类型有误！");
    return false;
  }
});
