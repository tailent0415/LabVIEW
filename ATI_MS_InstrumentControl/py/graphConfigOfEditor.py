import numpy
def init(sigType, data=None):
    if data is None:
        data = []
    if sigType == 'pri':
        struct = priDisplay( data )
    else:
        struct = peakDisplay( data )
    return struct

class priDisplay:
    def __init__(self, data):
        self.ScanSig = []
        for dataIdx in data:
            self.ScanSig.append( scanAttr( dataIdx ) )
        self.mzGraph = xyLable( 'm/z (Th)', 'Intensity (V)' )

class peakDisplay:
    def __init__(self, data):
        self.PeakInfo = []
        for dataIdx in data:
            self.PeakInfo.append( peakAttr( ( [], [], [], [], [] ) ) )

class xyLable:
    def __init__(self, xlableStr, ylabelStr ):
        self.xlabel = xlableStr
        self.ylabel = ylabelStr

class scanAttr:
    def __init__(self, data ):
        self.dt = data[0]
        self.xdata = data[1]
        self.ydata = data[2]
        self.beta = data[3]

class peakAttr:
    def __init__(self, data ):
        self.xLdata = data[0]
        self.xCdata = data[1]
        self.xRdata = data[2]
        self.baseline = data[3]
        self.halfHeight = data[4]

