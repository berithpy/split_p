# ����ͼƬ�ָ�

һ����ԣ�������������������������ҳ����ɨ��ģ�����

![whaever](/raw/master/original.jpg "original image")

�Ķ������ǳ������㡣���Ǿ�������ôһ����ͼƬ�ֿ��Ĺ��ߡ�֮��ͱ������ͼ��:

![whatever](/raw/master/splitted_1.jpg  "splitted image 1")

![whatever](/raw/master/splitted_2.jpg "splitted image 1")

### ʹ��
�ű�������������¡��Լ���comicdir�滻�ɱ��������ĸ�Ŀ¼·�����ɡ�
��������Ķ���ʽ�Ǵ������ң���Ϊ`mode=LEFT2RIGHT`

	comicdir = ''
    main(comicdir, mode)

# Image split for manga reading

Downloaded manga usually contains two pages in one image,which makes painful reading.This tool separate the original images.

### How to use
Open the `split.py` file, custom the last two lines.

You should fill `comicdir` with your own comic directory.Note that if left part of the original image precedes the right part, you should change `mode` to `LEFT2RIGHT`.