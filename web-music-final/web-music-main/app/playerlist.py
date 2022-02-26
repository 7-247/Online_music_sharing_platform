from app.models import Music

playerlist = []  #播放列表


def initplayerlist():
    global playerlist
    playerlist.clear()
    Musics = Music.select().where(Music.id != '')  # 查全
    for i in Musics:
        dic = {}
        dic['music_id'] = i.id
        dic['singer_name'] = i.singer_name
        dic['music_name'] = i.music_name
        dic['music_type'] = i.music_type
        dic['album_name'] = i.album_name
        dic["path"] = i.singer_name + ' - ' + i.music_name + '.' + i.music_type
        playerlist.append(dic)


initplayerlist()
