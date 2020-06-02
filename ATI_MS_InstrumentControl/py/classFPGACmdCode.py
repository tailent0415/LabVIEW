from typing import List, Any
import numpy as np


##uint type classification
def typeNum(typeClass):
    className = {
        'uint8': 0,
        'uint16': 1,
        'uint32': 2,
    }
    return className.get(typeClass, None)


##join numbers of uint type
def uintMerge(hi, lo):
    assert isinstance( hi, ( np.uint8, np.uint16, np.uint32 ) ), 'The type of hi must be int'
    assert isinstance( lo, ( np.uint8, np.uint16, np.uint32 ) ), 'The type of hi must be int'
    mergeVal = None
    formatNum = typeNum(type(hi).__name__)
    if formatNum is None:
        return None
    if formatNum == 0:
        mergeVal = (hi << 8) | np.uint8(lo)
        mergeVal = np.uint16(mergeVal)
    if formatNum == 1:
        mergeVal = (hi << 16) | np.uint16(lo)
        mergeVal = np.uint32(mergeVal)
    if formatNum == 2:
        mergeVal = (hi << 32) | np.uint32(lo)
        mergeVal = np.uint64(mergeVal)
    return mergeVal


##Primary RF Data
class priRFDataSet:
    _priCode: List[Any]

    def __init__(self):
        self._priCode = []

    def addPriData(self, cycIncrement, amplitude, totalTicks, conjTicks, repeat):
        assert isinstance(cycIncrement, int), 'The type of cycIncrement must be int'
        assert isinstance(amplitude, int), 'The type of amplitude must be int'
        assert isinstance(totalTicks, int), 'The type of totalTicks must be int'
        assert isinstance(conjTicks, int), 'The type of conjTicks must be int'
        assert isinstance(repeat, int), 'The type of repeat must be int'
        self._priCode.append(uintMerge(np.uint32(cycIncrement), np.uint32(amplitude)))
        self._priCode.append(uintMerge(np.uint32(totalTicks), uintMerge(np.uint16(conjTicks), np.uint16(repeat))))

    @property
    def getPriDataCode(self):
        return self._priCode


##Auxiliary Waveform Data
class auxWfmDataSet:
    _auxCode: List[Any]

    def __init__(self):
        self._auxCode = []

    def addAuxData(self, intenPls, auxBias, auxTicks, repeat):
        assert isinstance(intenPls, int), 'The type of intenPls must be int'
        assert isinstance(auxBias, int), 'The type of auxBias must be int'
        assert isinstance(auxTicks, int), 'The type of auxTicks must be int'
        assert isinstance(repeat, int), 'The type of repeat must be int'
        self._auxCode.append(uintMerge(np.uint32(0), uintMerge(np.uint16(intenPls), np.uint16(auxBias))))
        self._auxCode.append(uintMerge(uintMerge(np.uint16(0), np.uint16(auxTicks)), np.uint32(repeat)))

    @property
    def getAuxDataCode(self):
        return self._auxCode


##FPGA Actions Data
class actionDataSet:
    _actCode: List[Any]

    def __init__(self):
        self._actCode = []

    def addActCmd(self, majorActCode, subActCode, stateVal, setVal):
        assert isinstance(majorActCode, int), 'The type of majorActCode must be int'
        assert isinstance(subActCode, int), 'The type of subActCode must be int'
        assert isinstance(stateVal, int), 'The type of stateVal must be int'
        assert isinstance(setVal, int), 'The type of setVal must be int'
        self._actCode.append(uintMerge(uintMerge(uintMerge(np.uint8(majorActCode), np.uint8(subActCode)),
                                                 np.uint16(stateVal)), np.uint32(setVal)
                                      )
                             )

    @property
    def getActCmd(self):
        return self._actCode
