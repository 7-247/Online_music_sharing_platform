from app import models
from mutagen import File
from PIL import Image
import os

lrcpath = "./app/static/resource/lrc/"
flacpath = "./app/static/resource/flac/"
mp3path = "./app/static/resource/mp3/"
coverpath = "./app/static/resource/cover/"
cover = Image.open("./app/static/resource/默认封面.jpg")


def rename(srcFile, dstFile):
    #print(srcFile, "------", dstFile)
    if srcFile == dstFile:
        return
    os.rename(srcFile, dstFile)
    '''
    try:
        os.rename(srcFile, dstFile)
    except Exception as e:
        print(str(e), repr(e), sep='\n')
        print('rename file fail\r\n')
    else:
        print('rename file success\r\n')
    '''


def formatname(string):
    list = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for i in list:
        string = string.replace(i, '_')
    return string


def getflacinfo():
    teplist = os.listdir(flacpath)
    for i in teplist:
        path = flacpath + i
        afile = File(path)
        author = afile.tags["Artist"][0]  # 作者
        author = formatname(author)
        title = afile.tags["Title"][0]  # 标题
        title = formatname(title)
        album = afile.tags["Album"][0]  # 专辑
        #print(album)  # 专辑
        try:
            models.Music.get(models.Music.singer_name == author,
                             models.Music.music_name == title,
                             models.Music.album_name == album)
        except:  #未找到
            models.Music(singer_name=author,
                         music_name=title,
                         music_type='flac',
                         album_name=album).save()
            try:
                artwork = afile.pictures[0].data
                with open(coverpath + author + ' - ' + title + '.jpg',
                          'wb') as img:
                    img.write(artwork)  # write artwork to n
            except:
                cover.save(coverpath + author + ' - ' + title + '.jpg')
                #可以自己添加一张默认封面

            srcFile = path
            dstFile = flacpath + author + ' - ' + title + '.flac'
            try:
                rename(srcFile, dstFile)  #歌曲重命名
            except:  #去重
                os.remove(dstFile)
                rename(srcFile, dstFile)  #歌曲重命名

            try:
                rename(lrcpath + i[:-5] + ".lrc",
                       lrcpath + author + ' - ' + title + ".lrc")  #歌词重命名
            except:
                pass


def getmp3info():
    teplist = os.listdir(mp3path)
    for i in teplist:
        path = mp3path + i
        afile = File(path)
        author = afile.tags["TPE1"].text[0]  # 作者
        author = formatname(author)
        title = afile.tags["TIT2"].text[0]  # 标题
        title = formatname(title)
        album = afile.tags["TALB"].text[0]  # 专辑
        #print(album)  # 专辑
        try:
            models.Music.get(models.Music.singer_name == author,
                             models.Music.music_name == title,
                             models.Music.album_name == album)
        except:  #未找到
            models.Music(singer_name=author,
                         music_name=title,
                         music_type='mp3',
                         album_name=album).save()
            try:
                artwork = afile.tags["APIC:"].data
                with open(coverpath + author + ' - ' + title + '.jpg',
                          'wb') as img:
                    img.write(artwork)  # write artwork to n
            except:
                cover.save(coverpath + author + ' - ' + title +
                           '.jpg')  #可以自己添加一张默认封面

            srcFile = path
            dstFile = mp3path + author + ' - ' + title + '.mp3'  # 命名规则： 歌手名 - 歌曲名
            try:
                rename(srcFile, dstFile)  #歌曲重命名
            except:  #去重
                os.remove(dstFile)
                rename(srcFile, dstFile)  #歌曲重命名
            try:
                rename(lrcpath + i[:-4] + ".lrc",
                       lrcpath + author + ' - ' + title + ".lrc")  #歌词重命名
            except:
                pass


if models.Music.table_exists():
    models.Music.drop_table()  #先删表
models.Music.create_table()
getflacinfo()
getmp3info()

from app.playerlist import initplayerlist


def initdatabase():
    if models.Music.table_exists():
        models.Music.drop_table()  #先删表
    models.Music.create_table()
    getflacinfo()
    getmp3info()
    initplayerlist()


'''
def GetMusicInfo(s):
    type = s.split('.')[-1]
    u = s.rstrip('.' + type).split(' - ')
    return (u[0], u[1], type)
# 命名规则： 歌手名 - 歌曲名
musicstr = os.listdir(mp3path) + os.listdir(flacpath)  # 获取歌曲/歌手名字
for i in musicstr:
    tep = GetMusicInfo(i)
    models.Music(singer_name=tep[0], music_name=tep[1],
                     music_type=tep[2]).save()
'''
