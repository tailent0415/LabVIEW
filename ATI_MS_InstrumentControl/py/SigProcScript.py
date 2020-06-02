import math
import sys
import numpy
import scipy
import signalProcess as sp
import signalProcessOfGPU as gsp
import graphConfig
from classShowFunc import show, Show, getShowArr

def main( data, showMsg, errMsg ):
    PriPlt = graphConfig.init( 'pri', data[1] )
    SecPlt = graphConfig.init( 'sec', data[2] )
    processStartIndex = 15
    try:
#__startpoint__
#__endpoint__
        showMsg.append( getShowArr() )
        result = transTuple( data[0], PriPlt, SecPlt )
        return(  result );
    except Exception:
        errMsg.append( str(sys.exc_info()[0]) );
        errMsg.append( str(sys.exc_info()[1]) );
        errMsg.append( str(sys.exc_info()[-1].tb_lineno - processStartIndex) );
        return []

def transTuple( StartTime, PriPlt, SecPlt ):

    ScanData = pkgScanData( PriPlt.ScanSig )
    IonData = pkgIonData( SecPlt.IonSig )
    result = ( StartTime,
               ScanData,
               PriPlt.mzGraph.xlabel,
               PriPlt.mzGraph.ylabel,
               PriPlt.tGraph.xlabel,
               PriPlt.tGraph.ylabel,
               IonData,
               SecPlt.ionGraph.xlabel,
               SecPlt.ionGraph.ylabel )
    return result

def pkgScanData( sig ):
    scanData=[]
    for sig in sig:
        if type( sig.xdata ) != list:
            sig.xdata = sig.xdata.tolist()
        if type( sig.ydata ) != list:
            sig.ydata = sig.ydata.tolist()
            
        scanTuple = ( sig.dt, sig.xdata, sig.ydata, sig.beta ) 
        scanData.append( scanTuple )
        
    return scanData

def pkgIonData( sig ):
    ionData=[]
    for sig in sig:
        if type( sig.ydata ) != list:
            sig.ydata = sig.ydata.tolist()
            
        ionTuple = ( sig.dt, sig.ydata ) 
        ionData.append( ionTuple )

    return ionData