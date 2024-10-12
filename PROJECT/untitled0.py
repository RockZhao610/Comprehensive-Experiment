import nibabel as nib
import numpy as np
import imageio
import os

def makedir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def read_niifile(niifile):
    try:
        img = nib.load(niifile)
        img_fdata = img.get_fdata()
        return img_fdata
    except Exception as e:
        print(f"Error reading {niifile}: {e}")
        return None

def save_fig(file, savepicdir, name, slice_index):
    fdata = read_niifile(file)
    if fdata is not None:
        (x, y, z) = fdata.shape
        for k in range(z):
            slice_data = fdata[:, :, k]

            # 将数据标准化到0-1范围
            slice_normalized = (slice_data - np.min(slice_data)) / (np.max(slice_data) - np.min(slice_data))

            # 转换为8位整数
            slice_8bit = (slice_normalized * 255).astype(np.uint8)

            # 保存为PNG
            imageio.imwrite(os.path.join(savepicdir, '{}_{}.png'.format(name, k)), slice_8bit)


def getName(na):

    return na

niiGzFolder = 'COVID-19-CT-Seg_20cases'
niiGzNames = os.listdir(niiGzFolder)
target = 'phaoto'
makedir(target)  # 确保目标目录存在
for niiGzName in niiGzNames:
    name = getName(niiGzName)
    file_path = os.path.join(niiGzFolder, niiGzName)
    save_fig(file_path, target, name, 0)  # 假设您想要第0个切片
