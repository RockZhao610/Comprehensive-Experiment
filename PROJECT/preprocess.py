import nibabel as nib
import numpy as np
import imageio
import os
def makedir(path):
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)

def read_niifile(niifile):  # 读取niifile文件
    img = nib.load(niifile)  # 下载niifile文件（其实是提取文件）
    img_fdata = img.get_fdata()  # 获取niifile数据
    return img_fdata


def save_fig(file,savepicdir,name):  # 保存为图片
    fdata = read_niifile(file)  # 调用上面的函数，获得数据
    # (x, y, z) = fdata.shape  # 获得数据shape信息：（长，宽，维度-切片数量）
    # for k in range(z):
    silce = fdata[:, :, i]  # 三个位置表示三个不同角度的切片
    imageio.imwrite(os.path.join(savepicdir, '{}.png'.format(name)), silce)
        # 将切片信息保存为png格式
def getName(na):
    for i in range(0,len(na)):
        if na[i]=='_':
            return na[:i]
#传入nii.gz文件所在文件夹
niiGzFolder='/.nii文件夹路径/'
niiGzNames=os.listdir(niiGzFolder)
#存放解压后的分割图片
target='/存放png图片的路径/'
for i in range(0,len(niiGzNames)):
    niiGzName=niiGzNames[i]
    name=getName(niiGzName)
    pred="pred"
    gt="gt"
    img="img"
    if  pred in niiGzName:
        path=target+pred+'/'

    if gt in niiGzName:
        path=target+gt+'/'

    if img in niiGzName:
        path=target+img+'/'
    makedir(path)
    save_fig(niiGzFolder+niiGzName,path,name)
    print("finish",niiGzName)