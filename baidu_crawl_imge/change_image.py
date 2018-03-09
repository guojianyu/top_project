from PIL import Image
import os
from resizeimage import resizeimage

# 1024 x 682
def change_size(image_doc):
    pathDir = os.listdir(image_doc)#查看目录下的所有文件
    before_dir = os.path.dirname(image_doc)
    #print (os.path.dirname(image_doc))#上一层目录
    #print(os.path.split(image_doc)[-1])#当前目录名称
    new_dir = os.path.split(image_doc)[-1]+'new'
    new_size_dir = os.path.join(before_dir,new_dir)
    if not os.path.exists(new_size_dir):
        os.mkdir(new_size_dir)
    for item in pathDir[0:2]:
        with open(os.path.join(image_doc,item), 'r+b') as f:
            with Image.open(f) as image:
                cover = resizeimage.resize_contain(image, [800, 600])
                cover = cover.convert("RGB")
                cover.save(os.path.join(new_size_dir,item))
if __name__ == '__main__':
    change_size('C:/untitled/baidu_crawl_image/肝病/肝')