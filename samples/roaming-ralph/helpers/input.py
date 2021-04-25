

import sys

defaultToggleKeyConfig = {
    "moveForward":"arrow_up",
    "turnLeft":"arrow_left",
    "turnRight":"arrow_right",
    "moveBackward":"arrow_down",
    "turnCameraLeft":"a",
    "turnCameraRight":"s"
}

class InputMgr:
    def __init__(self, app, toggleKeyConfig=defaultToggleKeyConfig) -> None:
        self.app = app

        # This is used to store which keys are currently pressed.
        self.keyMap={}

        # Accept the control keys for movement and rotation
        for i in toggleKeyConfig.keys():
            self.keyMap[i] = 0
            self.app.accept(toggleKeyConfig[i], self.setKey, [i, True])
            self.app.accept(toggleKeyConfig[i]+"-up", self.setKey, [i, False])

        self.app.accept("escape", sys.exit)        
    
    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value 

    