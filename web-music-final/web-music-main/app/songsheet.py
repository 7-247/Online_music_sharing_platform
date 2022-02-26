from app import app
from app.models import Music, User, SongSheet
from flask_login import current_user
from flask import Flask, make_response, request, redirect, render_template, url_for, jsonify


@app.route('/getsheetname/', methods=['GET', 'POST'])
def GetSheetName():
    "查询一个用户所有的表的名字"
    if request.method == 'POST':
        userid = current_user.id
        #lis = [{'text': "Choose one...", "value": "Choose one..."}]
        lis = []
        p = SongSheet.select().where(SongSheet.userid == userid)
        for i in p:
            lis.append({'text': i.sheet_name, "value": i.sheet_name})
        return make_response(jsonify(lis))


@app.route('/getsheet/', methods=['GET', 'POST'])
def GetSheet():
    "初始化用户首页时，前端向传递表单名，后端向前端传递歌单信息"
    if request.method == 'POST':
        userid = current_user.id
        sheet_name = request.form.get("sheet_name")
        lis = []
        try:
            p = SongSheet.get(SongSheet.userid == userid,
                              SongSheet.sheet_name == sheet_name)  # 查
        except:  #不存在该歌单，或是用户未登录
            pass
        if p.musiclist == "":
            pass
        else:
            teplist = p.musiclist.split('-')
            for i in teplist:
                p = Music.get(id=int(i))
                dic = {}
                dic['music_id'] = i.id
                dic['singer_name'] = i.singer_name
                dic['music_name'] = i.music_name
                dic['music_type'] = i.music_type
                dic['album_name'] = i.album_name
                dic["path"] = i.singer_name + ' - ' + i.music_name + '.' + i.music_type
                lis.append(dic)
        resp = make_response(jsonify(lis))
        print(resp)
        return resp


@app.route('/addsheet/', methods=['POST'])
def AddSheet():
    "某用户创建歌单，需传入歌单名(认为同一用户不能创建两个同名歌单)"
    if request.method == 'POST':
        userid = current_user.id
        sheet_name = request.form.get("sheet_name")
        #print("-----------------------")
        #print(username, "----", sheet_name)
        dic = {}
        try:  #同一个用户不能有同样名字的歌单
            SongSheet.get(SongSheet.userid == userid,
                          SongSheet.sheet_name == sheet_name)  # 查
        except:  #没查到,可以建立
            SongSheet(userid=userid, sheet_name=sheet_name).save()
            dic['isok'] = 1
        else:  #查到了,不能建立
            dic['isok'] = 0
        return make_response(jsonify(dic))


@app.route('/deletesheet/', methods=['POST'])
def DeleteSheet():
    "某用户删除歌单，需传入歌单名"
    if request.method == 'POST':
        userid = current_user.id
        sheet_name = request.form.get("sheet_name")
        dic = {}
        try:  #同一个用户不能有同样名字的歌单
            p = SongSheet.get(SongSheet.userid == userid,
                              SongSheet.sheet_name == sheet_name)  # 查
        except:  #没查到,没法删
            dic['isok'] = 0
        else:
            #用户名和表名必须同时对应，不然会误删
            SongSheet.delete().where(
                SongSheet.userid == userid,
                SongSheet.sheet_name == sheet_name).execute()
            dic['isok'] = 1
        return make_response(jsonify(dic))


@app.route('/addsong/', methods=['POST'])
def AddSong():
    "某用户在某首歌单中加入一首歌,需传入歌单名及歌曲id"
    if request.method == 'POST':
        userid = current_user.id
        sheet_name = request.form.get("sheet_name")
        music_id = request.form.get("music_id")
        dic = {}
        try:
            p = SongSheet.get(SongSheet.userid == userid,
                              SongSheet.sheet_name == sheet_name)  # 查
            Music.get(id=music_id)
        except:  #没找到对应歌单/歌曲
            dic['isok'] = 0
        else:
            dic['isok'] = 1
            if p.musiclist == '':  #空
                SongSheet.update({
                    SongSheet.musiclist: str(music_id)
                }).where(SongSheet.userid == userid,
                         SongSheet.sheet_name == sheet_name).execute()  # 改
            else:  #非空
                teplist = p.musiclist.split('-')
                if str(music_id) not in teplist:
                    teplist.append(str(music_id))
                    SongSheet.update({
                        SongSheet.musiclist: '-'.join(teplist)
                    }).where(SongSheet.userid == userid,
                             SongSheet.sheet_name == sheet_name).execute()  # 改
                else:
                    dic['isok'] = -1
        return make_response(jsonify(dic))


@app.route('/deletesong/', methods=['POST'])
def DeleteSong():
    "某用户在某首歌单中删除一首歌,需传入歌单名及歌曲id"
    if request.method == 'POST':
        userid = current_user.id
        sheet_name = request.form.get("sheet_name")
        music_id = request.form.get("music_id")
        dic = {}
        try:
            p = SongSheet.get(SongSheet.userid == userid,
                              SongSheet.sheet_name == sheet_name)  # 查
            Music.get(id=music_id)
        except:  #没找到对应歌单/歌曲
            dic['isok'] = 0
        if p.musiclist == '':  #歌单中元素为空
            dic['isok'] = -1
        else:
            dic['isok'] = 1
            teplist = p.musiclist.split('-')
            try:
                teplist.remove(str(music_id))
                SongSheet.update({
                    SongSheet.musiclist: '-'.join(teplist)
                }).where(SongSheet.userid == userid,
                         SongSheet.sheet_name == sheet_name).execute()  # 改
            except:  #teplist里面没有对应元素，没法删
                dic['isok'] = -1
        return make_response(jsonify(dic))
