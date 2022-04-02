#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import re
from app.models import Music


def fuzzyfinder(user_input, collection):
    suggestions = []
    pattern = '.*?'.join(user_input)  # e.g. 'abc' -> 'a.*?b.*?c'
    for item in collection:
        match = re.search(pattern, item[1], re.I)  # 歌曲名
        if match:
            suggestions.append(item)
        match = re.search(pattern, item[2], re.I)  # 歌手名
        if match:
            suggestions.append(item)
        match = re.search(pattern, item[4], re.I)  #专辑名
        if match:
            suggestions.append(item)
    teplis = list(set(suggestions))  #去重
    teplis.sort(key=lambda x: x[0])  #排序
    return teplis


def find(inputstr):
    "找遍歌手名、歌曲名，模糊查询，返回一个四元组(id,music_name,singer_name,music_type)"
    collections = []
    Musics = Music.select().where(Music.id != '')  # 查全
    for i in Musics:
        collections.append(
            (i.id, i.music_name, i.singer_name, i.music_type, i.album_name))
    return fuzzyfinder(inputstr, collections)
