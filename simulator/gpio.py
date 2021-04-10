BCM = 'BCM'
OUT = 'OUT'
IN = 'IN'

def setmode(mode):
    print('Setting mode ;) '+mode)

def setup(pin,operation):
    print("Setting Pin "+str(pin)+" "+str(operation))

def output(pin,status):
    print("Outputting Pin "+str(pin)+" "+str(status))

def cleanup():
    print("Lets cleaaaaan")