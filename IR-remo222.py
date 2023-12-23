#!/usr/bin/env python
# coding: utf-8

u"""
ビット・トレード・ワン社提供のラズベリー・パイ専用 学習リモコン基板(型番：ADRSIR)用のツール
著作権者:(C) 2015 ビット・トレード・ワン社
ライセンス: ADL(Assembly Desk License)
+ちょっとmycustom
"""

import sys

import smbus2


# This must match in the Arduino Sketch
#SLAVE_ADDRESS = 0x04
SLAVE_ADDRESS = 0x52

# command
R1_MEMO_NO_WRITE = 0x15  # bus-write(ADR,cmd,1)
R2_DATA_NUM_READ = 0x25  # bus-read(ADR,cmd,3)
R3_DATA_READ = 0x35  # bus-read(ADR,cmd,n)
W1_MEMO_NO_WRITE = 0x19  # bus-write(ADR,cmd,1)
W2_DATA_NUM_WRITE = 0x29  # bus-write(ADR,cmd,3)
W3_DATA_WRITE = 0x39  # bus-read(ADR,cmd,n)
W4_FLASH_WRITE = 0x49  # bus-read(ADR,cmd,n)
T1_TRANS_START = 0x59  # bus-write(ADR,cmd,1)


def get_smbus():
    # for RPI version 1, use "bus = smbus.SMBus(0)"
    bus = smbus2.SMBus(1)
    return bus


def read_command(memo_no):
    bus = get_smbus()

    bus.write_i2c_block_data(SLAVE_ADDRESS, R1_MEMO_NO_WRITE, memo_no)

    data_numHL = bus.read_i2c_block_data(SLAVE_ADDRESS, R2_DATA_NUM_READ, 3)
    data_num = data_numHL[1]
    data_num *= 256
    data_num += data_numHL[2]

    block = []
    block_dat = bus.read_i2c_block_data(SLAVE_ADDRESS, R3_DATA_READ, 1)
    for i in range(data_num):
        block_dat = bus.read_i2c_block_data(SLAVE_ADDRESS, R3_DATA_READ, 4)
        block.append(block_dat[0])
        block.append(block_dat[1])
        block.append(block_dat[2])
        block.append(block_dat[3])
    return block


def write_command(memo_no, block2):
    bus = get_smbus()

    str_tmp = ""
    int_tmp = []
    for i in range(int(len(block2) / 2)):
        str_tmp = block2[i * 2] + block2[i * 2 + 1]
        int_tmp.append(int(str_tmp, 16))

    bus.write_i2c_block_data(SLAVE_ADDRESS, W1_MEMO_NO_WRITE, memo_no)

    data_num = int(len(int_tmp) / 4)  # for test
    data_numHL = [0x31, 0x32]  # for test
    data_numHL[0] = int(data_num / 256)
    data_numHL[1] = int(data_num % 256)
    bus.write_i2c_block_data(SLAVE_ADDRESS, W2_DATA_NUM_WRITE, data_numHL)

    data_numHL = [0x31, 0x32, 0x33, 0x34]  # for test
    for i in range(data_num):
         data_numHL[0] = int_tmp[i * 4 + 0]
         data_numHL[1] = int_tmp[i * 4 + 1]
         data_numHL[2] = int_tmp[i * 4 + 2]
         data_numHL[3] = int_tmp[i * 4 + 3]
         bus.write_i2c_block_data(SLAVE_ADDRESS, W3_DATA_WRITE, data_numHL)

    bus.write_i2c_block_data(SLAVE_ADDRESS, W4_FLASH_WRITE, memo_no)


def trans_command(block2):
    bus = get_smbus()

    str_tmp = ""
    int_tmp = []
    for i in range(int(len(block2)/2)):
        str_tmp = block2[i * 2] + block2[i * 2 + 1]
        int_tmp.append(int(str_tmp, 16))

    data_num = int(len(int_tmp) / 4)  #for test
    data_numHL = [0x31, 0x32]  # for test
    data_numHL[0] = int(data_num / 256)
    data_numHL[1] = int(data_num % 256)
    bus.write_i2c_block_data(SLAVE_ADDRESS, W2_DATA_NUM_WRITE, data_numHL)

    data_numHL = [0x31, 0x32, 0x33, 0x34]  # for test
    for i in range(data_num):
         data_numHL[0] = int_tmp[i * 4 + 0]
         data_numHL[1] = int_tmp[i * 4 + 1]
         data_numHL[2] = int_tmp[i * 4 + 2]
         data_numHL[3] = int_tmp[i * 4 + 3]
         bus.write_i2c_block_data(SLAVE_ADDRESS, W3_DATA_WRITE, data_numHL)

    # cmd T1_TRANS_START             0x59 bus-write(ADR,cmd,1)
    memo_no = [0x00]  # for dummy
    bus.write_i2c_block_data(SLAVE_ADDRESS, T1_TRANS_START, memo_no)

def trans_file_command(filename):
    bus = get_smbus()

    f = open(filename,'r')
    block2 =f.read()
    f.close()

    str_tmp = ""
    int_tmp = []
    for i in range(int(len(block2)/2)):
        str_tmp = block2[i * 2] + block2[i * 2 + 1]
        int_tmp.append(int(str_tmp, 16))

    data_num = int(len(int_tmp) / 4)  #for test
    data_numHL = [0x31, 0x32]  # for test
    data_numHL[0] = int(data_num / 256)
    data_numHL[1] = int(data_num % 256)
    bus.write_i2c_block_data(SLAVE_ADDRESS, W2_DATA_NUM_WRITE, data_numHL)

    data_numHL = [0x31, 0x32, 0x33, 0x34]  # for test
    for i in range(data_num):
         data_numHL[0] = int_tmp[i * 4 + 0]
         data_numHL[1] = int_tmp[i * 4 + 1]
         data_numHL[2] = int_tmp[i * 4 + 2]
         data_numHL[3] = int_tmp[i * 4 + 3]
         bus.write_i2c_block_data(SLAVE_ADDRESS, W3_DATA_WRITE, data_numHL)

    # cmd T1_TRANS_START             0x59 bus-write(ADR,cmd,1)
    memo_no = [0x00]  # for dummy
    bus.write_i2c_block_data(SLAVE_ADDRESS, T1_TRANS_START, memo_no)

def print_usage():
    print(u"{0} r 0".format(sys.argv[0]))
    print(u"{0} w 0 code".format(sys.argv[0]))
    print(u"{0} t code".format(sys.argv[0]))
    print(u"{0} tf filename".format(sys.argv[0]))
    print(u"{0} rf 0 filename".format(sys.argv[0]))

def main():
    argc = len(sys.argv)
    if argc < 2:
        print_usage()
        return 1

    command = sys.argv[1]
    if command == 'r':
        if argc != 3:
            print_usage()
            return 1

        res_data = [141, 0, 47, 0]  # bin num [0x141, 0x0, 0x68, 0x0]
        memo_no = [0x0]  # エラー対策TypeError: 'int'
        memo_no[0] = int(sys.argv[2])
        res_data = read_command(memo_no)
        for i in range(len(res_data)):
            sys.stdout.write("{:02X}".format(res_data[i]))
        print("")
        return 0

    elif command == 'rf':
        if argc != 4:
            print_usage()
            return 1

        res_data = [141, 0, 47, 0]  # bin num [0x141, 0x0, 0x68, 0x0]
        memo_no = [0x0]  # エラー対策TypeError: 'int'
        memo_no[0] = int(sys.argv[2])
        filename = sys.argv[3]
        res_data = read_command(memo_no)

        f = open(filename,'w')
        for i in range(len(res_data)):
            f.write("{:02X}".format(res_data[i]))
        f.close

    elif command == 'w':
        if argc != 4:
            print_usage()
            return 1

        memo_no = [0x0]  # エラー対策TypeError: 'int'
        memo_no[0] = int(sys.argv[2])
        block2 = sys.argv[3]

        write_command(memo_no,block2)
        return 0
    elif command == 't':
        if argc != 3:
            print_usage()
            return 1

        block2 = sys.argv[2]
        trans_command(block2)
        return 0

    elif command == 'tf':
        if argc != 3:
            print_usage()
            return 1


        file_name = sys.argv[2]
        trans_file_command(file_name)
        return 0

    elif command == "help":
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
