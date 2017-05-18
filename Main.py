import threading
from BandMain import BandUI
from PhoneMain import PhoneUI

threads=[]
t1=threading.Thread(target=BandUI)
threads.append(t1)
t2=threading.Thread(target=PhoneUI)
threads.append(t2)

for t in threads:
    t.setDaemon(True)
    t.start()