from scipy import signal
wid= 0.003

PriPlt = sp.PltFiltering( PriPlt, 'Gaussian', wid )
PriPlt = sp.PltNumRectifier( PriPlt )

a = int( wid/5/10**-6 )

for n, sig in enumerate( PriPlt.ScanSig ):
    PriPlt.ScanSig[n].ydata = sig.ydata * sig.dt / 1.6 / 10 ** -19
    PriPlt.ScanSig[n].ydata = PriPlt.ScanSig[n].ydata - PriPlt.ScanSig[n].ydata[0] - 4
    for idx, val in enumerate( PriPlt.ScanSig[n].ydata ):
        if PriPlt.ScanSig[n].ydata[idx] < 0:
            PriPlt.ScanSig[n].ydata[idx] = 0
        if idx < a+1:
            PriPlt.ScanSig[n].ydata[idx] = 0
        if len(PriPlt.ScanSig[n].ydata)-idx < a+1:
            PriPlt.ScanSig[n].ydata[idx] = 0
    PriPlt.ScanSig[n].ydata = numpy.add.accumulate( PriPlt.ScanSig[n].ydata )
