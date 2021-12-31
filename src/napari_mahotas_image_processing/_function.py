import numpy as np
from napari_plugin_engine import napari_hook_implementation
from napari_tools_menu import register_function
from napari_time_slicer import time_slicer, slice_by_slice
import napari
from napari.types import ImageData, LabelsData



@napari_hook_implementation
def napari_experimental_provide_function():
    return [
        gaussian_blur,
        threshold_otsu,
        connected_component_labeling,
        sobel_edge_detector,
        binary_fill_holes,
        seeded_watershed,
        split_touching_objects,
        euclidean_distance_map
    ]


@register_function(menu="Filtering / noise removal > Gaussian (n-mahotas)")
@time_slicer
def gaussian_blur(image:ImageData, sigma: float = 1, viewer: napari.Viewer = None) -> ImageData:
    """
    Filters an image using a Gaussian kernel with a given sigma.

    See also
    --------
    ..[0] https://mahotas.readthedocs.io/en/latest/api.html#mahotas.gaussian_filter
    """
    import mahotas as mh
    return mh.gaussian_filter(image, sigma)


def _8bit(image):
    return (image / image.max() * 255).astype(np.uint8)


@register_function(menu="Segmentation / binarization > Threshold (Otsu et al 1979, n-mahotas)")
@time_slicer
def threshold_otsu(image:ImageData, viewer: napari.Viewer = None) -> LabelsData:
    """
    Thresholds an image using Otsu's technique

    See also
    --------
    ..[0] https://mahotas.readthedocs.io/en/latest/api.html#mahotas.otsu
    """
    import mahotas as mh
    image_8bit = _8bit(image)
    t = mh.otsu(image_8bit)
    return image_8bit > t

@register_function(menu="Segmentation / labeling > Connected component labeling (n-mahotas)")
@time_slicer
def connected_component_labeling(binary_image: LabelsData, viewer: napari.Viewer = None) -> LabelsData:
    """
    Label connected regions in a binary image

    See also
    --------
    ..[0] https://mahotas.readthedocs.io/en/latest/api.html#mahotas.label
    """
    labeled, nr_objects = mh.label(binary_image)
    return labeled

@register_function(menu="Filtering / edge enhancement > Sobel edge detection (slice-by-slice, n-mahotas)")
@time_slicer
def sobel_edge_detector(image:ImageData, viewer: napari.Viewer = None) -> ImageData:
    """
    Enhances edges using a sobel operator

    See also
    --------
    ..[0] https://mahotas.readthedocs.io/en/latest/api.html#mahotas.sobel
    """
    import mahotas as mh
    return mh.sobel(image, just_filter=True)

@register_function(menu="Segmentation post-processing > Binary fill holes (slice_by_slice, n-mahotas)")
@slice_by_slice
@time_slicer
def binary_fill_holes(binary_image:LabelsData, viewer: napari.Viewer = None) -> LabelsData:
    """
    Fill holes in a binary image

    See also
    --------
    ..[0] https://mahotas.readthedocs.io/en/latest/api.html#mahotas.close_holes
    """
    import mahotas as mh
    return mh.close_holes(binary_image)


@register_function(menu="Segmentation / labeling > Seeded watershed (n-mahotas)")
@time_slicer
def seeded_watershed(image:ImageData, labeled_seeds:LabelsData, viewer: napari.Viewer = None) -> LabelsData:
    """
    Labels all pixels in an image by flooding intensity valleys in a given image starting from labeled region seeds.

    See also
    --------
    ..[0] https://mahotas.readthedocs.io/en/latest/api.html#mahotas.cwatershed
    """
    import mahotas as mh
    labels = mh.cwatershed(image, labeled_seeds)
    return labels

@register_function(menu="Measurement > Euclidean distance map (n-mahotas)")
@time_slicer
def euclidean_distance_map(binary_image:LabelsData, viewer: napari.Viewer = None) -> LabelsData:
    """
    Draws a Euclidean distance map from a binary image. Non-zero values in th binary image will be
    replaced by the distance to the next zero pixel.

    See also
    --------
    ..[0] https://en.wikipedia.org/wiki/Distance_transform
    """
    import mahotas as mh
    return mh.distance(binary_image)

def _sobel_3d(image):
    from scipy import ndimage as ndi

    kernel = np.asarray([
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ], [
            [0, 1, 0],
            [1, -6, 1],
            [0, 1, 0]
        ], [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
    ])
    return ndi.convolve(image, kernel)


@register_function(menu="Segmentation post-processing > Split touching objects (n-mahotas)")
@time_slicer
def split_touching_objects(binary:LabelsData, sigma:float=3.5, viewer: napari.Viewer = None) -> LabelsData:
    """
    Takes a binary image and draws cuts in the objects similar to the ImageJ watershed algorithm.

    See also
    --------
    .. [0] https://imagej.nih.gov/ij/docs/menus/process.html#watershed
    """
    import mahotas as mh

    binary = _8bit(np.asarray(binary))

    # typical way of using scikit-image watershed
    distance = mh.distance(binary)
    blurred_distance = mh.gaussian_filter(distance, sigma=sigma)
    fp = np.ones((3,) * binary.ndim)
    markers, num_labels = mh.label(mh.regmax(blurred_distance, Bc=fp))
    labels = mh.cwatershed(-blurred_distance, markers)

    # identify label-cutting edges
    if len(binary.shape) == 2:
        edges = mh.sobel(labels, just_filter=True)
        edges2 = mh.sobel(binary, just_filter=True)
    else:  # assuming 3D
        edges = _sobel_3d(labels)
        edges2 = _sobel_3d(binary)

    almost = np.logical_not(np.logical_xor(edges != 0, edges2 != 0)) * binary
    return mh.open(almost) != 0
