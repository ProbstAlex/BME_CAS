import numpy as np
from scipy import ndimage
import queue


def region_grow(image, seed_point):
    """
    Performs a region growing on the image from seed_point
    :param image: An 3D grayscale input image
    :param seed_point: The seed point for the algorithm
    :return: A 3D binary segmentation mask with the same dimensions as image
    """
    segmentation_mask = np.zeros(image.shape, np.bool)
    z, y, x = seed_point 
    threshold = image[z, y, x]
    print('segmenting at ({0}, {1}, {2}) is {3}'.format(x, y, z, threshold))

    ## TODO: choose a lower and upper threshold
    threshold_lower = threshold - 100
    threshold_upper = threshold + 100
    _segmentation_mask = (np.greater(image, threshold_lower)
                          & np.less(image, threshold_upper)).astype(np.bool)
    structure = np.ones((2, 2, 2))

    ## TODO: post-process the image with a morphological filter

    to_check = queue.Queue()
    check_point = np.asarray([z, y, x], dtype=np.uint32)
    to_check.put(check_point)

    while not to_check.empty():
        check_point = to_check.get()
        if _segmentation_mask[check_point[0], check_point[1], check_point[2]]:
            _segmentation_mask[check_point[0], check_point[1], check_point[2]] = False
            segmentation_mask[check_point[0], check_point[1], check_point[2]] = 1

            
            # These for loops will visit all the neighbors of a voxel and see if
            # they belong to the region
            for ix in range(-1, 2, 2):
                for iy in range(-1, 2, 2):
                    for iz in range(-1, 2, 2):
                        ## TODO: implement the code which checks whether the current
                        ## voxel (new_check_point) belongs to the region or not
                        if not (iz == 0 and ix == 0 and iy == 0):
                            new_check_point = check_point + np.asarray([iz, iy, ix], dtype=np.uint32)
                            if (image[new_check_point[0], new_check_point[1], new_check_point[2]]<threshold_upper and 
                            image[new_check_point[0], new_check_point[1], new_check_point[2]]>threshold_lower):
                                segmentation_mask[new_check_point[0], new_check_point[1], new_check_point[2]]=1
                        ## TODO: implement a stop criteria such that the algorithm
                        ## doesn't check voxels which are too far away
                                if ( 
                                    new_check_point[0] + 1 < image.shape[0] and
                                    new_check_point[1] + 1 < image.shape[1] and
                                    new_check_point[2] + 1 < image.shape[2] and
                                    new_check_point[0] - 1 > 0 and
                                    new_check_point[1] - 1 > 0 and
                                    new_check_point[2] - 1 > 0
                                ):
                                    to_check.put(new_check_point)

    # Your code goes here
    structure = np.ones((2, 2, 2))
    segmentation_mask = ndimage.binary_closing(segmentation_mask, structure=structure).astype(np.bool)
    print('finished')
    return segmentation_mask
