#fuck volmoe

import os
import zipfile
from bs4 import BeautifulSoup

files = os.listdir(".")
# print(type(files))

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print("新建目录:", path)
    if folder:
        print("已有目录:", path)


for filename in files:
    portion = os.path.splitext(filename) 

    # 如果后缀是.epub
    if portion[1] == ".epub": 
        
        folder_path = ("./" + portion[0])
        mkdir(folder_path)

        z = zipfile.ZipFile(portion[0]+".epub", "r")
        html_name = []
        image_name = []
        #打印zip文件中的文件列表
        for filename in z.namelist( ):
            if "html/" in filename:
                html_name.append(filename)
                # if "cover" in filename:
                #     html_name.append(filename)
                # elif ("0","1","2","3","4","5","6","7","8","9") in filename:
                #     html_name.append(filename)
            if "image/" in filename:
                image_name.append(filename) 
        html_name.sort()
        print("html:",len(html_name))
        print(portion[0],"中的image数量:",len(image_name))
        # print(image_name)

        try:
            #读取zip文件中的文件
            for i in html_name:

                content = z.read(i)

                # print(content)
                # print(type(content))

                soup = BeautifulSoup(z.read(i),features='html.parser')  #features值可为lxml

                main_div = soup.find('div',{'class': 'fs'})
                img = main_div.find("img")
                img_url = img.get("src")
                img_url = img_url[3:]
                # print("img_url:",img_url)

                # print(type(("./" + folder_path + "已处理/" + img_url)))
                

                # z.extract(img_url, path = folder_path)
                z.extract(img_url, path = folder_path)
                if "cover" in i:
                    newname = i[5:]
                else: 
                    newname = i[5:-5]
                    if len(newname) <= 4:
                        newname = "0"*(4-len(newname)) + newname

                os.rename((folder_path +"/"+ img_url), folder_path + "/" + newname + ".jpg")
                # print("已完成:", newname)
        except KeyError:
            pass

