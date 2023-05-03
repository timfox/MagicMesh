__version__ = "2.0"

from meshroom.core import desc


class PairsEstimations(desc.AVCommandLineNode):
    commandLine = 'aliceVision_pairsEstimations {allParams}'
    size = desc.DynamicNodeSize('input')
    
    parallelization = desc.Parallelization(blockSize=25)
    commandLineRange = '--rangeStart {rangeStart} --rangeSize {rangeBlockSize}'

    category = 'Sparse Reconstruction'
    documentation = '''
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
        desc.File(
            name='tracksFilename',
            label='Tracks file',
            description='Tracks file.',
            value='',
            uid=[0],
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
            description='Verbosity level (fatal, error, warning, info, debug, trace).',
            value='info',
            values=['fatal', 'error', 'warning', 'info', 'debug', 'trace'],
            exclusive=True,
            uid=[],
        )
    ]

    outputs = [
        desc.File(
            name='output',
            label='Pairs Infos',
            description='Path to the output Pairs info file',
            value=desc.Node.internalFolder + 'sfm.json',
            uid=[],
        )
    ]
