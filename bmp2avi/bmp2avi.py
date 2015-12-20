# -*- coding: utf-8 -*-

import cv2
import numpy as np
import sys
import os
import shutil
import Image


def bmp2avi(path_dir, target_dir, remake=False):
    if not os.path.isdir(path_dir):
        print "Error 1"
        return
    if not path_dir.endswith("/"):
        path_dir += "/"

    if not os.path.isdir(target_dir):
        print "Error 2"
        return
    if not target_dir.endswith("/"):
        target_dir += "/"

    files = os.listdir(path_dir)
    if len(files) == 0:
        print "Error 3"
        return 
    if not os.path.isfile(path_dir+files[0]):
        print "Error 4"
        return
    if not files[0].endswith(".BMP"):
        print "Error 5"
        return

    print "Check:"+path_dir+"log.txt"
    xc=[]
    yc=[]
    lockon_num     = " 0"
    lockon_num_pre = " 0"
    if os.path.exists(path_dir+"log.txt" ) :
        f=open(path_dir+"log.txt","r")
        strlist = f.readlines()
        for line in strlist:
            lockon_num_pre = lockon_num
            lockon_num = line.split( "](" )[1][20:22]
            if lockon_num==" 1" and lockon_num_pre == " 0" :
                xc.append(int(line.split( "](" )[1][0:3]))
                yc.append(int(line.split( "](" )[1][4:7]))
        
        for i in range(0,len(xc)):
            print "(xc,yc)["+str(i)+"]=("+str(xc[i])+","+str(yc[i])+")"
        
        f.close()

    # 2度目のavi化は行わない
    print "Check:"+path_dir+"avi_make_ended.txt"
    if os.path.exists(path_dir+"avi_make_ended.txt" ) and remake==False :
        print "avi_make_ended.txt exist!!"
        return

    img1 = cv2.imread(path_dir+files[0])
    height , width , layers =  img1.shape
    filename     = target_dir+"/"+files[0][4:].split(".")[0]+'_00.avi'
    filename_log = target_dir+"/"+files[0][4:].split(".")[0]+'_00t.txt'
    if os.path.exists( filename ) :
        os.remove( filename )
        #return
    if os.path.exists( filename_log ) :
        os.remove( filename_log )
        #return
    fourcc = cv2.cv.CV_FOURCC('D', 'I', 'B', ' ')
    #fourcc = cv2.cv.CV_FOURCC('I', '4', '2', '0')
    #fourcc = cv2.cv.CV_FOURCC('D', 'I', 'V', 'X')
    video = cv2.VideoWriter(filename, fourcc,30,(width,height))
    #video = cv2.VideoWriter(filename, cv2.cv.CV_FOURCC('H', 'Y', 'M', 'T'),30,(width,height))
    #video = cv2.VideoWriter(filename, cv2.cv.CV_FOURCC('U', 'L', 'Y', '0'),30,(width,height))
    #video = cv2.VideoWriter(filename, cv2.cv.CV_FOURCC('L', 'A', 'G', 'S'),30,(width,height))
    #video = cv2.VideoWriter(filename, cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'),30,(width,height))

    cv2.namedWindow('BMP2AVI')
    ft=[]
    for fn in files:
        ft.append( fn[4:] )
    dic = dict(zip(ft,files))

    # key値でソート
    for k, fn in sorted(dic.items()):
        print k, fn
    
        if fn.endswith(".BMP") :
            img = cv2.imread(path_dir+fn)
            for i in range(0,len(xc)):
                cv2.circle(img,(xc[i],yc[i]),25-i,(255-5*i,255-5*i,0))
            cv2.imshow('BMP2AVI', img)
            video.write(img)
        
            cv2.waitKey(20)
        if fn == "log.txt":
            shutil.copyfile(path_dir+fn, filename_log)
            
    cv2.destroyAllWindows()
    video.release()

    print "Output:",filename
    
    #avi作成済み目印
    f=open(path_dir+"avi_make_ended.txt","w")
    f.close()
    print path_dir+"avi_make_ended.txt"

#def fname(main_dir) :
#    files = os.listdir(main_dir)
#
import zipfile
def fish_dir_org(main_dir):
    fdir=[]
    fjpg=[]
    flog=[]
    zf = zipfile.ZipFile('sample.zip', 'w', zipfile.ZIP_DEFLATED)
    files = os.listdir(main_dir)
    for f in files :
        print len(f), f
        if len(f) == 5 :
            fdir.append(main_dir + f )
        elif f.endswith(".JPG") :
            fjpg.append( main_dir + f )
        else :
            flog.append( f )
            zf.write( main_dir + f )
    # ログファイル作成        
    zf.close()
    
    
    for fd in fdir :
        bmp2avi( fd )
    
#    for f in fjpg :
    
    print zf
#    print fjpg
#    print flog

def fish_dir(main_dir, t_dir, remake=False):
    print "fish_dir() "+main_dir , t_dir
    if not os.path.isdir(main_dir):
        print "Error 1 fish_dir()"
        return
    if not main_dir.endswith("/"):
        main_dir += "/"

    if not os.path.isdir(t_dir):
        print "Error 2 fish_dir()"
        return
    if not t_dir.endswith("/"):
        t_dir += "/"

    fdir=[]
    fjpg=[]
    flog=[]
#    zf = zipfile.ZipFile('sample.zip', 'w', zipfile.ZIP_DEFLATED)
    files = os.listdir(main_dir)
    for f in files :
#        print len(f), f
        if len(f) == 5 :
            fdir.append(main_dir + f )
        elif f.endswith(".JPG") :
            fjpg.append( main_dir + f )
        else :
            flog.append( f )
#            zf.write( main_dir + f )
    # ログファイル作成        
#    zf.close()
    
    
    for fd in fdir :
        print fd,t_dir
        bmp2avi( fd, t_dir, remake )

if __name__ == '__main__':
           
    #main_dir = './fish1/'
    #t_dir = './'
    #fish_dir(main_dir, t_dir)

    #指定する画像フォルダ
    path_dir ='C:/temp/tmp/14368/'
    target_dir ='C:/temp/'
    bmp2avi(path_dir,target_dir)
