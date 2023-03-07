import numpy as np
import glob
import pandas as pd
import nibabel as nib
import monai # MONAI cropforeground vs EDA-NIf get_nonzero3d


def count_center_voxel_labels(self, nifti_path: str, x_val: int, y_val: int, z_val):
    img = nib.load(nifti_path)
    x,y,z = img.shape
    center_x, center_y, center_z = int(np.round(x/2)), int(np.round(y/2)), int(np.round(z/2))
    n_count = np.count_nonzero 
    img_array = img.get_fdata()

    center_region_mask_label_count = n_count(img_array [center_x-x_val:center_x+x_val, center_y-y_val:center_y+y_val, center_z-z_val:center_z+z_val])

    return center_region_mask_label_count


## get_nonzero3d
def if_minus_return_0(value: float) -> float:
    if np.sign(value) == -1:
        value = 0
    return value


def get_nonzero3d(nifti_file_path: str, save_path: str, margin: int) -> None:
    file_name = nifti_file_path.split('\\')[-1].rstrip('nii.gz')
    nii = nib.load(nifti_file_path)
    nii_array = nii.get_fdata()
    original_affine = nii.affine
    # print(nii.shape)
    non_zeros = np.nonzero(nii_array>3)

    x_min = non_zeros[0].min()
    x_max = non_zeros[0].max()
    y_min = non_zeros[1].min()
    y_max = non_zeros[1].max()
    z_min = non_zeros[2].min()
    z_max = non_zeros[2].max()
    
    clip_x_min = if_minus_return_0(x_min-margin)
    clip_x_max = if_minus_return_0(x_max+margin)
    clip_y_min = if_minus_return_0(y_min-margin)
    clip_y_max = if_minus_return_0(y_max-margin)
    clip_z_min = if_minus_return_0(z_min-margin)
    clip_z_max = if_minus_return_0(z_max-margin)
    
    nonzero3darray = nii_array[clip_x_min:clip_x_max, clip_y_min:clip_y_max, clip_z_min:clip_z_max]
    img = nib.Nifti1Image(nonzero3darray, original_affine) 
    img.to_filename(f'{save_path}/{file_name}.nii.gz')
    
    return nonzero3darray


## for get nonzero 3darray shape from cohort dataset
def get_nonzero3d_shape(nifti_file_path: str) -> int:
    nii = nib.load(nifti_file_path)
    nii_array = nii.get_fdata()
    non_zeros = np.nonzero(nii_array>2)

    x_min = non_zeros[0].min()
    x_max = non_zeros[0].max()
    y_min = non_zeros[1].min()
    y_max = non_zeros[1].max()
    z_min = non_zeros[2].min()
    z_max = non_zeros[2].max()
    return x_min, x_max, y_min, y_max, z_min, z_max


## for crop same size when all data(with mask) is co-registerd and preprocessed.
def get_hardcrop(nifti_file_path: str, save_path: str, x_min: int, x_max: int, y_min:int, y_max: int, z_min: int, z_max: int) -> None:
    file_name = nifti_file_path.split('\\')[-1].rstrip('nii.gz')
    nii = nib.load(nifti_file_path)
    nii_array = nii.get_fdata()
    nii_array = nii_array[x_min:x_max, y_min:y_max, z_min:z_max]
    original_affine = nii.affine
    img = nib.Nifti1Image(nii_array, original_affine) 
    img.to_filename(f'{save_path}/{file_name}.nii.gz')
    return None


## monai.cropforeground
def threshold_at_two(x):
    # threshold at 2
    return x > 2


def monai_cropforeground(nifit_file_path:str, save_path: str):
    file_name = nifit_file_path.split('\\')[-1].rstrip('.nii.gz')
    img = nib.load(nifit_file_path)
    img_array = img.get_fdata()
    original_affine = img.affine
    cropper = monai.transforms.CropForeground(select_fn=threshold_at_two, margin=2)
    cropped_img = cropper(img_array)
    img = nib.Nifti1Image(cropped_img, original_affine) 
    img.to_filename(f'{save_path}/{file_name}.nii.gz')


def get_nonzero_xyz_of_nii(nifti_file_path: str) -> (int, int, int, int, int, int):
    nii = nib.load(nifti_file_path)
    nii_array = nii.get_fdata()
    # print(nii.shape)
    non_zeros = np.nonzero(nii_array>3)
    x_min = non_zeros[0].min()
    x_max = non_zeros[0].max()
    y_min = non_zeros[1].min()
    y_max = non_zeros[1].max()
    z_min = non_zeros[2].min()
    z_max = non_zeros[2].max()
    
    return x_min, x_max, y_min, y_max, z_min, z_max

