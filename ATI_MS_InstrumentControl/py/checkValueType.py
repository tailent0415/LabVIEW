def checkValue( warningStr, tagValue, dataType, minValue=float("inf"), maxValue=float("-inf") ):
    assert isinstance( tagValue, dataType ), warningStr
    try:
        if dataType.__name__ == 'bool':
            return True
    except Exception as e:
        if minValue > maxValue:
            raise ValueError('wrong range setting')
        if minValue <= tagValue <= maxValue:
            return True
        raise ValueError( 'the value must be between ' + str( minValue ) + ' and ' + str( maxValue ) )

def checkList( warningStr, tagArr, dataType, minValue=float("inf"), maxValue=float("-inf"), minArr=None, maxArr=None ):
    assert isinstance( tagArr, list ), warningStr
    if minArr > maxArr:
        raise ValueError( 'wrong array range setting' )
    try:
        if dataType.__name__ == 'bool':
            for val in tagArr:
                checkValue( warningStr, val, dataType )
            return True
    except Exception as e:
        if not minArr <= len(tagArr) <= maxArr:
            raise ValueError( 'the array size must be between ' + str( minArr ) + ' and ' + str( maxArr ) )
        for val in tagArr:
            checkValue(warningStr, val, dataType, minValue, maxValue)
        return True
