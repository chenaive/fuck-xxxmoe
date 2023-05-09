# %%
#fuck volmoe
import os
import zipfile
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
#导入库

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        # print("新建目录:", path)
    if folder:
        pass
        # print("已有目录:", path)

#读取文件列表
files = os.listdir(".")
# epublist=[]
#     
for filename in files:
    portion = os.path.splitext(filename) 
    if portion[1] == ".epub": 
        # epublist.append(portion[0])
        folder_path = ("./" + portion[0])

        if folder_path[-5:] == "kepub":
            folder_path = folder_path[:-6]
            
        mkdir(folder_path) #新建目录

        z = zipfile.ZipFile(portion[0]+".epub", "r")
        for filename in z.namelist():
            if os.path.splitext(filename)[1] == ".opf":
                vol_opf = filename
            if os.path.splitext(filename)[1] == ".ncx":
                vol_ncx = filename
        
# print("list:",epublist)

            # content = z.read(vol_opf)
            # soup = BeautifulSoup(content, features='xml')  #features值可为lxml html.parser
            # main_div = soup.find_all("item",{'id':'Page_1'})
            # print((main_div))

            # for html in main_div:
            #     print(html["href"])

        content = z.read(vol_ncx)
        soup_html = BeautifulSoup(content, features='xml')  #features值可为lxml html.parser
        main_div = soup_html.find_all("content")

        html_list = []

        for html in main_div:
            html_address = html["src"][3:]
            # print(html_address)
            html_list.append(html_address)
        # print(html_list)
        num = 1

        try:
            z.extract("image/cover.jpg", path = folder_path)
            os.replace((folder_path +"/image/cover.jpg"), (folder_path + "/cover.jpg"))
            for i in html_list:
                img_url = BeautifulSoup(z.read(i), features='xml').find('div',{'class': 'fs'}).find("img").get("src")[3:]
                # print(img_url)
                format = os.path.splitext(img_url)[1] #.jpg

                z.extract(img_url, path = folder_path)
                if "cover" in img_url:
                    name = "cover"
                elif "createby" in img_url:
                    name = "createby"
                else: 
                    name = str(num)
                    if len(name) <= 4:
                        name = "0"*(4-len(name)) + name
                    num = num + 1

                os.replace((folder_path +"/"+ img_url), folder_path + "/" + name + format)
                os.rmdir(folder_path + "/image")
        except KeyError:
            pass

# %%



