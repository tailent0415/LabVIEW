import classFPGACmdCode as clsCode
import classFPGAActionMethod as clsMethod
import tableBetaAndQ
import math
from checkValueType import checkValue, checkList
from scipy.interpolate import interp1d

# ================== Initialization ========================= #
priDataCode = clsCode.priRFDataSet()
auxDataCode = clsCode.auxWfmDataSet()
actEventCode = clsMethod.mzMethod()
constBetaArr = tableBetaAndQ.getBetaList()
constQArr = tableBetaAndQ.getQList()

# ===========================Q And Beta================================ #
def qOfBeta( beta=1 ):
    checkValue('The type of beta must be int or float', beta, (int, float), 1e-10, 1)
    curveEquation = interp1d( constBetaArr, constQArr, kind='cubic' )
    return float(curveEquation(beta))

def betaOfQ( q_z=0.908046333734577 ):
    checkValue('The type of q_z must be int or float', q_z, (int, float), 1e-10, 1)
    curveEquation = interp1d( constQArr, constBetaArr, kind='cubic' )
    return float(curveEquation(q_z))


# ===========================Mathieu================================ #
class mathieu:
    def __init__(self):
        self.ec = 1.6021766208000001E-19 * 8  # 1.6021766208000001E-19 is Elementary Charge
        self.atomicMZ = 1.66053892173E-27  # 1.66053892173E-27 is Atomic mass
        self.twoPi = math.pi * 2

    def GetFreq(self, mz, amp, betaz):
        checkValue('input MZ is incorrect', mz, (int, float), 0, float("inf") )
        checkValue('input Amp is incorrect', amp, (int, float), 0, 100000 )
        checkValue('input Betaz is incorrect', betaz, (int, float), 0, 1 )
        maxAmp, r0, z0 = actEventCode.getHeaderParam()

        algorithm1 = (math.pow(z0, 2) * 2 + math.pow(r0, 2)) * 1e-6
        algorithm2 = self.atomicMZ * mz
        q_z = qOfBeta( betaz )

        freq = math.sqrt((self.ec * amp) / (algorithm1 * algorithm2 * q_z)) / self.twoPi
        return float(freq)

    def GetAmp(self, mz, freq, betaz):
        checkValue('input MZ is incorrect', mz, (int, float), 0, float("inf") )
        checkValue('input Freq is incorrect', freq, (int, float), 0, 2000000 )
        checkValue('input Betaz is incorrect', betaz, (int, float), 0, 1 )
        maxAmp, r0, z0 = actEventCode.getHeaderParam()

        algorithm1 = (math.pow(z0, 2) * 2 + math.pow(r0, 2)) * 1e-6
        algorithm2 = self.atomicMZ * mz
        algorithm3 = math.pow(freq * self.twoPi, 2)

        q_z = qOfBeta( betaz )

        amp = (algorithm1 * algorithm2 * algorithm3 * q_z) / self.ec
        return float(amp)

    def GetBeta(self, mz, amp, freq):
        checkValue('input MZ is incorrect', mz, (int, float), 0, float("inf") )
        checkValue('input Amp is incorrect', amp, (int, float), 0, 100000 )
        checkValue('input Freq is incorrect', freq, (int, float), 0, 2000000 )
        maxAmp, r0, z0 = actEventCode.getHeaderParam()

        algorithm1 = (math.pow(z0, 2) * 2 + math.pow(r0, 2)) * 1e-6
        algorithm2 = self.atomicMZ * mz
        algorithm3 = math.pow(freq * self.twoPi, 2)

        q_z = (self.ec * amp) / (algorithm1 * algorithm2 * algorithm3)

        beta = betaOfQ( q_z )
        return float(beta)

    def GetMZ(self, amp, freq, betaz):
        checkValue('input Amp is incorrect', amp, (int, float), 0, 100000 )
        checkValue('input Freq is incorrect', freq, (int, float), 0, 2000000 )
        checkValue('input Betaz is incorrect', betaz, (int, float), 0, 1 )
        maxAmp, r0, z0 = actEventCode.getHeaderParam()

        algorithm1 = (math.pow(z0, 2) * 2 + math.pow(r0, 2)) * 1e-6
        algorithm3 = math.pow(freq * self.twoPi, 2)
        q_z = qOfBeta( betaz )

        MZ = ((self.ec * amp) / (algorithm1 * algorithm3 * q_z)) / self.atomicMZ
        return float(MZ)


# ===========================MZ Event================================ #
class mzEvent:
    def __init__(self):
        self.maxAmp = 330
        self.r0 = 7.071
        self.z0 = 10

    def setPriDataCode(self, cycIncrement, amplitude, totalTicks, conjTicks, repeat):
        priDataCode.addPriData(cycIncrement, amplitude, totalTicks, conjTicks, repeat)

    def setAuxData(self, intenPls, auxBias, auxTicks, repeat):
        auxDataCode.addAuxData(intenPls, auxBias, auxTicks, repeat)

    def mzHeader(self, maxAmp, r0, z0):
        actEventCode.setHeader(maxAmp, r0, z0)
        self.maxAmp = maxAmp
        self.r0 = r0
        self.z0 = z0

    def mzIdle(self):
        actEventCode.actIdle()

    def mzWait(self, timeOut):
        actEventCode.actWait(timeOut)

    def mzDDSStart(self, iniCycle):
        actEventCode.actDDSStart(iniCycle)

    @property
    def pkgResponse(self):
        codeTuple = (actEventCode.getActCmd, priDataCode.getPriDataCode, auxDataCode.getAuxDataCode)
        return codeTuple
