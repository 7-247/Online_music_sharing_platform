import hashlib
from cv2 import VideoCapture
from moviepy.editor import *
import os
'''
dir_paths = os.path.join(os.path.dirname(os.path.abspath(__file__)),'files')

files = os.listdir(dir_paths)

for file in files:
'''
dir_paths = "C:\\Users\\111\\Desktop\\"
file = "结果展示.mp4"
file_ext = str(os.path.splitext(file)[-1]).lower()
file_name = os.path.join(dir_paths, file)
clip = VideoFileClip(file_name)
v_len = clip.duration
if v_len > 10:
    v_len = 6
if v_len < 3:
    zoom = 0
elif 3 <= v_len <= 5:
    zoom = 1
elif 5 < v_len < 7:
    zoom = 2.7
else:
    zoom = 3
# zoom = 2
cap = VideoCapture(file_name)
# 获取视频信息
zoom = 0
if zoom > 0:
    content = clip.subclip(0, v_len).resize(
        (int(cap.get(3) / zoom), int(cap.get(4) / zoom)))  # 修改分辨率
else:
    content = clip.subclip(0, v_len)  # 不修改分辨率
# 导出GIF
md5 = hashlib.md5()
md5.update(file_name.encode(encoding='utf-8'))
gif_name = md5.hexdigest() + '.gif'
content.write_gif(os.path.join(dir_paths, gif_name))
del (clip, cap, md5)
