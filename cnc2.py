'''
Date: 2024-04-20 09:53:25
LastEditors: Zfj
LastEditTime: 2024-04-25 11:31:23
FilePath: /python-cnc/cnc2.py
Description: 
'''
# https://u.cewaycloud.com/scan-code?short-chain=/aE2ayUYeaa
import os
import shutil
import tkinter as tk
from tkinter import ttk
import psutil
import get_name2
import threading
import time
def find_usb_drives():
    """查找并返回所有连接的USB驱动器的挂载路径。"""
    # drives = []
    # for part in psutil.disk_partitions():
    #     if 'removable' in part.opts:
    #         drives.append(part.mountpoint)
    # print(drives[0])
    # return drives[0]
    # 无线u盘配置的地址
    return r"\\192.168.3.11\udisk"

def copy_folder(src, dest):
    """复制文件或文件夹到目标路径，并更新进度条"""
    if os.path.isdir(src):
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(src) for f in filenames]
        total_files = len(files)
        copied_files = 0

        if not os.path.exists(dest):
            os.makedirs(dest, exist_ok=True)
        
        for file in files:
            dest_file = file.replace(src, dest)
            dest_dir = os.path.dirname(dest_file)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(file, dest_file)
            copied_files += 1
    elif os.path.isfile(src):
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)


def download_file():
  
    file_names = get_name2.main()  # 获取需要下载的文件名称

    usb_drives = find_usb_drives()  # 查找USB驱动器路径列表
    if not usb_drives:
        print("No USB drives detected.")
        return

    # 选择第一个USB驱动器进行操作
    destination_drive = usb_drives
    # destination_drive = usb_drives[0]
    print("Using USB drive:", destination_drive,file_names)
    
    # 共享文件夹路径
    # share_path = r"\\10.10.30.2\1"
    share_path = r"\\192.168.9.3\DD2023\部门文件\CNC加工部"
    if file_names:
    # 为每个文件进行复制操作
     
    #  for file_name in file_names:
        source_folder = os.path.join(share_path, file_names)
        destination = os.path.join(destination_drive, file_names)
        print("Source:", source_folder)
        print("Destination:", destination)
        
        if os.path.exists(source_folder):
            copy_folder(source_folder, destination)
            print("Copy operation completed successfully for:", file_names)
        else:
            print("Specified source does not exist for:", file_names)
    
    

def repeat_func():
    while True:
        download_file()
        time.sleep(5)
        
t = threading.Thread(target=repeat_func)
t.start()
