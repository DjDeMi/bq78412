class CRCError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "Error " + str(self.value)

class timeoutError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "Error " + str(self.value)

class sizeError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "Error " + str(self.value)

class ACKError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "Error " + str(self.value)
