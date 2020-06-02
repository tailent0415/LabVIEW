import numpy as np
import scipy as sci
from scipy import signal
from scipy.linalg import lstsq


def custom_savgol_coeffs(window_length, polyorder, deriv=0, delta=1.0, pos=None, use="conv"):
    if polyorder >= window_length:
        raise ValueError("polyorder must be less than window_length.")

    halflen, rem = divmod(window_length, 2)

    if pos is None:
        pos = halflen

    if not (0 <= pos < window_length):
        raise ValueError("pos must be nonnegative and less than window_length.")

    if use not in ['conv', 'dot']:
        raise ValueError("use must be 'conv' or 'dot'")

    if deriv > polyorder:
        coeffs = np.zeros(window_length)
        return coeffs

    # interval value
    x = np.arange(-pos, window_length - pos, dtype=float)
    if use == "conv":
        x = x[::-1]

    # deriv level order
    order = np.arange(polyorder + 1).reshape(-1, 1)

    # matrix
    A = x ** order
    y = np.zeros(polyorder + 1)
    y[deriv] = sci.math.factorial(deriv) / (delta ** deriv)
    coeffs, _, _, _ = lstsq(A, y)
    return coeffs


# ================================Negative===================================#
# Negative of multiple#
def PltNeg(pltData=None):
    if pltData is None:
        return []
    pltName = type(pltData).__name__
    if pltName == 'priDisplay':
        for n, sig in enumerate(pltData.ScanSig):
            pltData.ScanSig[n].ydata = np.negative(sig.ydata)
    elif pltName == 'secDisplay':
        for n, sig in enumerate(pltData.IonSig):
            pltData.IonSig[n].ydata = np.negative(sig.ydata)
    else:
        raise TypeError("Source error")

    return pltData


# ================================FFT===================================#
# FFT of multiple#
def PltFFT(pltData=None):
    if pltData is None:
        return []
    pltName = type(pltData).__name__
    if pltName == 'priDisplay':
        for n, sig in enumerate(pltData.ScanSig):
            dataLen = len(sig.ydata)
            pltData.ScanSig[n].dt = 1 / sig.dt / dataLen
            pltData.ScanSig[n].ydata = np.fft.fft(sig.ydata).real
        pltData.tGraph.xlabel = 'Frequency (Hz)'
    elif pltName == 'secDisplay':
        for n, sig in enumerate(pltData.IonSig):
            dataLen = len(sig.ydata)
            pltData.IonSig[n].dt = 1 / sig.dt / dataLen
            pltData.IonSig[n].ydata = np.fft.fft(sig.ydata).real
        pltData.ionGraph.xlabel = 'Frequency (Hz)'
    else:
        raise TypeError("Source error")

    return pltData


# ================================Abs===================================#
# Absolute of multiple#
def PltAbs(pltData=None):
    if pltData is None:
        return []
    pltName = type(pltData).__name__
    if pltName == 'priDisplay':
        for n, sig in enumerate(pltData.ScanSig):
            pltData.ScanSig[n].ydata = np.absolute(sig.ydata)
    elif pltName == 'secDisplay':
        for n, sig in enumerate(pltData.IonSig):
            pltData.IonSig[n].ydata = np.absolute(sig.ydata)
    else:
        raise TypeError("Source error")

    return pltData


# ================================NumRectifier===================================#
# NumRectifier of single#
def NumRectifier(dt=-1, ydata=[]):
    if dt <= 0:
        return []

    if len(ydata) == 0:
        return []

    C = 1e-12
    R = 1e+10

    kernelSize = 5
    kernel = np.zeros(kernelSize)
    halflen, rem = divmod(kernelSize, 2)

    kernel[0] = 1 * C / (12 * dt)
    kernel[1] = -2 * C / (3 * dt)
    kernel[2] = -1 / R
    kernel[3] = 2 * C / (3 * dt)
    kernel[4] = -1 * C / (12 * dt)
    kernel = kernel * 0.25

    I_b = sci.convolve(ydata, kernel, 'same')
    I_b[0:halflen] = I_b[halflen + 1]
    I_b[len(I_b) - halflen:len(I_b)] = I_b[len(I_b) - halflen - 1]

    return I_b


def NumRectifier_SG(dt=-1, ydata=[], winwidth=5):
    if dt <= 0:
        return []

    if len(ydata) == 0:
        return []

    if winwidth < dt:
        winwidth = dt * 5

    windowSize = int(winwidth / dt)
    if windowSize > 10000:
        windowSize = 10001

    halflen, rem = divmod(windowSize, 2)
    if rem == 0:
        windowSize = windowSize + 1

    d0 = custom_savgol_coeffs(window_length=windowSize, polyorder=3, deriv=0, delta=dt)
    d1 = custom_savgol_coeffs(window_length=windowSize, polyorder=3, deriv=1, delta=dt)

    k1 = 0.25
    C = 1e-12
    R = 1e+10

    v1 = sci.convolve(ydata, d0, 'same')
    dv1 = sci.convolve(ydata, d1, 'same')
    I_b = -1 * C * k1 * (dv1 + v1 / (C * R))

    I_b[0:halflen] = I_b[halflen + 1]
    I_b[len(I_b) - halflen:len(I_b)] = I_b[len(I_b) - halflen - 1]

    return I_b


# NumRectifier of multiple#
def PltNumRectifier(pltData=[]):
    pltName = type(pltData).__name__
    if pltName == 'priDisplay':
        for n, sig in enumerate(pltData.ScanSig):
            pltData.ScanSig[n].ydata = NumRectifier(sig.dt, sig.ydata)
        pltData.tGraph.ylabel = 'Current (A)'
        pltData.mzGraph.ylabel = 'Current (A)'

    elif pltName == 'secDisplay':
        for n, sig in enumerate(pltData.IonSig):
            pltData.IonSig[n].ydata = NumRectifier(sig.dt, sig.ydata)
    else:
        raise TypeError("Source error")

    return pltData


def PltNumRectifier_SG(pltData=[], winwidth=5):
    pltName = type(pltData).__name__
    if pltName == 'priDisplay':
        for n, sig in enumerate(pltData.ScanSig):
            pltData.ScanSig[n].ydata = NumRectifier_SG(sig.dt, sig.ydata, winwidth)
        pltData.tGraph.ylabel = 'Current (A)'
        pltData.mzGraph.ylabel = 'Current (A)'

    elif pltName == 'secDisplay':
        for n, sig in enumerate(pltData.IonSig):
            pltData.IonSig[n].ydata = NumRectifier_SG(sig.dt, sig.ydata, winwidth)
    else:
        raise TypeError("Source error")

    return pltData


# ================================Filtering===================================#
# Filtering of single#
def Filtering(dt=-1, ydata=[], ktype='boxcar', kwidth=1):
    if (dt <= 0):
        return []

    if len(ydata) == 0:
        return []

    if kwidth < dt:
        kwidth = dt
    elif kwidth > 3:
        kwidth = 3

    winsize = int(np.floor(kwidth / dt))
    if winsize != 1:
        if (ktype == 'norm' or ktype == 'Gaussian'):
            window = signal.windows.gaussian(winsize, winsize / 6)
        else:
            # boxcar, triang, blackman, hamming, hann, bartlett, flattop, parzen...
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.get_window.html#scipy.signal.get_window
            window = signal.get_window(ktype, winsize)

        window = window / sum(window)
        ydata = sci.convolve(ydata, window, 'same')
        halflen, rem = divmod(winsize, 2)
        if rem == 0:
            halflen = halflen + 1
        ydata[0:halflen] = ydata[halflen + 1]
        ydata[len(ydata) - halflen:len(ydata)] = ydata[len(ydata) - halflen - 1]

    return ydata


# Filtering of multiple#
def PltFiltering(pltData=[], ktype='boxcar', kwidth=1):
    pltName = type(pltData).__name__
    if pltName == 'priDisplay':
        for n, sig in enumerate(pltData.ScanSig):
            pltData.ScanSig[n].ydata = Filtering(sig.dt, sig.ydata, ktype, kwidth)
    elif pltName == 'secDisplay':
        for n, sig in enumerate(pltData.IonSig):
            pltData.IonSig[n].ydata = Filtering(sig.dt, sig.ydata, ktype, kwidth)
    else:
        raise TypeError("Source error")

    return pltData


# ================================Convolution===================================#
# Convolution plot data#
def PltConv1D(pltData, kernel):
    halflen = int(len(kernel) / 2)
    pltName = type(pltData).__name__
    if pltName == 'priDisplay':
        for n, sig in enumerate(pltData.ScanSig):
            ydata = sci.convolve(sig.ydata, kernel, 'same')
            ydata[0:halflen] = ydata[halflen + 1]
            ydata[len(ydata) - halflen:len(ydata)] = ydata[len(ydata) - halflen - 1]
            pltData.ScanSig[n].ydata = ydata
    elif pltName == 'secDisplay':
        for n, sig in enumerate(pltData.IonSig):
            ydata = sci.convolve(sig.ydata, kernel, 'same')
            ydata[0:halflen] = ydata[halflen + 1]
            ydata[len(ydata) - halflen:len(ydata)] = ydata[len(ydata) - halflen - 1]
            pltData.IonSig[n].ydata = ydata
    else:
        raise TypeError("Source error")

    return pltData


# ===============================MakeKernel====================================#
# Maker kernel data#
def MakeKernel(dt=-1, ktype='boxcar', kwidth=1):
    if dt <= 0:
        return []

    if kwidth < dt:
        kwidth = dt
    elif kwidth > 3:
        kwidth = 3

    items = int(np.floor(kwidth / dt))
    winsize = int(items / 2)

    if ktype == 'boxcar':
        kernelData = np.arange(winsize)
        kernelData = np.append(kernelData, [np.append(winsize, np.flip(kernelData))])
        kernelData = np.full(kernelData.shape[0], 1 / kernelData.shape[0])

    elif ktype == 'triang':
        kernelData = np.arange(winsize)
        kernelData = np.append(kernelData, [np.append(winsize, np.flip(kernelData))])
        kernelData = kernelData / np.sum(kernelData)

    elif ktype == 'norm' or ktype == 'Gaussian':
        w = winsize * (-1)
        vara = items / (items - 1)
        factor = np.zeros(items)
        alpha = (items / 6) ** 2 * 2

        for i in range(items):
            if i != 0:
                w = w + vara;
            factor[i] = (w ** 2 * (-1)) / alpha

        expVal = np.exp(factor)
        kernelData = expVal / np.sum(expVal)

    else:
        raise ValueError("This kernel type isn't exist")

    return kernelData


# ==============================================================#
# =================Peak Finding Function========================#
# ==============================================================#

# Find peak processs
def FindPeak(peakData, pltData, kwidth=1, iteration=30, ampTh=float("-inf"), slopeTh=float("-inf")):
    className = type(peakData).__name__
    if className != 'peakDisplay':
        raise TypeError("Peak Data Source error")
    className = type(pltData).__name__
    if className != 'priDisplay':
        raise TypeError("Polt Data Source error")

    for n, sig in enumerate(pltData.ScanSig):
        if sig.dt <= 0 or len(sig.xdata) == 0 or len(sig.ydata) == 0:
            return peakData, pltData

        items = int(np.floor(kwidth / sig.dt))
        winwidth = int(items / 2)
        kernelData = MakeKernel(sig.dt, 'Gaussian', kwidth)
        halflen = int(len(kernelData) / 2)

        smoothY = sci.convolve(sig.ydata, kernelData, 'same')
        smoothY[0:halflen] = smoothY[halflen + 1]
        smoothY[len(smoothY) - halflen:len(smoothY)] = smoothY[len(smoothY) - halflen - 1]

        if ampTh == float("-inf"):
            ampTh = np.sqrt(np.mean(smoothY ** 2))

        newY = GetBaseline(sig.xdata, smoothY)
        print(newY)
        peakX, centerIdx = GetPeak(sig.dt, sig.xdata, newY, winwidth, ampTh, slopeTh)
        leftX, rightX, leftIdx, rightIdx = GetPeakWidth(sig.dt, sig.xdata, newY, centerIdx)
        halfHeight = GetPeakHalfHeight(sig.xdata, newY, centerIdx, leftIdx, rightIdx)
        pltData.ScanSig[n].ydata = smoothY
        peakData.PeakInfo[n].xLdata = leftIdx
        peakData.PeakInfo[n].xCdata = centerIdx
        peakData.PeakInfo[n].xRdata = rightIdx
        peakData.PeakInfo[n].baseline = smoothY - newY
        peakData.PeakInfo[n].halfHeight = halfHeight

    return peakData, pltData


# Get remove baseline Y data #
def GetBaseline(xdata=[], ydata=[], iteration=30):
    if len(xdata) == 0 or len(ydata) == 0:
        return []

    threshold = np.sum(np.absolute(ydata)) * 1e-10
    weight = np.ones(len(ydata))
    condition = True
    idx = 0
    baseline = []
    newY = ydata
    while condition:
        poly = np.polyfit(xdata, ydata, 2, w=weight)
        baseline = np.polyval(poly, xdata)
        newY = ydata - baseline
        maxVal = float("-inf")
        sumVal = 0
        for n, val in enumerate(newY):
            if val < 0:
                sumVal = sumVal + val
                if val > maxVal:
                    maxVal = val
        sumVal = np.absolute(sumVal)
        if sumVal < threshold:
            break
        for n, val in enumerate(newY):
            if val >= 0:
                weight[n] = 0
            else:
                weight[n] = np.exp(np.absolute(((idx + 1) * val) / sumVal))

        weight[n] = maxVal / sumVal
        weight[len(weight) - 1] = maxVal / sumVal

        if idx > iteration:
            condition = False
        idx = idx + 1

    poly = np.polyfit(xdata, newY, 3)
    baseline = np.polyval(poly, xdata)
    ydata = newY - baseline
    return ydata


# Get peak index and X value #
def GetPeak(dt=-1, xdata=[], ydata=[], winwidth=3, ampTh=float("-inf"), slopeTh=float("-inf")):
    if dt <= 0 or len(ydata) == 0 or len(xdata) == 0:
        return [], []
    derive1 = np.gradient(ydata, dt)
    derive1[0] = derive1[1]
    derive1[derive1.size - 1] = derive1[derive1.size - 2]
    derive2 = np.gradient(derive1, dt)
    lastVal = 0
    peakIdx = []
    for n, val in enumerate(derive1):
        if winwidth < n < derive1.size - winwidth:
            if lastVal > 0 and val <= 0:
                if ydata[n] > ampTh and derive2[n] > slopeTh:
                    peakIdx.append(n)
        lastVal = val

    peakX = np.zeros(len(peakIdx))
    for i in range(len(peakX)):
        peakX[i] = xdata[peakIdx[i]]

    return peakX, peakIdx


# Get peak left and right point information #
def GetPeakWidth(dt=-1, xdata=[], ydata=[], peakIdx=[]):
    if dt <= 0 or len(ydata) == 0 or len(xdata) == 0 or len(peakIdx) == 0:
        return [], [], [], []

    derive1 = np.gradient(ydata, dt)
    lastVal = 0
    tagetIdx = 0
    pervIdx = 0

    leftIdx = []
    rightIdx = []

    for n, val in enumerate(derive1):
        if tagetIdx >= len(peakIdx):
            break
        if lastVal <= 0 and val > 0:
            if n > peakIdx[tagetIdx]:
                leftIdx.append(pervIdx)
                rightIdx.append(n)
                tagetIdx = tagetIdx + 1
                pervIdx = n
            else:
                pervIdx = n
        lastVal = val

    if tagetIdx < len(peakIdx):
        leftIdx.append(pervIdx)
        rightIdx.append(n)

    leftX = np.zeros(len(leftIdx))
    rightX = np.zeros(len(rightIdx))
    for i in range(len(leftIdx)):
        leftX[i] = xdata[leftIdx[i]]
        rightX[i] = xdata[rightIdx[i]]

    return leftX, rightX, leftIdx, rightIdx


# Get peak half height #     
def GetPeakHalfHeight(xdata=[], ydata=[], peakIdx=[], leftIdx=[], rightIdx=[]):
    if len(ydata) == 0 or len(xdata) == 0:
        return []
    halfHeight = []
    for n, val in enumerate(peakIdx):
        xp = [xdata[leftIdx[n]], xdata[rightIdx[n]]]
        fp = [ydata[leftIdx[n]], ydata[rightIdx[n]]]
        halfHeight.append((ydata[peakIdx[n]] - np.interp(xdata[peakIdx[n]], xp, fp)) * 0.5)
    return halfHeight
