## -*- coding: utf-8 -*-

import os
import sys
import datetime
import shutil
import time
import cr2_file_move
import bmp2avi

#---------------------------------------------------
# 2_ .avi ファイル名変更
# datedir -> yyyymmdd
#
def proc_2_rename(BaseSoucePath,dir):
    datedir = dir.replace("/","")
    # 条件確認
    if os.path.exists(BaseSoucePath) == False:
        print "Base Souce path '%s' not exists!" % BaseSoucePath
        return BaseSoucePath

    # src list up
    SoucePath = BaseSoucePath+"/"+datedir
    FileList = os.listdir(SoucePath)
    for f in FileList:
        if ( f[-4:]==".avi"):
            if ( f[:2]=="2_" ):
                fn=f[2:]
                fn=fn[:-4]+"_2.avi"
                src = SoucePath +"/"+ f
                dst = SoucePath +"/"+ fn
                os.rename(src, dst)
            if ( f[:2]=="3_" ):
                fn=f[2:]
                fn=fn[:-4]+"_3.avi"
                src = SoucePath +"/"+ f
                dst = SoucePath +"/"+ fn
                os.rename(src, dst)
            if ( f[:2]=="4_" ):
                fn=f[2:]
                fn=fn[:-4]+"_4.avi"
                src = SoucePath +"/"+ f
                dst = SoucePath +"/"+ fn
                os.rename(src, dst)
            if ( f[:2]=="7_" ):
                fn=f[2:]
                fn=fn[:-4]+"_7.avi"
                src = SoucePath +"/"+ f
                dst = SoucePath +"/"+ fn
                os.rename(src, dst)
            if ( f[:2]=="8_" ):
                fn=f[2:]
                fn=fn[:-4]+"_8.avi"
                src = SoucePath +"/"+ f
                dst = SoucePath +"/"+ fn
                os.rename(src, dst)
            if ( f[:3]=="11_" ):
                fn=f[3:]
                fn=fn[:-4]+"_11.avi"
                src = SoucePath +"/"+ f
                dst = SoucePath +"/"+ fn
                os.rename(src, dst)
   
            
#---------------------------------------------------
# avi ファイルコピー
def mt3filemove(dt = datetime.datetime.now()):
    dir = dt.strftime("/%Y%m%d")
    print dt,dir
    
    BaseSoucePath = "J:/MT"

    # 2_のファイル名変更後、年月日ディレクトリに再振り分け
    proc_2_rename(BaseSoucePath,dir)
    
    
#---------------------------------------------------
# main
# 日付指定   
if __name__ == "__main__":
    dtnow = datetime.datetime.now()
    drange=1 #実行日数（戻り日数）
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
        print "Year '%s' 範囲外" % yyyy
        sys.exit()

    if mm < 1 or mm > 12 :
        print "Month '%s' 範囲外" % mm
        sys.exit()
    
    if dd < 1 or dd > 31 :
        print "Day '%s' 範囲外" % dd
        sys.exit()

    if drange < 1 or drange > 365 :
        print "Drange '%s' 範囲外" % drange
        sys.exit()
    
    for i in range(drange):
        dt = datetime.date(yyyy,mm,dd) -datetime.timedelta(days=i)
        print dt
        time.sleep(1)
        mt3filemove(dt)
