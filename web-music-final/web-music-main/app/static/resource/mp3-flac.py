from mutagen import File
from PIL import Image
import os

flacpath = "./flac/"
mp3path = "./mp3/"
coverpath = "./cover/"
cover = Image.open("默认封面.jpg")


def rename(srcFile, dstFile):
    try:
        os.rename(srcFile, dstFile)
    except Exception as e:
        print(e)
        print('rename file fail\r\n')
    else:
        print('rename file success\r\n')


def getflacinfo():
    teplist = os.listdir(flacpath)
    for i in teplist:
        path = flacpath + i
        afile = File(path)
        author = afile.tags["Artist"][0]  # 作者
        #print(author)
        title = afile.tags["Title"][0]  # 标题
        #print(title)
        album = afile.tags["Album"][0]  # 专辑
        #print(album)  # 专辑
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
        rename(srcFile, dstFile)


def getmp3info():
    teplist = os.listdir(mp3path)
    for i in teplist:
        path = mp3path + i
        afile = File(path)
        author = afile.tags["TPE1"].text[0]  # 作者
        #print(author)
        title = afile.tags["TIT2"].text[0]  # 标题
        #print(title)
        album = afile.tags["TALB"].text[0]  # 专辑
        #print(album)  # 专辑
        try:
            artwork = afile.tags["APIC:"].data
            with open(coverpath + author + ' - ' + title + '.jpg',
                      'wb') as img:
                img.write(artwork)  # write artwork to n
        except:
            cover.save(coverpath + author + ' - ' + title +
                       '.jpg')  #可以自己添加一张默认封面

        srcFile = path
        dstFile = mp3path + author + ' - ' + title + '.mp3'
        rename(srcFile, dstFile)


getflacinfo()
getmp3info()
