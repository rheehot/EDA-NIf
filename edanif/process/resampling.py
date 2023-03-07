import numpy as np
import os
import SimpleITK as sitk


def resampling(modified_path, reference_path, save_folder, interpolator=sitk.sitkLinear):
    os.makedirs(save_folder, exist_ok=True)
    info = os.path.basename(reference_path).split('_')
    filename = info[0] + '_' + info[1]
    modified_nii_img = sitk.ReadImage(modified_path, imageIO="NiftiImageIO")
    reference_nii_img = sitk.ReadImage(reference_path, imageIO="NiftiImageIO")
    resampler = sitk.ResampleImageFilter()
    resampler.SetOutputOrigin(modified_nii_img.GetOrigin())
    resampler.SetOutputDirection(modified_nii_img.GetDirection())
    resampler.SetSize(reference_nii_img.GetSize())
    resampler.SetOutputSpacing(reference_nii_img.GetSpacing())
    resampler.SetInterpolator(interpolator)
    resampled_modified_nii_img = resampler.Execute(modified_nii_img)

    sitk.WriteImage(resampled_modified_nii_img, f'{save_folder}/{filename}_resampled_to_mask.nii')
    
    return resampled_modified_nii_img 


def resample_fixedsize_fixedspacing (nifti_file_path: str, save_folder_path: str, interpolation: str, new_size: int, new_spacing: list) -> None:
    '''
    #img_sitk : sitk image (3D)
    #interppolation: sitk.sitkLinear
    #new_size : 64
    #new_spacing: [1,1,1]
    
    Example Code:
      resample_fixedsize_fixedspacing(nii_list[0], './result', sitk.sitkLinear, 64, [1,1,1])
    '''
    img_sitk = sitk.ReadImage(nifti_file_path)
    # img_array = sitk.GetArrayFromImage(img_sitk)
    try:
        file_name = nifti_file_path.split('\\')[-1].rstrip('.nii.gz')
    except:
        file_name = nifti_file_path.split('/')[-1].rstrip('.nii.gz')
    dimension = img_sitk.GetDimension()
    reference_size = [new_size,new_size,new_size]
    reference_physical_size = np.zeros(img_sitk.GetDimension())
    reference_physical_size[:] = [(sz-1)*spc if sz*spc>mx  else mx for sz,spc,mx in zip(img_sitk.GetSize(), img_sitk.GetSpacing(), reference_physical_size)]
    reference_direction = img_sitk.GetDirection()
    reference_origin = img_sitk.GetOrigin()
    reference_image = sitk.Image(reference_size, img_sitk.GetPixelIDValue())
    reference_image.SetOrigin(reference_origin)
    reference_image.SetSpacing(new_spacing)
    reference_image.SetDirection(reference_direction)
    reference_center = np.array(reference_image.TransformContinuousIndexToPhysicalPoint(np.array(reference_image.GetSize())/2.0))
    transform = sitk.AffineTransform(dimension)
    transform.SetMatrix(img_sitk.GetDirection())
    transform.SetTranslation(np.array(img_sitk.GetOrigin()) - reference_origin)
    centering_transform = sitk.TranslationTransform(dimension)
    img_center = np.array(img_sitk.TransformContinuousIndexToPhysicalPoint(np.array(img_sitk.GetSize())/2.0))
    centering_transform.SetOffset(np.array(transform.GetInverse().TransformPoint(img_center) - reference_center))
    centered_transform = sitk.CompositeTransform([centering_transform,transform])
    new_img = sitk.Resample(img_sitk, reference_image, centered_transform, interpolation, 0.0)
    os.makedirs(save_folder_path, exist_ok=True)
    sitk.WriteImage(new_img, f'{save_folder_path}/{file_name}_resampled.nii.gz')

    return None


def make_isotropic(image, interpolator = sitk.sitkLinear, spacing = None):
    '''
    Many file formats (e.g. jpg, png,...) expect the pixels to be isotropic, same
    spacing for all axes. Saving non-isotropic data in these formats will result in
    distorted images. This function makes an image isotropic via resampling, if needed.
    Args:
        image (SimpleITK.Image): Input image.
        interpolator: By default the function uses a linear interpolator. For
                      label images one should use the sitkNearestNeighbor interpolator
                      so as not to introduce non-existant labels.
        spacing (float): Desired spacing. If none given then use the smallest spacing from
                         the original image.
    Returns:
        SimpleITK.Image with isotropic spacing which occupies the same region in space as
        the input image.
    '''
    original_spacing = image.GetSpacing()
    # Image is already isotropic, just return a copy.
    if all(spc == original_spacing[0] for spc in original_spacing):
        return sitk.Image(image)
    # Make image isotropic via resampling.
    original_size = image.GetSize()
    if spacing is None:
        spacing = min(original_spacing)
    new_spacing = [spacing]*image.GetDimension()
    new_size = [int(round(osz*ospc/spacing)) for osz, ospc in zip(original_size, original_spacing)]
    return sitk.Resample(image, new_size, sitk.Transform(), interpolator,
                         image.GetOrigin(), new_spacing, image.GetDirection(), 0, # default pixel value
                         image.GetPixelID())