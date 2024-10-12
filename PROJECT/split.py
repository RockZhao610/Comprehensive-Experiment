import nibabel as nib
import matplotlib.pyplot as plt
import os

def convert_and_split_dataset(data_folder, label_folder, output_folder, train_ratio=0.8):
    # 获取所有 .nii 文件的路径
    nii_files = [file for file in os.listdir(data_folder) if file.endswith('.nii.gz')]

    # 计算用于训练的文件数量
    num_train = int(train_ratio * len(nii_files))

    # 分割成训练集和测试集
    train_files = nii_files[:num_train]
    test_files = nii_files[num_train:]

    # 处理训练集
    for file in train_files:
        process_nii_file(file, data_folder, label_folder, output_folder, 'train')

    # 处理测试集
    for file in test_files:
        process_nii_file(file, data_folder, label_folder, output_folder, 'test')

def process_nii_file(file, data_folder, label_folder, output_folder, subset):
    # 构建 .nii 文件的路径
    nii_data_path = os.path.join(data_folder, file)
    nii_label_path = os.path.join(label_folder, file)

    # 加载 .nii 文件
    data_img = nib.load(nii_data_path)
    label_img = nib.load(nii_label_path)
    
    data = data_img.get_fdata()
    label = label_img.get_fdata()

    # 遍历每个切片
    for i in range(data.shape[2]):
        # 选择切片数据和标签
        slice_data = data[:, :, i]
        slice_label = label[:, :, i]

        # 构建输出文件夹路径
        output_folder_data = os.path.join(output_folder, subset, 'data')
        output_folder_label = os.path.join(output_folder, subset, 'label')

        if not os.path.exists(output_folder_data):
            os.makedirs(output_folder_data)

        if not os.path.exists(output_folder_label):
            os.makedirs(output_folder_label)

        # 构建输出文件的路径
        output_file_path = os.path.join(output_folder_data, f"{file}_{i}.png")
        output_label_path = os.path.join(output_folder_label, f"Infection_Mask_{file}_{i}.png")

        # 保存为 .png 格式
        plt.imsave(output_file_path, slice_data, cmap='gray')
        plt.imsave(output_label_path, slice_label, cmap='gray')

# 示例使用
data_folder = 'COVID-19-CT-Seg_20cases'  # 替换为您的数据文件夹路径
label_folder = 'Infection_Mask'          # 替换为您的标签文件夹路径
output_folder = 'COVID19_CT_dataset_png' # 替换为您想要保存 .png 文件的文件夹路径
convert_and_split_dataset(data_folder, label_folder, output_folder)