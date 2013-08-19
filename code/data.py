import threading

class Data ( ) :
    
    data = None 
    lock = None

    def __init__ (self ):
        self.data = {}
        self.lock = threading.Lock()  

    def lock(self): 
        self.lock.acquire() 

    def unlock(self):
        self.lock.release() 
    
    def read ( self , key ):
        return self.data[key]

    def write ( self, key , valor ) :
        self.data[key] = valor



