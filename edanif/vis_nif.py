import os
import nibabel as nib 
import matplotlib.pyplot as plt


def save_nifti_images(nif_file_path:str, axis:str, layer_numb_list:list, interval:int, save_path:str) -> None:
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_name = nif_file_path.split('\\')[-1].rstrip('.nii.gz')
    img = nib.load(nif_file_path)
    data = img.get_fdata()
    fig, axs = plt.subplots(3, 3, figsize=(10,10))
    if layer_numb_list==None:
        layer_numb_list = [int((data.shape[axis]/2+(interval*4))-interval*i) for i in range(9)]
        for ax, layer_numb in zip(axs.ravel(), layer_numb_list):
            if axis==2:
                sample = data[:,:,layer_numb]
            elif axis==1:
                sample = data[:,layer_numb,:]
            elif axis==0:
                sample = data[layer_numb,:,:]
            ax.imshow(sample, cmap='gray')
    else:
        for ax, layer_numb in zip(axs.ravel(), layer_numb_list):
            if axis==2:
                sample = data[:,:,layer_numb]
            elif axis==1:
                sample = data[:,layer_numb,:]
            elif axis==0:
                sample = data[layer_numb,:,:]
            ax.imshow(sample, cmap='gray')
    plt.savefig(os.path.join(save_path,file_name)+'.png', dpi=300)
    plt.close()

    return None