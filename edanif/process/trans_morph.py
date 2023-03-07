import sys
import numpy as np
import nibabel as nib
from pathlib import Path
from skimage import morphology


def voxel_erosion(array3d:np.array) -> np.array:
    (x, y, z) = np.shape(array3d)
    erosion_mask = array3d.copy()
    print(x,y,z)
    for slice_number in range(z):
        image_slice = erosion_mask[:, :, slice_number]
        erosion_mask[:, :, slice_number] = morphology.binary_erosion(image_slice, morphology.diamond(1))
        
    return erosion_mask        


def voxel_dilation(array3d: np.array) -> np.array:
    (x, y, z) = np.shape(array3d)
    dilated_img = array3d.copy()
    for slice_number in range(z):
        image_slice = dilated_img[:, :, slice_number]
        dilated_img[:, :, slice_number] = morphology.binary_dilation(image_slice, morphology.diamond(1))
        
    return dilated_img


def get_boundary_diff_index(raw_nifti_file_path, mask_nifti_file_path):
    raw_nii = nib.load(raw_nifti_file_path)
    raw_nii_array = raw_nii.get_fdata()
    x,y,z = raw_nii_array.shape
    # raw_affine = raw_nii.affine
    mask_nii = nib.load(mask_nifti_file_path)
    mask_nii_array = mask_nii.get_fdata()
    mask_nii_array = mask_nii_array[:,:,:z]
    # mask_affine = mask_nii.affine
    
    eroded_mask = voxel_erosion(mask_nii_array)
    dilated_mask = voxel_dilation(mask_nii_array)
    out_boundary_mask = dilated_mask - mask_nii_array
    out_boundary_mask[out_boundary_mask<0] = 0
    inner_boundary_mask = mask_nii_array - eroded_mask
    out_boundary_val = raw_nii_array*out_boundary_mask
    inner_boundary_val = raw_nii_array*inner_boundary_mask
    boundary_diff_index = np.sum(out_boundary_val) - np.sum(inner_boundary_val)
        
    return boundary_diff_index