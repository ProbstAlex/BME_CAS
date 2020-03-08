import argparse
import numpy as np
import nibabel as nib
import numpy as np
import os
from scipy import ndimage
import sys


LABELS = {
    "Liver": 1,
    "Tumor": 2
}

def calc_volume(image, label, spacing):
    """
    Calculates the volume of an object with the label
    :param image: A 3D segmented volume
    :param label: The label for which the volume shall be computed
    :param spacing: The voxel spacing of the image
    :return: The volume of the object
    """
    
    #TODO: implement code to calculate the volume in mL    
    count = np.count_nonzero(input_image == label)
    volume = abs(count*spacing[0]*spacing[1]*spacing[2])/1000
    
    return volume

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate volume')
    parser.add_argument('--case-id', type=str, help='...')
    parser.add_argument('--dataset-path', type=str, help='...')
    args = parser.parse_args()
    print(args)

    # CORRECTION
    # have to call format argumnt with args.case_id, not with only case.id
    filename = 'predictions_{0}.nii'.format(args.case_id)
    input_image = os.path.join(args.dataset_path, filename)

    input_image = nib.load(input_image)
    
    # CORRECTION
    # the spacing has to be extracted here from the input_image meta data, before converted to memmap numpy array
    spacing = [input_image.affine[0][0], input_image.affine[1][1], input_image.affine[2][2]]
    
    input_image = input_image.get_fdata().astype(np.float32)
    #input_image.tofile('input_image.txt', sep=" ",format="%s")
    #unique, counts = np.unique(input_image, return_counts=True)
    #print(dict(zip(unique, counts)))
    
    volume_liver = calc_volume(input_image, LABELS["Liver"], spacing)
    volume_tumors = calc_volume(input_image, LABELS["Tumor"], spacing)
    
    print("Liver volume: {0}".format(volume_liver))
    print("Tumor volume: {0}".format(volume_tumors))
