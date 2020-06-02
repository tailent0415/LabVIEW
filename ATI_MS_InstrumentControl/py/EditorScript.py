import math
import sys
import numpy
import scipy
import signalProcess as sp
import signalProcessOfGPU as gsp
import graphConfigOfEditor
from subFunc import showState, show, Show

def main( data, showMsg, errMsg ):
    showObj = showState()
    PriPlt = graphConfigOfEditor.init( 'pri', data[1] )
    PeakPlt = graphConfigOfEditor.init( 'peak', data[1] )
    processStartIndex = 16
    try:
#__startpoint__
        PriPlt = sp.PltNeg( PriPlt )
        PeakPlt,PriPlt = sp.FindPeak( PeakPlt, PriPlt, kwidth=5e-3, iteration=30, ampTh=0.0005 )
#__endpoint__
        showMsg.append( showObj.getShowMsg() )
        result = transTuple( data[0], PriPlt, PeakPlt )
        return(  result );
    except Exception:
        errMsg.append( str(sys.exc_info()[0]) )
        errMsg.append( str(sys.exc_info()[1]) )
        errMsg.append( str(sys.exc_info()[-1].tb_lineno - processStartIndex) )
        return []

def transTuple( StartTime, PriPlt, PeakPlt ):
    ScanData = pkgScanData( PriPlt.ScanSig )
    PeakData = pkgPeakData( PeakPlt.PeakInfo )
    result = ( StartTime,
               ScanData,
               PriPlt.mzGraph.xlabel,
               PriPlt.mzGraph.ylabel,
               PeakData )
    return result

### package scan data
def pkgScanData( data ):
    scanData=[]
    for sig in data:
        if type( sig.xdata ) != list:
            sig.xdata = sig.xdata.tolist()
        if type( sig.ydata ) != list:
            sig.ydata = sig.ydata.tolist()
        if type( sig.beta ) != list:
            sig.beta = sig.beta.tolist()
        scanTuple = ( sig.dt, sig.xdata, sig.ydata, sig.beta ) 
        scanData.append( scanTuple )
    return scanData

### package peak information data
def pkgPeakData( data ):
    peakData=[]
    for sig in data:
        if type( sig.xLdata ) != list:
            sig.xLdata = sig.xLdata.tolist()
        if type( sig.xCdata ) != list:
            sig.xCdata = sig.xCdata.tolist()
        if type( sig.xRdata ) != list:
            sig.xRdata = sig.xRdata.tolist()
        if type( sig.baseline ) != list:
            sig.baseline = sig.baseline.tolist()
        if type( sig.halfHeight ) != list:
            sig.halfHeight = sig.halfHeight.tolist()
        peakTuple = ( sig.xLdata, sig.xCdata, sig.xRdata, sig.baseline, sig.halfHeight )
        peakData.append( peakTuple )
    return peakData