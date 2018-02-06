#coding: utf-8
#
# ファイル名：IR-remocon03-dirbase.py　　　python2用
# バージョン：2017/12/13 v1.0
#
# ビット・トレード・ワン社提供のラズベリー・パイ専用 学習リモコン基板(型番：ADRSIR)用のツール
#　著作権者:(C) 2015 ビット・トレード・ワン社
#　ライセンス: ADL(Assembly Desk License)
#
#　******ディレクトリベース　実行コマンド　ディレクトリ単位（ファイル名固定：ch0-9.data）
# 呼び出し例　python /home/pi/I2C0x52-IR/I2C0x52-IR-remocon.py rd　tab0
#ＰＩＣ→ラズハ゜イ　ディレクトリ読込コマンド（rd:read　directry)：、保存ディレクトリ名（dir_name)
#ＰＩＣ←ラズハ゜イ　ディレクトリ書込コマンド（wd:write　directry)：、読込ディレクトリ名（dir_name)
#
#　******Ｉ２Ｃ関係内部コマンド
# cmd R1_memo_no_write 0x15 bus-write(ADR,cmd,n)
# cmd R2_data_num_read 0x25 bus-read(ADR,cmd,n)
# cmd R3_data_read     0x35 bus-read(ADR,cmd,n)
# cmd W1_memo_no_write 0x19 bus-write(ADR,cmd,n)
# cmd W2_data_num_write0x29 bus-write(ADR,cmd,n)
# cmd W3_data_write    0x39 bus-read(ADR,cmd,n)
# cmd W4_flash_write   0x49 bus-read(ADR,cmd,n)
# cmd T1_trans_start   0x59 bus-write(ADR,cmd,n)
#

import smbus
import time
from time import sleep
import commands
import subprocess
import os
import sys

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This must match in the Arduino Sketch
#SLAVE_ADDRESS = 0x04
SLAVE_ADDRESS = 0x52
data_numH = 0x31
data_numL = 0x32
data_numHL = [0x00,0x31,0x32]
data_num = 10
memo_no = 0
block = []

#command
R1_memo_no_write = 0x15  #bus-write(ADR,cmd,1)
R2_data_num_read = 0x25 #bus-read(ADR,cmd,3)
R3_data_read           = 0x35 #bus-read(ADR,cmd,n)
W1_memo_no_write  = 0x19 #bus-write(ADR,cmd,1)
W2_data_num_write = 0x29 #bus-write(ADR,cmd,3)
W3_data_write           = 0x39 #bus-read(ADR,cmd,n)
W4_flash_write           = 0x49 #bus-read(ADR,cmd,n)
T1_trans_start             = 0x59 #bus-write(ADR,cmd,1)

############# read command
def read_command(filename,memo_no):
# cmd R1_memo_no_write 0x15 bus-write(ADR,cmd,1)
    print("memo_no write=",memo_no)
    bus.write_i2c_block_data(SLAVE_ADDRESS, R1_memo_no_write ,memo_no )   #= 0x15  #bus-write(ADR,cmd,1)

# cmd R2_data_num_read 0x25 bus-read(ADR,cmd,3)
    data_numHL = bus.read_i2c_block_data(SLAVE_ADDRESS, R2_data_num_read ,3 )#= 0x25 #bus-read(ADR,cmd,3)
    data_num = data_numHL[1]
    data_num *= 256
    data_num += data_numHL[2]
    print("data_num =",data_num )

# cmd R3_data_read           0x35 bus-read(ADR,cmd,n)
    block = []
    block_dat  = bus.read_i2c_block_data(SLAVE_ADDRESS, R3_data_read , 1)       #= 0x35 #bus-read(ADR,cmd,n)
    for i in range(data_num ):
     block_dat  = bus.read_i2c_block_data(SLAVE_ADDRESS, R3_data_read , 4)       #= 0x35 #bus-read(ADR,cmd,n)
     block.append(block_dat[0])
     block.append(block_dat[1])
     block.append(block_dat[2])
     block.append(block_dat[3])
    print(block)  #for denug
    print(filename)
    f = open(filename,'w')
    for i in range(len(block)):
        #f.write('format(block[i]{ X}
        f.write('{:02X}'.format(block[i] ))
    f.close()

################# write command
def write_command(filename ,memo_no):
    f = open(filename,'r')
    block2 =f.read()
    f.close()
    print(block2)
    print(len(block2))
    str_tmp = ""
    int_tmp = []
    for i in range(len(block2)/2):
        str_tmp = block2[i*2] + block2[i*2+1]
        int_tmp.append( int(str_tmp, 16))
    print(int_tmp)  
    print(len(int_tmp))
# cmd W1_memo_no_write 0x19 bus-write(ADR,cmd,1)
    bus.write_i2c_block_data(SLAVE_ADDRESS, W1_memo_no_write ,memo_no )   #= 
# cmd W2_data_num_write 0x29 bus-write(ADR,cmd,3)
    data_num = len(int_tmp)/4  #for test
    data_numHL = [0x31,0x32] #for test
    data_numHL[0] = data_num/256
    data_numHL[1] = data_num%256
    bus.write_i2c_block_data(SLAVE_ADDRESS, W2_data_num_write ,  data_numHL)   #= 
# cmd W3_data_write           0x39 bus-read(ADR,cmd,n)
    print(data_num)
    data_numHL = [0x31,0x32,0x33,0x34] #for test 
    for i in range(data_num):
         data_numHL[0] = int_tmp[i*4+0]
         data_numHL[1] = int_tmp[i*4+1]
         data_numHL[2] = int_tmp[i*4+2]
         data_numHL[3] = int_tmp[i*4+3]
         bus.write_i2c_block_data(SLAVE_ADDRESS, W3_data_write , data_numHL)   #= 
# cmd W4_flash_write           0x49 bus-read(ADR,cmd,n)
    bus.write_i2c_block_data(SLAVE_ADDRESS, W4_flash_write,memo_no)   #=

# #############trans command
def trans_command(filename ):
    f = open(filename,'r')
    block2 =f.read()
    f.close()
    print(block2)
    print(len(block2))
    str_tmp = ""
    int_tmp = []
    for i in range(len(block2)/2):
        str_tmp = block2[i*2] + block2[i*2+1]
        int_tmp.append( int(str_tmp, 16))
    print(int_tmp)  
    print(len(int_tmp))
# cmd W2_data_num_write 0x29 bus-write(ADR,cmd,3)
    data_num = len(int_tmp)/4  #for test
    data_numHL = [0x31,0x32] #for test
    data_numHL[0] = data_num/256
    data_numHL[1] = data_num%256
    bus.write_i2c_block_data(SLAVE_ADDRESS, W2_data_num_write ,  data_numHL)   #= 
# cmd W3_data_write           0x39 bus-read(ADR,cmd,n)
    print(data_num)
    data_numHL = [0x31,0x32,0x33,0x34] #for test 
    for i in range(data_num):
         data_numHL[0] = int_tmp[i*4+0]
         data_numHL[1] = int_tmp[i*4+1]
         data_numHL[2] = int_tmp[i*4+2]
         data_numHL[3] = int_tmp[i*4+3]
         bus.write_i2c_block_data(SLAVE_ADDRESS, W3_data_write , data_numHL)   #= 
 # cmd T1_trans_start             0x59 bus-write(ADR,cmd,1)
    memo_no = [0x00 ] #for dummy
    bus.write_i2c_block_data(SLAVE_ADDRESS, T1_trans_start,memo_no )   #= 

###########################   main
dir_name = '/home/pi/I2C0x52-IR/'
os.chdir(dir_name)
    
while True:
    arg1 = ''
    argv = sys.argv
    argc = len(argv)
    if  (argc  == 3):
       command = sys.argv[1]
       print('command=',command)
       dir_name = sys.argv[2]
       if dir_name <>'':
          cmd = 'mkdir  -p ' + dir_name    #-pオプション（--parentsオプション）を指定
          d = subprocess.check_output(cmd.split())
          os.chdir(dir_name)
          print('dir_name=',dir_name)
          cmd = 'ls -l'
          d = subprocess.check_output(cmd.split())
          print(d)
          cmd = 'pwd'
          d = subprocess.check_output(cmd.split())
          print(d)

       print('dir_name=',dir_name)
       if command == 'rd' :
           print("rd_mode_start")
           for i in range(10):
             memo_no= [0x02 ] #for test
             memo_no[0] = i 
             filename = 'ch' + str(memo_no [0])+ '.data'
             print("read firename =",filename)
             read_command(filename,memo_no)
             sleep(0.5)
           print("rd_mode_end")
           cmd = 'ls -l'
           d = subprocess.check_output(cmd.split())
           print(d)
           break
       if command == 'wd' :
           print("wd_mode_start")
           for i in range(10):
             memo_no= [0x02 ] #for test
             memo_no[0] = i 
             filename = 'ch' + str(memo_no [0])+ '.data'
             print("write firename =",filename)
             write_command(filename,memo_no)
             sleep(1.0)  #0.55>NG 0.6:ok  sleep(1.0)  
           print("wd_mode_end")
           break   
    break

