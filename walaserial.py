from __future__ import print_function # WalabotAPI works on both Python 2 an 3.
from sys import platform
from os import system
from imp import load_source
from os.path import join
import serial
#import keyboard
ser = serial.Serial('/dev/ttyUSB0', timeout = 1)

if platform.startswith('linux'):
    modulePath = join('/usr', 'share', 'walabot', 'python', 'WalabotAPI.py')     

wlbt = load_source('WalabotAPI', modulePath)
wlbt.Init()

def PrintSensorTargets(targets):
    system('cls' if platform == 'win32' else 'clear')
 #   if keyboard.is_pressed('q'):
  #      ser.write(str(-69))
   #     print("sent kill signal")
    #    return
    if targets and targets[0].amplitude > 1.5e-3: 
        print('Target Found:\ny: {}\nz: {}\n'.format(
                targets[0].yPosCm, targets[0].zPosCm))
        ser.write(str(targets[0].yPosCm) + ',' + str(targets[0].zPosCm))
        if targets[0].yPosCm < 0 and targets[0].yPosCm > -30:
            print("\nturn left")
        elif targets[0].yPosCm >=0 and targets[0].yPosCm < 30:
            print("\nturn right");
	else:
	    print("\ngo straight")
    else:
        print('No Target Detected')

def SensorApp():
    # wlbt.SetArenaR - input parameters
    minInCm, maxInCm, resInCm = 1, 140, 2
    # wlbt.SetArenaTheta - input parameters
    minIndegrees, maxIndegrees, resIndegrees = -10, 10, 10
    # wlbt.SetArenaPhi - input parameters
    minPhiInDegrees, maxPhiInDegrees, resPhiInDegrees = -44, 44, 2
    # Set MTI mode
    mtiMode = False
    # Configure Walabot database install location (for windows)
    wlbt.SetSettingsFolder()
    # 1) Connect : Establish communication with walabot.
    wlbt.ConnectAny()
    # 2) Configure: Set scan profile and arena
    # Set Profile - to Sensor.
    wlbt.SetProfile(wlbt.PROF_SENSOR)
    # Setup arena - specify it by Cartesian coordinates.
    wlbt.SetArenaR(minInCm, maxInCm, resInCm)
    # Sets polar range and resolution of arena (parameters in degrees).
    wlbt.SetArenaTheta(minIndegrees, maxIndegrees, resIndegrees)
    # Sets azimuth range and resolution of arena.(parameters in degrees).
    wlbt.SetArenaPhi(minPhiInDegrees, maxPhiInDegrees, resPhiInDegrees)
    # Moving Target Identification: standard dynamic-imaging filter
    filterType = wlbt.FILTER_TYPE_MTI if mtiMode else wlbt.FILTER_TYPE_NONE
    wlbt.SetDynamicImageFilter(filterType)
    # 3) Start: Start the system in preparation for scanning.
    wlbt.Start()
    if not mtiMode: # if MTI mode is not set - start calibrartion
        # calibrates scanning to ignore or reduce the signals
        wlbt.StartCalibration()
        while wlbt.GetStatus()[0] == wlbt.STATUS_CALIBRATING:
            wlbt.Trigger()
    while True:
        appStatus, calibrationProcess = wlbt.GetStatus()
        # 5) Trigger: Scan(sense) according to profile and record signals
        # to be available for processing and retrieval.
        wlbt.Trigger()
        # 6) Get action: retrieve the last completed triggered recording
        targets = wlbt.GetSensorTargets()
        rasterImage, _, _, sliceDepth, power = wlbt.GetRawImageSlice()
        # PrintSensorTargets(targets)
        PrintSensorTargets(targets)
    # 7) Stop and Disconnect.
    wlbt.Stop()
    wlbt.Disconnect()
    print('Terminate successfully')

if __name__ == '__main__':
    SensorApp()
