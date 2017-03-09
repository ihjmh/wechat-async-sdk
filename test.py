class Test(object):
    """docstring for Test"""
    def __init__(self):
        super(Test, self).__init__()
        self._fee = None

    @property
    def fee(self):
        return self._fee

    @fee.setter
    def fee(self,feee):
        self._fee=feee  

    def start(self):
        print(self.fee)

if __name__=="__main__":
    f=Test()
    f.fee='111'
    print(f.start())