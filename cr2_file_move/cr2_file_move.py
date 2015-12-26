#! C:/tool/Python27/python.exe
# -*- coding: utf-8 -*-

import sys
import os
import re
import shutil
import datetime
import unittest

from struct import *

recognised_tags = { 
    0x0100 : 'imageWidth',
    0x0101 : 'imageLength',
    0x0102 : 'bitsPerSample',
    0x0103 : 'compression',
    0x010f : 'make',    
    0x0110 : 'model',
    0x0111 : 'stripOffset',
    0x0112 : 'orientation', 
    0x0117 : 'stripByteCounts',
    0x011a : 'xResolution',
    0x011b : 'yResolution',
    0x0128 : 'resolutionUnit',
    0x0132 : 'dateTime',
    0x8769 : 'EXIF',
    0x8825 : 'GPS data'};

def GetHeaderFromCR2( buffer, pflag=False ):
    # Unpack the header into a tuple
    header = unpack_from('HHLHBBL', buffer)

    if pflag :
        print "\nbyte_order = 0x%04X"%header[0]
        print "tiff_magic_word = %d"%header[1]
        print "tiff_offset = 0x%08X"%header[2]
        print "cr2_magic_word = %d"%header[3]
        print "cr2_major_version = %d"%header[4]
        print "cr2_minor_version = %d"%header[5]
        print "raw_ifd_offset = 0x%08X\n"%header[6]

    return header

def FindDateTimeOffsetFromCR2( buffer, ifd_offset, endian_flag, pflag=False ):
    # Read the number of entries in IFD #0
    (num_of_entries,) = unpack_from(endian_flag+'H', buffer, ifd_offset)
    if pflag :
        print "Image File Directory #0 contains %d entries\n"%num_of_entries

    # Work out where the date time is stored
    datetime_offset = -1

    # Go through all the entries looking for the datetime field
    if pflag :
        print " id  | type |  number  |  value   "
    for entry_num in range(0,num_of_entries):

        # Grab this IFD entry
        (tag_id, tag_type, num_of_value, value) = unpack_from(endian_flag+'HHLL', buffer, ifd_offset+2+entry_num*12)

        # Print out the entry for information
        if pflag :
            print "%04X | %04X | %08X | %08X "%(tag_id, tag_type, num_of_value, value),
            if tag_id in recognised_tags:
                print recognised_tags[tag_id]

        # If this is the datetime one we're looking for, make a note of the offset
        if tag_id == 0x0132:
            assert tag_type == 2
            assert num_of_value == 20
            datetime_offset = value

    return datetime_offset
#
# file type (.CR2) のチェック
# 画像の撮影時間の抽出
# 時間を明記したファイル名生成
def MakeNewFileName(fn, dev_id, sdir=''):
    # file type check
    if not (fn.endswith(".CR2") and len(fn)==12) :
        return fn

    with open(sdir+fn, "rb") as f:
        # read the first 1kb of the file should be enough to find the date/time
        buffer = f.read(1024) 

        # Grab the various parts of the header
        (byte_order, tiff_magic_word, tiff_offset, cr2_magic_word, cr2_major_version, cr2_minor_version, raw_ifd_offset) = GetHeaderFromCR2(buffer)

        # Set the endian flag
        endian_flag = '@'
        if byte_order == 0x4D4D:
            # motorola format
            endian_flag = '>'
        elif byte_order == 0x4949:
            # intel format
            endian_flag = '<'

        # Search for the datetime entry offset
        datetime_offset = FindDateTimeOffsetFromCR2(buffer, 0x10, endian_flag)

        datetime_string = unpack_from(20*'s', buffer, datetime_offset)
        print "\nDatetime: "+"".join(datetime_string)+fn+"\n"
        
        # make new fn
        t0=''.join(datetime_string)
        t1=t0.replace(":","")
        t1=t1.replace(" ","_")
        t1=t1.replace("\x00","_xxx_"+dev_id+"_"+fn)
    return t1

#---------------------------------------------------
# avi ファイルコピー
#
def proc_cr2_move(SoucePath,TargetPath,dev_id):
    # 条件確認
    if os.path.exists(SoucePath) == False:
        print "Souce path '%s' not exists!" % SoucePath
        return SoucePath
        
    if os.path.exists(TargetPath) == False:
        os.makedirs(TargetPath)

    files = os.listdir(SoucePath)
    for file in files:
        jpg = re.compile("CR2")
        if jpg.search(file):
            newfn = MakeNewFileName(file, dev_id, SoucePath)
            #print file
            #print newfn
            if not file==newfn:
                os.rename(SoucePath+file, SoucePath+newfn)
                file=newfn
            if file[8]=='_' and len(file)==35:
                obsdate=file.split("_")[0]
                if os.path.exists(TargetPath+"/"+obsdate) == False:
                    os.makedirs(TargetPath+"/"+obsdate)

                file_move(file,SoucePath,TargetPath+obsdate+"/")
    print 'Complete!!!'

#---------------------------------------------------
# ファイルムーブ
# ターゲットなしなら、そのままmove
# ターゲットに同名ファイルありなら、サイズ（大きい方が正）日付（新しい方が正）
# ソースが正なら、ターゲット削除後、ムーブ
# ソースが否なら、ソースを別名で移動（+".1"）
#              fn      dir(/)   dir(/)
def file_move(Filename,SouceDir,TargetDir):
    if SouceDir[-1:]!="/":
        SouceDir +="/"
    if TargetDir[-1:]!="/":
        TargetDir +="/"
    src = SouceDir  + Filename
    dst = TargetDir + Filename
    #print Filename,SouceDir,TargetDir
    if not os.path.exists(src):
        return 
    if os.path.exists(dst):
        #print "Destination path '%s' already exists!!" % dst
        if os.path.getsize(src) > os.path.getsize(dst):
            os.remove(dst)
            shutil.move(src,TargetDir)
        else:
            dt_target = datetime.datetime.fromtimestamp(os.stat(dst).st_mtime)
            dt_souce  = datetime.datetime.fromtimestamp(os.stat(src).st_mtime)
            if dt_target >= dt_souce:
                os.remove(src)
            else:                
                shutil.move(src+".1",TargetDir)
    else:
        try:
            shutil.move(src, TargetDir)
        except OSError:
            print 'no such file'

# テスト対象の関数
def factorial(n):
    """factorial function"""
    if n < 2:
        return 1
    return factorial(n - 1)

# テストケースをまとめたクラス
# メソッド名が test で始まるメソッドがひとつのテストとなる
class FactorialTest(unittest.TestCase):

    def test_factorial_with_arg_1(self):
        expected = 1
        actual = factorial(1)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
#    unittest.main()

    #指定する画像フォルダ
    TargetPath='C:/temp/'
    SoucePath='C:/temp/tmp/'
    dev_id="12"
    proc_cr2_move(SoucePath,TargetPath,dev_id)

    #指定する画像フォルダ
#    TargetPath='J:/MT/'
#    SoucePath='J:/DCIM/100EOS5D/'
#    dev_id="12"
#    proc_cr2_move(SoucePath,TargetPath,dev_id)
