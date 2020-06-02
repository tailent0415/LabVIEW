import classFPGACmdCode

##FPGA Actions Command
class mzMethod( classFPGACmdCode.actionDataSet ):
    def __init__(self):
        super().__init__()
        self._maxAmp = 330
        self._r0 = 7.071
        self._z0 = 10

    def getHeaderParam(self):
        return self._maxAmp, self._r0, self._z0

    ##The FPGA waits for action
    def setHeader(self, maxAmp, r0, z0):
        assert isinstance( maxAmp, ( int, float) ), 'The type of maxAmp must be int or float'
        assert isinstance(r0, (int, float)), 'The type of r0 must be int or float'
        assert isinstance(z0, (int, float)), 'The type of z0 must be int or float'
        self._maxAmp = maxAmp
        self._r0 = r0
        self._z0 = z0

    ##The FPGA waits for action
    def actIdle(self):
        self.addActCmd( 0, 0, 0, 0 )

    ##Wait for a while
    def actWait(self, timeout):
        self.addActCmd( 1, 0, 0, timeout )

    ##Start and reset the DDS of the primary RF.
    def actDDSStart(self, iniCycle):
        self.addActCmd( 2, 0, 0, iniCycle )

    #Stop the DDS of primary RF.
    def actDDSStop(self):
        self.addActCmd( 3, 0, 0, 0 )

    #Start a data acquisition process.
    def actDAQStart(self, channelNum, sampleRate, length):
        self.addActCmd( 9, channelNum, sampleRate, length )

    #Update digital outputs.
    def actUpdDO(self, channelNum, func, val):
        self.addActCmd( 11, channelNum, func, val )

    #Update analogue outputs.
    def actUpdAO(self, channelNum, analogueVal):
        self.addActCmd( 12, channelNum, 0, analogueVal )

    #Update extended digital outputs.
    def actExtDO(self, channelNum, val):
        self.addActCmd( 13, channelNum, 0, val )

    #Update extended analogue outputs.
    def actExtAO(self, channelNum, analogueVal):
        self.addActCmd( 14, channelNum, 0, analogueVal )

    #.
    def actUpdFGen(self, func, val):
        self.addActCmd( 200, func, 0, val )

    def checkCode(self):
        return self.getActCmd()
