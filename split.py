# coding:utf-8
"""
输入图片根目录录复制出一个完整的文件夹及子文件夹
假定漫画的存储结构如下
学园默示录
    第一话
        一堆jpg
    第二话
        一堆jpg
这样不会有更多层的目录.这个假设暂时看来是合理的
如果图片本身height就大于width,那么就改变原图
需要注意图片排版是从左到右还是从右到左,默认为RIGHT2LEFT
"""

import os
import re
import sys

from glob import glob

from PIL import Image, ImageFile


def getThreeDigit(num):
    #将漫画的页码规范为3位数显示，返回字符串，比'1'->'001','21'->'021'zz
    if len(str(num)) >= 3:
        return str(num)
    else:
        if num < 10: 
            return '00' + str(num)
        elif num > 9 and num < 100:
            return '0' + str(num)
        elif num > 99:
            return str(num)
        else:
            return False


def main(comicdir, mode, page_count):
    """入口函数"""
    (head,comicname) = os.path.split(comicdir)
    new_root = comicname + '_split'
    if not os.path.exists('%s\%s' % (head,new_root)):
        os.mkdir('%s\%s' % (head,new_root))
    
    #创建文件夹结构
    for _,subdirs,_ in os.walk(comicdir):
        for subdir in subdirs:
            if not os.path.exists('%s\%s\%s' % (head,new_root,subdir)):
                os.mkdir('%s\%s\%s' % (head,new_root,subdir))
    
    # 处理图片并保存到之前创建的文件夹结构
    types = ('*.jpg', '*.png',) # 支持的文件类型,可添加
    pics = []
    
    # glob会将[..]认为是匹配方括号中出现的字符,所以需要改为'['->'[[]',']'->'[]]'
    comicdir = re.sub(r'(?P<squarebracket>\[|\])', '[\g<squarebracket>]', comicdir)
    for type in types:
        pics.extend(glob(r'%s\%s' % (comicdir, type)))  # 不再使用生成器,直接用List
        pics.extend(glob(r'%s\*\%s' % (comicdir, type)))
        
    num_all = len(pics)
    num_split = 0

    for pic in pics:
        """ 找出图片的数字序号 """
        # from http://stackoverflow.com/questions/12984426/python-pil-ioerror-image-file-truncated-with-big-images
        # solves IOError: image file is truncated (2 bytes not processed).
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        try:
            image = Image.open(pic)
        except OSError:
            continue  # some pics are not downloaded correctly and has 0 size thus causing OSError
        size = image.size   # size = (width,height)
        width = size[0]
        height = size[1]
        
        if width > height:  # do split
            number = list(re.finditer(r"\d+", pic))[-1]  # match last occurence of \d+
            p_ID = number.group()
            start = number.start()
            end = number.end()
            
            if page_count == 'absolute':
                if mode == 'RTL':
                    p_ID_left = str(getThreeDigit(int(p_ID)*2))
                    p_ID_right = str(getThreeDigit(int(p_ID)*2-1))
                elif mode == 'LTR':
                    p_ID_left = str(getThreeDigit(int(p_ID)*2-1))
                    p_ID_right = str(getThreeDigit(int(p_ID)*2))
            elif page_count == 'relative':
                if mode == 'RTL':
                    p_ID_left = str(getThreeDigit(int(p_ID)+1))
                    p_ID_right = str(getThreeDigit(int(p_ID)))
                elif mode == 'LTR':
                    p_ID_left = str(getThreeDigit(int(p_ID)))
                    p_ID_right = str(getThreeDigit(int(p_ID)+1))
                
            save_left_dir = pic[:start] + p_ID_left + pic[end:]
            save_right_dir = pic[:start] + p_ID_right + pic[end:]
            save_left_dir = save_left_dir.replace(comicname, new_root, 1)
            save_right_dir = save_right_dir.replace(comicname, new_root, 1)
            
            left_image_box = (0, 0, int(width/2), height)
            right_image_box = (int(width/2), 0, width, height)
            left_image = image.crop(left_image_box)
            right_image = image.crop(right_image_box)
            left_image.convert('RGB').save(save_left_dir,'jpeg')
            right_image.convert('RGB').save(save_right_dir,'jpeg')
        else:  # 直接保存进新的路径即可
            save_dir = pic.replace(comicname, new_root, 1)
            image.convert('RGB').save(save_dir,'jpeg')
        num_split += 1
        if not num_split % 100:
            print('Pages Split: %s/%s' % (num_split,num_all))
        
    
if __name__ == '__main__':
    if len(sys.argv) == 4:
        comicdir = sys.argv[1]
        mode = sys.argv[2]
        page_count = sys.argv[3]
    elif len(sys.argv) == 3:
        comicdir = sys.argv[1]
        mode = sys.argv[2]
        page_count = 'absolute'
    elif len(sys.argv) == 2:
        comicdir = sys.argv[1]
        mode = 'RTL'
        page_count = 'absolute'
    elif len(sys.argv) == 1:
        print("You need to provide the manga path as an argument.\ne.g. split.py ~/Documents/manga")
        exit(0)
    else:
        print("Too many arguments.")
        exit(0)

    main(comicdir, mode, page_count)
