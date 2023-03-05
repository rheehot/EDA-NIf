import nibabel as nib 
import numpy as np


def count_center_voxel_labels(self, nifti_path: str, x_val: int, y_val: int, z_val):
    img = nib.load(nifti_path)
    x,y,z = img.shape
    center_x, center_y, center_z = int(np.round(x/2)), int(np.round(y/2)), int(np.round(z/2))
    n_count = np.count_nonzero 
    img_array = img.get_fdata()

    center_region_mask_label_count = n_count(img_array [center_x-x_val:center_x+x_val, center_y-y_val:center_y+y_val, center_z-z_val:center_z+z_val])

    return center_region_mask_label_count
