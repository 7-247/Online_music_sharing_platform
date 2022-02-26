from app.music import initdatabase
from app.find import find
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import SongSheet, User, Music
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from datetime import datetime
from app.forms import EditProfileForm
from app import login
from app.playerlist import playerlist


@login.user_loader
def load_user(id):
    try:
        user = User.get(User.id == id)  # 查
    except:
        user = None
    return user


@app.route("/", methods=['GET', 'POST'])
def rootindex():
    return redirect(url_for('index'))  # 重定向


@app.route('/index', methods=['GET', 'POST'])
# 这样，必须登录后才能访问首页了,会自动跳转至登录页
def index():
    if request.method == 'POST':
        searchname = request.form.get("search_content")
        tep = find(searchname)
        searchres = []
        for i in tep:
            dic = {}
            dic['music_id'] = i[0]
            dic['music_name'] = i[1]
            dic['singer_name'] = i[2]
            dic['music_type'] = i[3]
            dic['album_name'] = i[4]
            dic["path"] = i[2] + ' - ' + i[1] + '.' + i[3]
            searchres.append(dic)
        return render_template("index.html", Musics=searchres)
    return render_template('index.html', Musics=playerlist)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    # 对表格数据进行验证
    if form.validate_on_submit():
        # 根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
        try:
            user = User.get(User.username == form.username.data)  # 查
        except:
            flash('无效的用户名,请检查输入或注册')
            # 然后重定向到登录页面
            return redirect(url_for('login'))
        # 查到了，判断密码
        if not user.check_password(form.password.data):
            # 如果用户不存在或者密码不正确就会闪现这条信息
            flash('密码错误')
            # 然后重定向到登录页面
            return redirect(url_for('login'))

        # 这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        login_user(user, remember=form.remember_me.data)
        # 此时的next_page记录的是跳转至登录页面是的地址
        next_page = request.args.get('next')
        # 如果next_page记录的地址不存在那么就返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


import requests


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        namefound = True
        emailfound = True
        try:
            User.get(User.username == form.username.data)
        except:
            namefound = False
        try:
            User.get(User.email == form.email.data)
        except:
            emailfound = False
        if namefound == False and emailfound == False:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            user.save()
            url = user.avatar(256)
            strhtml = requests.get(url)  #Get方式获取网页数据
            with open("./app/static/resource/headpic/" + str(user.id) + '.jpg',
                      'wb') as fw:
                fw.write(strhtml.content)

            flash('恭喜你成为我们网站的新用户!')
            return redirect(url_for('login'))
        else:
            flash('该用户名或邮箱已被注册!')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)


# 设置允许的文件格式
ALLOWED_EXTENSIONS_PIC = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'BMP'])
ALLOWED_EXTENSIONS_MUSIC = set(['mp3', 'flac', 'MP3', 'FLAC'])


def allowed_file(filename, type):
    return '.' in filename and filename.rsplit('.', 1)[1] in type


import os
from PIL import Image


@app.route('/user/', methods=['GET', 'POST'])
@login_required
def user():
    if request.method == 'POST':
        f = request.files['musicfile']
        if not (f and allowed_file(f.filename, ALLOWED_EXTENSIONS_MUSIC)):
            flash("请上传合适的文件！")
        else:
            path = "./app/static/resource/" + f.filename.rsplit(
                '.', 1)[1] + "/" + f.filename
            f.save(path)
            initdatabase()

    lists = []
    tepuser = User.get(User.username == current_user.username)  # 查
    posts = SongSheet.select().where(SongSheet.userid == current_user.id)
    for i in posts:
        newdic = []
        newdic.append(i.sheet_name)
        if i.musiclist == "":
            newdic.append('')
        else:
            teplist = i.musiclist.split("-")
            searchres = []
            print(teplist)
            for j in teplist:
                dic = {}
                dic['music_id'] = j
                p = Music.get(id=j)
                dic['music_name'] = p.music_name
                dic['singer_name'] = p.singer_name
                dic['music_type'] = p.music_type
                dic['album_name'] = p.album_name
                dic["path"] = p.singer_name + ' - ' + p.music_name + '.' + p.music_type
                searchres.append(dic)
            newdic.append(searchres)
        lists.append(newdic)

    return render_template('user.html',
                           user=tepuser,
                           posts=lists,
                           posts_len=len(lists))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        current_user.save()  # db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            User.get(User.username == form.username.data)
        except:
            current_user.username = form.username.data
            current_user.about_me = form.about_me.data
            current_user.save()
            flash('您的提交已变更.')
            return redirect(url_for('edit_profile'))
        if current_user.username == form.username.data:
            current_user.about_me = form.about_me.data
            current_user.save()
            flash('您的提交已变更.')
            return redirect(url_for('edit_profile'))
        else:
            flash("该用户名已被注册!")
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='个人资料编辑', form=form)


@app.route('/upload_pic', methods=['GET', 'POST'])
@login_required
def upload_pic():
    form = EditProfileForm()
    if request.method == 'POST':
        print(request.files)
        f = request.files['picfile']
        if not (f and allowed_file(f.filename, ALLOWED_EXTENSIONS_PIC)):
            flash("请上传合适的文件！")
        else:
            path = "./app/static/resource/headpic/" + str(
                current_user.id) + '.' + f.filename.rsplit('.', 1)[1]
            f.save(path)
            im = Image.open(path).resize((256, 256)).convert('RGB')
            os.remove(path)
            im.save("./app/static/resource/headpic/" + str(current_user.id) +
                    '.jpg')  #以用户id.jpg保存在headpic文件夹中
            flash('您的提交已变更.')
    return redirect(url_for('edit_profile'))