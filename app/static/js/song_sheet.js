function show_song_sheet(sheet_name) {
  $.ajax({
    type: "POST",
    url: "/getsheet/",
    data: { sheet_name: sheet_name },
    async: false,
    success: function (data) {
      console.log(data);
      for (var name in data) {
        (function (name) {
          //这个是function里i，即function的形参，也可以换成j，换成什么变量名都无所谓
          console.log(name);
          var x = document.getElementById("user_list").insertRow();
          var cell1 = x.insertCell();
          cell1.innerHTML = data[name]["music_name"];
          var cell2 = x.insertCell();
          cell2.innerHTML = data[name]["singer_name"];
          var cell = document.createElement("audio");
          cell.controls = "controls";
          cell.preload = "auto";
          cel.src = "../static/resource/mp3/" + data[name]["path"];
          x.appendChild(cell);
        })(name); //这是循环中的i,被作为参数传入
      }
    },
  });
}
function get_sheet_name() {
  $.ajax({
    type: "POST",
    url: "/getsheetname/",
    data: {},
    async: false,
    success: function (data) {
      console.log(data);
      return data;
    },
    error: function () {
      return null;
    },
  });
}

function add_song_sheet() {
  console.log("add sheet begin");
  bootbox.prompt({
    title: "新建歌单",
    message: "请输入歌单名",
    //"输入歌单名字 传入result里面"
    callback: function (result) {
      console.log(result);
      if (result != null && result != "") {
        $.ajax({
          url: "/addsheet/",
          type: "POST",
          data: { sheet_name: result },
          dataType: "json",
          success: function (res) {
            console.log(res);
            if (res["isok"] == 1) {
              //bootbox.alert("Successfully add!");
              ////location.reload();
              window.location.href = "/user/";
            } else if (res["isok"] == 0) {
              bootbox.alert("添加失败，该歌单已存在");
            } else {
              bootbox.alert("Disconnect... Please try again later");
            }
          },
          error: function (res) {
            bootbox.alert("Disconnect... Please try again later");
          },
        });
      } else;
    },
  });
}
function delete_song_sheet() {
  console.log("delete sheet begin");
  $.ajax({
    type: "POST",
    url: "/getsheetname/",
    data: {},
    async: false,
    success: function (data) {
      console.log(data);
      bootbox.prompt({
        inputType: "radio",
        inputOptions: data,
        title: "删除歌单",
        message: "请选择待删除的歌单",
        buttons: {
          confirm: {
            label: "Yes",
          },
          cancel: {
            label: "No",
          },
        },
        callback: function (result) {
          if (result != null && result != "") {
            $.ajax({
              url: "/deletesheet/",
              type: "POST",
              data: { sheet_name: result },
              dataType: "json",
              success: function (res) {
                console.log(res);
                if (res["isok"] == 1) {
                  //bootbox.alert("Successfully deleted!");
                  location.reload();
                } else if (res["isok"] == 0) {
                  bootbox.alert("Delete failed!NO FOUND!");
                } else {
                  bootbox.alert("Disconnect... Please try again later");
                }
              },
              error: function (res) {
                bootbox.alert("Disconnect... Please try again later");
              },
            });
          } else;
        },
      });
      return null;
    },
    error: function () {
      return null;
    },
  });
}
function add_song(music_id) {
  console.log("add song begin");
  $.ajax({
    type: "POST",
    url: "/getsheetname/",
    data: {},
    async: false,
    success: function (data) {
      console.log(data.length);
      if (data.length == 0) {
        bootbox.prompt({
          title: "您还没有歌单哦，请新建歌单",
          message: "请输入歌单名",
          //"输入歌单名字 传入result里面"
          callback: function (result) {
            console.log(result);
            $.ajax({
              url: "/addsheet/",
              type: "POST",
              data: { sheet_name: result },
              dataType: "json",
              success: function (res) {
                console.log(res);
                if (res["isok"] == 1) {
                  $.ajax({
                    url: "/addsong/",
                    type: "POST",
                    data: { sheet_name: result, music_id: music_id },
                    dataType: "json",
                    success: function (res) {
                      console.log(res);
                      if (res["isok"] == 1) {
                        //bootbox.alert("Successfully add!");
                        location.reload();
                      } else if (res["isok"] == 0) {
                        bootbox.alert("Add failed!NO FOUND!");
                      } else if (res["isok"] == -1) {
                        bootbox.alert("该歌曲已存在");
                      } else {
                        bootbox.alert("Disconnect... Please try again later");
                      }
                    },
                    error: function (res) {
                      bootbox.alert("Disconnect... Please try again later");
                    },
                  });
                } else if (res["isok"] == 0) {
                  bootbox.alert("添加失败，该歌单已存在");
                } else {
                  bootbox.alert("Disconnect... Please try again later");
                }
              },
              error: function (res) {
                bootbox.alert("Disconnect... Please try again later");
              },
            });
          },
        });
      } else {
        bootbox.prompt({
          inputType: "radio",
          inputOptions: data,
          title: "加入歌曲",
          message: "请选择歌单",
          buttons: {
            confirm: {
              label: "Yes",
            },
            cancel: {
              label: "No",
            },
          },
          callback: function (result) {
            if (result != null && result != "") {
              $.ajax({
                url: "/addsong/",
                type: "POST",
                data: { sheet_name: result, music_id: music_id },
                dataType: "json",
                success: function (res) {
                  console.log(res);
                  if (res["isok"] == 1) {
                    //bootbox.alert("Successfully add!");
                    location.reload();
                  } else if (res["isok"] == 0) {
                    bootbox.alert("Add failed!NO FOUND!");
                  } else if (res["isok"] == -1) {
                    bootbox.alert("该歌曲已存在");
                  } else {
                    bootbox.alert("Disconnect... Please try again later");
                  }
                },
                error: function (res) {
                  bootbox.alert("Disconnect... Please try again later");
                },
              });
            } else;
          },
        });
      }
    },
  });
}
function delete_song(sheet_name, music_id) {
  console.log("delete song begin");
  console.log(sheet_name);
  console.log(music_id);
  bootbox.confirm({
    message: "确定从该歌单移除这首歌曲吗？",
    buttons: {
      confirm: {
        label: "Yes",
      },
      cancel: {
        label: "No",
      },
    },

    callback: function (result) {
      if (result) {
        $.ajax({
          url: "/deletesong/",
          type: "POST",
          data: { sheet_name: sheet_name, music_id: music_id },
          dataType: "json",
          success: function (res) {
            console.log(res);
            if (res["isok"] == 1) {
              //bootbox.alert("Successfully deleted!");
              location.reload();
            } else if (res["isok"] == 0 || res["isok"] == -1) {
              bootbox.alert("Delete failed!NO FOUND!");
            } else {
              bootbox.alert("Disconnect... Please try again later");
            }
          },
          error: function (res) {
            bootbox.alert("Disconnect... Please try again later");
          },
        });
      } else;
    },
  });
}
