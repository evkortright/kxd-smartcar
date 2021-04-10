import joystickapi
import msvcrt
import time
import rpyc

def handleButton(btns):
    if (btns[0]):
        print("Up")
        carStateService.root.set_state("move", "fwd")
    elif (btns[1]):
        print("Right")
        carStateService.root.set_state("move", "fwd-right")
    elif (btns[2]):
        print("Down")
        carStateService.root.set_state("move", "rev")
    elif (btns[3]):
        print("Left")
        carStateService.root.set_state("move", "fwd-left")
    elif (btns[4]):
        print("- Left")
        carStateService.root.set_state("move", "rev-left")
    elif (btns[5]):
        print("- Right")
        carStateService.root.set_state("move", "rev-right")
    elif (btns[6]):
        print("-- Left")
        carStateService.root.set_state("move", "stop")

print("start")

carStateService = rpyc.connect("192.168.1.243", 18861)
print("CarStateService: ", carStateService)

num = joystickapi.joyGetNumDevs()
ret, caps, startinfo = False, None, None
for id in range(num):
    ret, caps = joystickapi.joyGetDevCaps(id)
    if ret:
        print("gamepad detected: " + caps.szPname)
        ret, startinfo = joystickapi.joyGetPosEx(id)
        break
else:
    print("no gamepad detected")

run = ret
while run:
    time.sleep(0.1)
    if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode(): # detect ESC
        run = False

    ret, info = joystickapi.joyGetPosEx(id)
    if ret:
        btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
        axisXYZ = [info.dwXpos-startinfo.dwXpos, info.dwYpos-startinfo.dwYpos, info.dwZpos-startinfo.dwZpos]
        axisRUV = [info.dwRpos-startinfo.dwRpos, info.dwUpos-startinfo.dwUpos, info.dwVpos-startinfo.dwVpos]
        if info.dwButtons:
            # print("buttons: ", btns)
            handleButton(btns)
        if any([abs(v) > 10 for v in axisXYZ]):
            print("axis:", axisXYZ)
        if any([abs(v) > 10 for v in axisRUV]):
            print("rotation axis:", axisRUV)

print("end")
