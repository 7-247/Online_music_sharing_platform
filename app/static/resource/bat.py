import os

path = "lrc\\"
newpath = "lrc\\"
g = os.listdir(path)
code = {
    'utf-8': list(),
    'gbk': list(),
    'gb2312': list(),
    'ansi': list(),
    'utf-16': list()
}
err = open("error.log", mode='w', encoding='utf-8')
for i in g:
    print(i)
    for j in code:
        try:
            f = open(path + i, mode='r', encoding=j)
            k = f.read()
            #print(k)
        except Exception as e:
            err.write("{}\n{}\n{}\n\n\n".format(i, str(e), repr(e)))
        else:
            print("encoding = {}".format(j))
            code[j].append(g.index(i))
            p = open(newpath + i, mode='w', encoding='utf-8')
            p.write(k)
            p.close()
            break
        finally:
            f.close()
print(code)
