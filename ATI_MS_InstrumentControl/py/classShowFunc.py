class showState:
    def __init__(self):
        self.showArr = []

    def addArrVal(self, newMsg=None):
        if newMsg is None:
            raise ValueError('message is none')
        self.showArr.append(newMsg)

    def getShowMsg(self):
        return self.showArr


showArray = showState()

def show(var1="", var2=""):
    if var2 == '':
        showArray.addArrVal(str(var1))
    else:
        showArray.addArrVal(str(var1) + str(var2))


def Show(var1="", var2=""):
    show(var1, var2)


def getShowArr():
    return showArray.getShowMsg()
