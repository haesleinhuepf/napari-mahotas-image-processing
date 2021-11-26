# napari-mahotas-image-processing (n-mahotas)

[![License](https://img.shields.io/pypi/l/napari-mahotas-image-processing.svg?color=green)](https://github.com/haesleinhuepf/napari-mahotas-image-processing/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-mahotas-image-processing.svg?color=green)](https://pypi.org/project/napari-mahotas-image-processing)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-mahotas-image-processing.svg?color=green)](https://python.org)
[![tests](https://github.com/haesleinhuepf/napari-mahotas-image-processing/workflows/tests/badge.svg)](https://github.com/haesleinhuepf/napari-mahotas-image-processing/actions)
[![codecov](https://codecov.io/gh/haesleinhuepf/napari-mahotas-image-processing/branch/main/graph/badge.svg)](https://codecov.io/gh/haesleinhuepf/napari-mahotas-image-processing)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-mahotas-image-processing)](https://napari-hub.org/plugins/napari-mahotas-image-processing)

Image processing based using the [Mahotas library](https://github.com/luispedro/mahotas) in [napari](https://napari.org)

## Usage



### Gaussian blur

Applies a [Gaussian blur](https://mahotas.readthedocs.io/en/latest/api.html#mahotas.gaussian_filter) to an
image. This might be useful for denoising, e.g. before applying the Threshold-Otsu method.

![img.png](docs/gaussian_blur.png)

### Otsu's threshold

Binarizes an image using [scikit-image's threshold Otsu algorithm](https://mahotas.readthedocs.io/en/latest/api.html#mahotas.otsu), also known as 
[Otsu's method](https://ieeexplore.ieee.org/document/4310076).

![img.png](docs/threshold_otsu.png)

### Split connected objects

In case objects stick together after thresholding, this tool might help.
It aims to deliver similar results as [ImageJ's watershed implementation](https://imagej.nih.gov/ij/docs/menus/process.html#watershed).

![img.png](docs/split_touching_objects.png)

### Connected component labeling

Takes a binary image and produces a label image with all separated objects labeled differently. Under the hood, it uses
[mahotas' label function](https://mahotas.readthedocs.io/en/latest/api.html#mahotas.label).

![img.png](docs/connected_component_labeling.png)

### Seeded watershed

Starting from an image showing high-intensity membranes and a seed-image where objects have been labeled,
objects are labeled that are constrained by the membranes. Hint: you may want to blur the membrane channel a bit in advance.

![img.png](docs/seeded_watershed.png)


----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

## Installation

Before installing this napari plugin, please [install `mahotas`](https://github.com/luispedro/mahotas#install), e.g. using conda:

```
conda config --add channels conda-forge
conda install mahotas
```

Afterwards, you can install `napari-mahotas-image-processing` via [pip]:

    pip install napari-mahotas-image-processing



To install latest development version :

    pip install git+https://github.com/haesleinhuepf/napari-mahotas-image-processing.git


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-mahotas-image-processing" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/haesleinhuepf/napari-mahotas-image-processing/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
