import user
import instr
import math
import sys
import numpy
import scipy
from mzProcess import mzEvent, mathieu
from classShowFunc import show, Show, getShowArr

def main( showMsg, errMsg ):
    MSProcess = mzEvent()
    Mathieu = mathieu()
    T = True
    F = False
    versionInfo = "2.6.0.1"
    fileName = "C:\\ATI_MS_InstrumentControl\\Method\\temp.arp"
    timeStamp = "356FA07E848"

    instr.MaxAmp=330.000000
    instr.RO=10.000000
    instr.ZO=7.071068
    instr.LasingPhase=0.000000
    instr.Bias_Pri=0.000000
    instr.Bias_Aux=0.000000
    instr.Bias_AO=[0.000000,0.000000,0.000000,0.000000]
    instr.Offset_MZ=0.000000
    processStartIndex = 29
    try:
#__startpoint__
        from scipy import stats
        
        r0 = 10
        z0 = 7.07107
        Vmax = 316
        MSProcess.Header( r0, z0, instr.MaxAmp );
        MSProcess.SetDAQ( 1, 0 );
        MSProcess.UpdDO( [1,1,1,1], [F,F,F,F] );
        MSProcess.UpdAO( [0,0,0,0], [0,0,0,0] )
        
        
        #the following script does voltage calibration
        
        RFbch1 = 0.0043  #0.0043 = 0V
        RFbch2 = 0.0037  #0.0037 = 0V
        RFbch3 = 0.0009  #0.0009 = 0V
        
        
        PRFCh={ 'ch1':{'a':1, 'b':0}}
        FRFCh1 = {'i':[-1.000, -0.660, -0.330, 0.0000, 0.330, 0.660, 1.000],
                  'o':[-2.996, -1.986, -1.004, -0.021, 0.959, 1.940, 2.952]}
        slope, intercept, r_value, p_value, std_err = stats.linregress(FRFCh1['i'],FRFCh1['o'])
        show('FRFCh1: slope='+str(slope)+', '+'i='+str(intercept)+', '+'r_sq='+str(r_value**2))
        PRFCh['ch1']['a']=slope
        PRFCh['ch1']['b']=intercept
        
        PAmp={  'Amp1':{'a':1, 'b':0},
                'Amp2':{'a':1, 'b':0},
                'Amp3':{'a':1, 'b':0}}
        
        
        FAmp1 = {'i':[-0.40, -0.30, -0.20, -0.10, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01],
                 'o':[36.90, 27.65, 18.40, 9.160, 8.230, 7.310, 6.350, 5.420, 4.540, 3.612, 2.689, 1.767, 0.843]}
        
        FAmp2 = {'i':[-0.40, -0.30, -0.20, -0.10, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01],
                 'o':[36.80, 27.58, 18.34, 9.120, 8.190, 7.270, 6.350, 5.520, 4.490, 3.576, 2.654, 1.733, 0.810]}
        
        FAmp3 = {'i':[-0.40, -0.30, -0.20, -0.10, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01],
                 'o':[36.93, 27.68, 18.46, 9.220, 8.300, 7.370, 6.450, 5.530, 4.610, 3.684, 2.762, 1.830, 0.893]}
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(FAmp1['i'],FAmp1['o'])
        show('AMP1: slope='+str(slope)+', '+'i='+str(intercept)+', '+'r_sq='+str(r_value**2))
        PAmp['Amp1']['a'] = slope
        PAmp['Amp1']['b'] = intercept
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(FAmp2['i'],FAmp2['o'])
        show('AMP2: slope='+str(slope)+', '+'i='+str(intercept)+', '+'r_sq='+str(r_value**2))
        PAmp['Amp2']['a'] = slope
        PAmp['Amp2']['b'] = intercept
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(FAmp3['i'],FAmp3['o'])
        show('AMP3: slope='+str(slope)+', '+'i='+str(intercept)+', '+'r_sq='+str(r_value**2))
        PAmp['Amp3']['a'] = slope
        PAmp['Amp3']['b'] = intercept
        
        
        '''
        Experimental setup...
        RF1---(Amp2)--(QIT-Ring-electrode)
        RF2---(Amp1)--(QIT-Endcap-electrode)
        AO1---(Amp3)--(RIDefl-y)
        '''
        #======Experimental conditions==========
        y = {'amp':200,'freq':[280E3, 400E3]}
        ampQit = 300
        mzQit = [160, 2E3]
        #========================================
        
        freqQit = [Mathieu.GetFreq( mzQit[0], ampQit, 1 ), Mathieu.GetFreq( mzQit[1], ampQit, 1 )]
        show(freqQit)
        
        FRM = numpy.linspace(y['freq'][0], y['freq'][1], 4, T)
        show(FRM)
        FRM = list(FRM)
        MSProcess.UpdAO( [0,0,0,0], [0,0,0,0] )
        MSProcess.UpdRFChFunc( 1, 3, 9 );
        MSProcess.UpdRFChBias( RFbch1, RFbch2, RFbch3)
        MSProcess.UpdRFChScale( 1, 1, 1 );
        conjlen = 4*25E-6
        MSProcess.UpdConj( 0, [6*25E-6, 3*25E-6, 1*25E-6], [2**32, 2*2**32, 3*2**32], T )
        MSProcess.RFStart( freqQit[0], ampQit, 0 )
        
        ampFgen = y['amp']
        ampFgen= ampFgen/(PAmp['Amp3']['a']*PRFCh['ch1']['a'])
        # ======scan condition======
        auxWfmType = 0
        auxStart = 0
        iauxCyc = 0
        auxCyc = 2
        beta = 1
        betaScale = 1
        auxAmp = 0
        auxPulse1 = [0, 0]
        auxPulse2 = [0.5, 0.55]
        auxPulseAmp = [0, -0.1]
        dm = 6
        freq = freqQit
        stepWidth = 60
        # ===========================
        for ff in FRM:
            freqFgen = ff
            MSProcess.UpdFGen( numpy.absolute(ampFgen), freqFgen )
            MSProcess.RFStart( freqQit[0], ampQit, 0 )
            MSProcess.Wait( 10, 0, 0 )
            MSProcess.LaserTrig( 200, 355, 15 )
            MSProcess.Wait( 5, 0, 0 )
            MSProcess.UpdFGen( 0, freqFgen )
            MSProcess.Wait( 25, 0, 0 )
            MSProcess.PhaseScanII( auxWfmType, auxStart, iauxCyc, auxCyc, beta, betaScale, auxAmp, auxPulse1, auxPulse2, auxPulseAmp, dm, freq, stepWidth )
        
        MSProcess.Wait( 50, 0, 0 )
        MSProcess.UpdFGen( 0, freqFgen )
        MSProcess.RFStop()
#__endpoint__
        showMsg.append( getShowArr() )
        response = MSProcess.getResponse
        return(  ( numpy.c_[response[0],response[1]] ).tolist() )
    except Exception:
        errMsg.append( str(sys.exc_info()[0]) )
        errMsg.append( str(sys.exc_info()[1]) )
        errMsg.append( str(sys.exc_info()[-1].tb_lineno - processStartIndex) )
        return []