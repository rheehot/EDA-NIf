import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from io import StringIO


def find_all_files(top_folder_path: str, include_word: str) -> list:
    all_file_pathes = []
    for (root, directories, files) in os.walk(top_folder_path):
        for file in files:
            if include_word in file:
                detect_file_path = os.path.join(root, file)
                all_file_pathes.append(detect_file_path)
    return all_file_pathes
    

def save_print_instance(*message):
    io = StringIO()
    print(*message, file=io, end="")
    return io.getvalue()


def center_niishow(nifti_file_path: str, axis: str) -> np.array:
    nii = nib.load(nifti_file_path)
    nii_array = nii.get_fdata()
    try:
        x,y,z = nii_array.shape
        if axis=='x':
            plt.imshow(nii_array[int(np.round(x/2)),:,:])
        elif axis=='y':
            plt.imshow(nii_array[:,int(np.round(y/2)),:])
        elif axis=='z':
            plt.imshow(nii_array[:,:,int(np.round(z/2))])
        
    except Exception as e:
        print(e)
        pass
    # print(nii_array.shape)
    # print(f'sx=={sx}, sy=={sy}, sz=={sz}, volume_unit_of_nii=={volume_unit}')

    return nii_array


# support func for <get_matching_path_dict> method 
def get_mask_nii_path(nii_list: list, subject_numb: int, mask_word: str) -> str:
    '''Support method for `get_matching_path_dict`

    parameters:
    -----------
    nii_list: list
        globbed nii list(raw and mask)
    subject_numb: int 
        only for BIDS format file name must be has subject and modality
    mask_word: str 
        mask file include word(like 'msk' or 'mask' word in mask nifti file name)
    '''
    mask_nii_path = None
    for nii_path in nii_list:
        if subject_numb in nii_path and mask_word in nii_path:
            mask_nii_path = nii_path

    return mask_nii_path


def get_matching_path_dict(nii_list: list, maskword: str) -> dict: 
    '''
    Example code:
        matching_path_dict = get_matching_path_dict(nii_list, 'msk')
        matching_path_dict_keys = [key for key in matching_path_dict.keys()]

    parameters:
    -----------
    nii_list: str 
        1 list containing globs of raw and mask filepaths in BIDS format
    maskword: 
        mask file include word(like 'msk' or 'mask' word in mask nifti file name)
    '''
    matching_path_dict = dict()
    for nii_path in nii_list:
        if maskword not in nii_path:
            raw_nii = nii_path
            subject = nii_path.split('\\')[-1].split('_')[0]
            mask_nii_path = get_mask_nii_path(nii_list, subject, maskword)
            matching_path_dict[raw_nii] = mask_nii_path
        else:
            pass
    
    return matching_path_dict


def get_maskout_array(resampled_raw_nifti_path: str, resampled_mask_nifti_path: str, axial: str) -> np.array:
    raw_nii = nib.load(resampled_raw_nifti_path)
    raw_array = raw_nii.get_fdata()
    x,y,z = raw_array.shape[0], raw_array.shape[1], raw_array.shape[2]
    mask_nii = nib.load(resampled_mask_nifti_path)
    mask_array = mask_nii.get_fdata()

    if axial == 'x':
        mask_array = mask_array[:x,:,:]
    elif axial == 'y':
        mask_array = mask_array[:,:y,:]
    elif axial == 'z':
        mask_array = mask_array[:,:,:z]

    if raw_array.shape == mask_array.shape:
        mask_array = 1-mask_array
        maskout_array = raw_array * mask_array
    else:
        maskout_array = None
        print('Error [get_maskout_array]: raw_nii shape does not match to mask nii shape. please check')

    return maskout_array