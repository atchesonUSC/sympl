import os
import subprocess

def changeDirectory():
    path = '/Users/alexatcheson/Desktop/harvi/block/program'
    os.chdir(path)

def make():
    subprocess.call(['make'])

def makeFlash():
    subprocess.call(['make','flash'])

def compileAndUpload():
    changeDirectory()
    make()
    makeFlash()



# def compile(filename):
#     end = len(filename) - 2
#     filename = filename[0:end]
#     cmd = ['avr-gcc','-Os','-DF_CPU=16000000','-mmcu=atmega328p','-c','-o',filename + '.o',filename + '.c','-std=c99']
#     subprocess.call(cmd)
#
# def createELFprogram(filename):
#     end = len(filename) - 2
#     filename = filename[0:end]
#     cmd = ['avr-gcc','-mmcu=atmega328p',filename + '.o','-o',filename]
#     subprocess.call(cmd)
#
# def convertToIHEXfile(filename):
#     end = len(filename) - 2
#     filename = filename[0:end]
#     cmd = ['avr-objcopy','-O','ihex','-R','.eeprom',filename,filename+'.hex']
#     subprocess.call(cmd)
#
# def uploadIHEXfileToChip(filename):
#     end = len(filename) - 2
#     filename = filename[0:end]
#     cmd = ['avrdude','-F','-V','-c','arduino','-p','ATMEGA328P','-P','/dev/cu.usbmodem14201','-b','115200','U','flash:w:'+filename+'.hex']
#     subprocess.call(cmd)
#
# def makeProgram(filename):
#     changeDirectory()
#     compile(filename)
#     createELFprogram(filename)
#     convertToIHEXfile(filename)
#     uploadIHEXfileToChip(filename)

# def main():
#     file = 'beep'
#     changeDirectory()
#     compile(file)
#     createELFprogram(file)
#     convertToIHEXfile(file)
#     uploadIHEXfileToChip(file)
#
# main()