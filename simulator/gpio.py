import logutil
BCM = 'BCM'
OUT = 'OUT'
IN = 'IN'

def setmode(mode):
    logutil.info('Setting mode ;) '+mode)

def setup(pin,operation):
    logutil.info("Setting Pin "+str(pin)+" "+str(operation))

def output(pin,status):
    logutil.info("Outputting Pin "+str(pin)+" "+str(status))

def cleanup():
    logutil.info("Lets cleaaaaan")