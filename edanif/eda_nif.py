import pandas as pd
import numpy as np
import nibabel as nib 
import tqdm
import edanif

def count_center_voxel_labels(nifti_file_path: str, x_val: int, y_val: int, z_val):
    img = nib.load(nifti_file_path)
    x,y,z = img.shape
    center_x, center_y, center_z = int(np.round(x/2)), int(np.round(y/2)), int(np.round(z/2))
    n_count = np.count_nonzero 
    img_array = img.get_fdata()
    center_region_quadrant_count_label_count = n_count(img_array [center_x-x_val:center_x+x_val, center_y-y_val:center_y+y_val, center_z-z_val:center_z+z_val])
    return center_region_quadrant_count_label_count


def meta_df(nifti_folder_path: str, include_word: str, save_path: str, is_binary: bool) -> pd.DataFrame:
    """If you enter the top-level folder path that contains the nifti files you want to obtain meta data for and keywords (such as 'nii.gz','mask.n) 
    commonly included in those nifti files, a meta data frame is created.

    :param nifti_folder_path: 
        This is the top-level folder path that contains the nifti files you want to obtain metadata from, recursively traverse all folders.
    :type nifti_folder_path: str
    :param include_word: 
        Enter keywords commonly included in nifti files (such as 'nii.gz', 'mask.nii.gz') in the parent folder path.
    :type include_word: str
    :param save_path: Enter the full path to the csv file to save the meta dataframe to.
    :type save_path: str
    :param is_binary: Enter True in case of a binary file such as a mask nifti file.
    :type is_binary: bool
    :return: 
        pandas.DataFrame containing meta information and appended information of each nifti file
    :rtype: pd.DataFrame
    """
    total_dict = dict()
    n_count = np.count_nonzero 
    all_nifti_files = edanif.find_all_files(nifti_folder_path, include_word)
    for i, nifti_path in tqdm(enumerate(all_nifti_files), total=len(all_nifti_files)):
        temp_dict = dict()
        img = nib.load(nifti_path)
        x,y,z = img.shape
        center_x, center_y, center_z = int(np.round(x/2)), int(np.round(y/2)), int(np.round(z/2))
        sx, sy, sz = img.header.get_zooms()
        volume_unit = sx * sy * sz
        img_array = img.get_fdata()
        img_flatten_array = np.ravel(img_array)
        abnormal_quadrant_count = img_flatten_array[(img_flatten_array != 0) & (img_flatten_array != 1)] 
        file_name = nifti_path.split('\\')[-1].rstrip('.nii.gz')
        hdr = img.header
        raw = hdr.structarr		

        temp_dict['filePath'] = nifti_path
        temp_dict['volumeOfVoxel'] = f'{volume_unit}mm3'
        temp_dict['spacing'] = f'{sx}mm x {sy}mm x {sz}mm'
        temp_dict['imgAffineMetrix'] = np.round(img.affine)
        temp_dict['fileName'] = file_name
        temp_dict['data_dtype'] = img.get_data_dtype()
        temp_dict['niftiImgShape'] = img.shape
        temp_dict['XYZTunits'] = hdr.get_xyzt_units()
        temp_dict['hdrRaw'] = raw
        temp_dict['3dArrayMean'] = img_array.mean()
        temp_dict['3dArrayStd'] = img_array.std()
        temp_dict['3dArrayMin'] = img_array.min()
        temp_dict['3dArrayMax'] = img_array.min()
        temp_dict['isUniqueValues'] = np.unique(img_flatten_array, return_counts=True)[0]
        # hdr_info = save_print_instance(hdr)
        # temp_dict['img_affine_metrix(raw value)'] = img.affine
        # temp_dict['img_affine_metrix(raw value)'] = img.affine
        # temp_dict['hdr_info'] = hdr_info.strip("<class 'nibabel.nifti1.Nifti1Header'> object, ")
        if is_binary: 
            temp_dict['exceptionValueCountInBinary'] = abnormal_quadrant_count.size
            temp_dict['(quadrant_count)voxelVolumeEstimation'] = n_count(img_array) * volume_unit
            temp_dict['(quadrant_count)topBackLeft'] = n_count(img_array[center_x:, :center_y, center_z:])
            temp_dict['(quadrant_count)topBackRight'] = n_count(img_array[:center_x, :center_y, :center_z])
            temp_dict['(quadrant_count)topFrontLeft'] = n_count(img_array [:center_x, center_y:, center_z:])
            temp_dict['(quadrant_count)topFrontRight'] = n_count(img_array [:center_x , center_y:, :center_z])
            temp_dict['(quadrant_count)bottomBackLeft'] = n_count(img_array[center_x:, :center_y, center_z:])
            temp_dict['(quadrant_count)bottomBackRight'] = n_count(img_array[center_x:, :center_y, center_z])
            temp_dict['(quadrant_count)bottmoFrontLeft'] = n_count(img_array[center_x:, center_y:, center_y:])
            temp_dict['(quadrant_count)bottomFrontRight'] = n_count(img_array[center_x:, center_y:, :center_z])
            # temp_dict['(quadrant_count)bottomFrontRight +- 10'] = n_count(img_array[center_x-10:center_x+10, center_y-10:center_y+10, center_z-10:center_z+10])
        total_dict[i] = temp_dict
    df_edanif = pd.DataFrame(total_dict).T
    df_edanif.to_csv(save_path, encoding='utf-8-sig', index=False)

    return df_edanif

