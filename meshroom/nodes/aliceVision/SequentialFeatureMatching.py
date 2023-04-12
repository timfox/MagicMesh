__version__ = "2.0"

from meshroom.core import desc


class SequentialFeatureMatching(desc.AVCommandLineNode):
    commandLine = 'aliceVision_sequentialFeatureMatching {allParams}'
    size = desc.DynamicNodeSize('input')
    parallelization = desc.Parallelization(blockSize=20)
    commandLineRange = '--rangeStart {rangeStart} --rangeSize {rangeBlockSize}'

    category = 'Sparse Reconstruction'
    documentation = '''
This node performs the matching of all features between the candidate image pairs.
For each image with a given frame ID fid1, it is matched with all images with a given frame ID fid2 where fid1 < fid2, sequentially, until the matching fails.

It is performed in 2 steps:

 1/ **Photometric Matches**

It performs the photometric matches between the set of features descriptors from the 2 input images.
For each feature descriptor on the first image, it looks for the 2 closest descriptors in the second image and uses a relative threshold between them.
This assumption kill features on repetitive structure but has proved to be a robust criterion.

 2/ **Geometric Filtering**

It performs a geometric filtering of the photometric match candidates.
It uses the features positions in the images to make a geometric filtering by using epipolar geometry in an outlier detection framework
called RANSAC (RANdom SAmple Consensus). It randomly selects a small set of feature correspondences and compute the fundamental (or essential) matrix,
then it checks the number of features that validates this model and iterate through the RANSAC framework.

## Online
[https://alicevision.org/#photogrammetry/feature_matching](https://alicevision.org/#photogrammetry/feature_matching)
'''

    inputs = [
        desc.File(
            name='input',
            label='SfMData',
            description='SfMData file.',
            value='',
            uid=[0],
        ),
        desc.ListAttribute(
            elementDesc=desc.File(
                name="featuresFolder",
                label="Features Folder",
                description="",
                value="",
                uid=[0],
            ),
            name="featuresFolders",
            label="Features Folders",
            description="Folder(s) containing the extracted features and descriptors."
        ),
        desc.ChoiceParam(
            name='describerTypes',
            label='Describer Types',
            description='Describer types used to describe an image.',
            value=['dspsift'],
            values=['sift', 'sift_float', 'sift_upright', 'dspsift', 'akaze', 'akaze_liop', 'akaze_mldb', 'cctag3', 'cctag4', 'sift_ocv', 'akaze_ocv', 'tag16h5'],
            exclusive=False,
            uid=[0],
            joinChar=',',
        ),
        desc.ChoiceParam(
            name='verboseLevel',
            label='Verbose Level',
            description='verbosity level (fatal, error, warning, info, debug, trace).',
            value='info',
            values=['fatal', 'error', 'warning', 'info', 'debug', 'trace'],
            exclusive=True,
            uid=[],
        )
    ]
    outputs = [
        desc.File(
            name='output',
            label='Matches Folder',
            description='Path to a folder in which computed matches will be stored.',
            value=desc.Node.internalFolder,
            uid=[],
        ),
    ]
