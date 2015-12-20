# -*- coding: utf-8 -*-

import os
import sys
import datetime
import shutil
import time
import cr2_file_move
import bmp2avi

#---------------------------------------------------
# 00002_ .avi �t�@�C�����ύX
# datedir -> yyyymmdd
#
def proc_00002_rename(BaseSoucePath,dir):
    datedir = dir.replace("/","")
    # �����m�F
    if os.path.exists(BaseSoucePath) == False:
        print "Base Souce path '%s' not exists!" % BaseSoucePath
        return BaseSoucePath

    # src list up
    SoucePath = BaseSoucePath+"/"+datedir
    FileList = os.listdir(SoucePath)
    for f in FileList:
        if (f.find("00002_") > -1 and f.find(".avi") > -1 ) :
            fn=f.replace("00002_","")
            fn=fn.replace(".avi","_002.avi")
            src = SoucePath +"/"+ f
            dst = SoucePath +"/"+ fn
            os.rename(src, dst)
    # dir move        
    FileList = os.listdir(SoucePath)
    for f in FileList:
        fdate=f.split("_")[0]
        if ( len(fdate)==8 and fdate.isdigit() and fdate != datedir) :
            SPath = BaseSoucePath+"/"+datedir+"/"+f
            TPath = BaseSoucePath+"/"+fdate
            if os.path.exists(TPath) == False:
                os.makedirs(TPath)
            # _00.avi�@�Ȃ�@�폜
            if ( f.find("_00.avi")>-1 or f.find("_00t.txt")>-1) and os.path.exists( TPath+"/"+f ) :
                print "remove:"+TPath+"/"+f
                os.remove( TPath+"/"+f )

            try:
                print SPath + " -> " +TPath
                shutil.move(SPath, TPath)
            except OSError:
                print 'no such file'

#---------------------------------------------------
# avi �t�@�C���R�s�[
def proc_move(SoucePath,TargetPath,Extension=".avi"):
    # �����m�F
    if os.path.exists(SoucePath) == False:
        print "Souce path '%s' not exists!" % SoucePath
        return SoucePath
        
    if os.path.exists(TargetPath) == False:
        os.makedirs(TargetPath)

    # src list up
    FileList = os.listdir(SoucePath)
    for f in FileList:
        print f
        if (f.find(Extension) > -1) :
            src = SoucePath +"/"+ f
            dst = TargetPath +"/"+ f
            if os.path.exists(dst):
                print "Destination path '%s' already exists!" % dst
            else:
                try:
                    print src + " -> " +TargetPath
                    shutil.move(src, TargetPath)
                except OSError:
                    print 'no such file'

    print 'Complete!!!'
#---------------------------------------------------
# FishEye �f�B���N�g���R�s�[
def proc_dir_move(SoucePath,TargetPath):
    # �����m�F
    if os.path.exists(TargetPath) == False:
        os.makedirs(TargetPath)

    if os.path.exists(SoucePath) == False:
        print "Souce path '%s' not exists!" % SoucePath
        return SoucePath

    # src list up
    FileList = os.listdir(SoucePath)
    for f in FileList:
        print f
        src = SoucePath +"/"+ f
        if  os.path.isdir(src) :
            dst = TargetPath +"/"+ f
            proc_move(src,dst,".BMP") #AFP Fish data
            proc_move(src,dst,".txt") #AFP Fish data
            
    print 'MoveDir Complete!!!!'
#---------------------------------------------------
# ��f�B���N�g���̍폜
def proc_dir_remove(TargetPath):
    # dir list up
    #dirList = os.listdir(TargetPath)
    #for f in dirList:

    # �����m�F
    if os.path.exists(TargetPath) == True :
        try:
            os.removedirs(TargetPath)

        except WindowsError:
            print 'Data exist:'+str(TargetPath)
            #break
            
        except Exception as e:
            print '=== �G���[(proc_dir_remove) ==='
            print 'type:' + str(type(e))
            print 'args:' + str(e.args)    
            print 'message:' + e.message    
            print 'e���g:' + str(e)
            
#---------------------------------------------------
# avi �t�@�C���R�s�[
def mt3filemove(dt = datetime.datetime.now()):
    dir = dt.strftime("/%Y%m%d")
    print dt,dir
    
#    TargetPath1 = "J:/MT"+dir+"/MT3" #2014 8 11���ɕύX

    BaseSoucePath = "J:/MT"
    TargetPath1 = "J:/MT"+dir
    TargetPath2 = "J:/MT"+dir+"/Fish1"
    SoucePath1 = "T:"+dir
    SoucePath2 = "U:/public/piccolo"+dir
    SoucePath3 = "R:"+dir
    SoucePath4 = "V:"+dir
    SoucePath5 = "W:"+dir
    SoucePath6 = "X:"+dir
    SoucePath7 = "T:"+dir
    SoucePath8 = "Y:"+dir

    # fishdata
    proc_move(SoucePath3,TargetPath1) #SpCam mon SC440
    proc_move(SoucePath3,TargetPath2,".JPG") #AFP Fish data
    proc_move(SoucePath3,TargetPath2,".txt") #AFP Fish data
    proc_move(SoucePath3,TargetPath2,".log") #AFP Fish data
    proc_dir_move(SoucePath3,TargetPath2) #AFP Fish data
    bmp2avi.fish_dir(TargetPath2, TargetPath1)

    # other cam
    proc_move(SoucePath6,TargetPath1) #MT3 TX100S3 (Wide)
    proc_move(SoucePath2,TargetPath1) #MT3 TX100S3 (SpCam)
    proc_move(SoucePath7,TargetPath1) #MT3 I5-3450(Fine) 
    proc_move(SoucePath4,TargetPath1) #MT3 I5-3450(SF)
    proc_move(SoucePath1,TargetPath1) #MT3 I5-3450(PV)
    proc_move(SoucePath5,TargetPath1) #Train Liva1 
    proc_move(SoucePath8,TargetPath1) #MT3 MJ34LL(Fine2) 
    

    #�w�肷��摜�t�H���_

    TargetPath100 = "J:/MT"
    SoucePath100  = "J:/DCIM/100EOS5D/"
    dev_id="12"
    cr2_file_move.proc_cr2_move(SoucePath100,TargetPath100,dev_id)

    SoucePath101  = "J:/DCIM/101EOS5D/"
    cr2_file_move.proc_cr2_move(SoucePath101,TargetPath100,dev_id)

    SoucePath102 = "J:/SpCam/DCIM/100EOS5D/"
    dev_id="20"
    cr2_file_move.proc_cr2_move(SoucePath102,TargetPath100,dev_id)
    
    # 00002_�̃t�@�C�����ύX��A�N�����f�B���N�g���ɍĐU�蕪��
    proc_00002_rename(BaseSoucePath,dir)
    
#---------------------------------------------------
# main
# ���t�w��   
if __name__ == "__main__":
    dtnow = datetime.datetime.now()
    drange=1 #���s�����i�߂�����j
    if len( sys.argv )   >= 5:
        yyyy=int(sys.argv[1])
        mm  =int(sys.argv[2])
        dd  =int(sys.argv[3])
        drange =int(sys.argv[4])
    elif len( sys.argv ) == 4:
        yyyy=int(sys.argv[1])
        mm  =int(sys.argv[2])
        dd  =int(sys.argv[3])
    elif len( sys.argv ) == 3:
        yyyy=dtnow.year
        mm  =int(sys.argv[1])
        dd  =int(sys.argv[2])
    elif len( sys.argv ) == 2:
        yyyy=dtnow.year
        mm  =dtnow.month
        dd  =int(sys.argv[1])
    elif len( sys.argv ) == 1:
        yyyy=dtnow.year
        mm  =dtnow.month
        dd  =dtnow.day
        drange =7
    
    if yyyy < 2000 or yyyy > dtnow.year :
        print "Year '%s' �͈͊O" % yyyy
        sys.exit()

    if mm < 1 or mm > 12 :
        print "Month '%s' �͈͊O" % mm
        sys.exit()
    
    if dd < 1 or dd > 31 :
        print "Day '%s' �͈͊O" % dd
        sys.exit()

    if drange < 1 or drange > 365 :
        print "Drange '%s' �͈͊O" % drange
        sys.exit()
    
    for i in range(drange):
        dt = datetime.date(yyyy,mm,dd) -datetime.timedelta(days=i)
        print dt
        time.sleep(1)
        mt3filemove(dt)