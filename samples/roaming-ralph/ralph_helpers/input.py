

import sys

class RalphInput:
    def __init__(self, app) -> None:
        self.app = app
        # This is used to store which keys are currently pressed.
        self.keyMap = {"left": 0, "right": 0, "forward": 0, "cam-left": 0, "cam-right": 0}

        # Accept the control keys for movement and rotation

        self.app.accept("escape", sys.exit)
        self.app.accept("arrow_left", self.setKey, ["left", True])
        self.app.accept("arrow_right", self.setKey, ["right", True])
        self.app.accept("arrow_up", self.setKey, ["forward", True])
        self.app.accept("a", self.setKey, ["cam-left", True])
        self.app.accept("s", self.setKey, ["cam-right", True])
        self.app.accept("arrow_left-up", self.setKey, ["left", False])
        self.app.accept("arrow_right-up", self.setKey, ["right", False])
        self.app.accept("arrow_up-up", self.setKey, ["forward", False])
        self.app.accept("a-up", self.setKey, ["cam-left", False])
        self.app.accept("s-up", self.setKey, ["cam-right", False])

        # Game state variables
        self.isMoving = False



        self.app.disableMouse()
    
    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value
    
    def updateCamera(self, dt):
        # If the camera-left key is pressed, move camera left.
        # If the camera-right key is pressed, move camera right.

        if self.keyMap["cam-left"]:
            self.app.camera.setX(self.app.camera, -20 * dt)
        if self.keyMap["cam-right"]:
            self.app.camera.setX(self.app.camera, +20 * dt)
    
    def updateRalph(self, dt):
        # If a move-key is pressed, move ralph in the specified direction.

        if self.keyMap["left"]:
            self.app.scene.ralph.setH(self.app.scene.ralph.getH() + 300 * dt)
        if self.keyMap["right"]:
            self.app.scene.ralph.setH(self.app.scene.ralph.getH() - 300 * dt)
        if self.keyMap["forward"]:
            self.app.scene.ralph.setY(self.app.scene.ralph, -25 * dt)
        
        # If ralph is moving, loop the run animation.
        # If he is standing still, stop the animation.

        if self.keyMap["forward"] or self.keyMap["left"] or self.keyMap["right"]:
            if self.isMoving is False:
                self.app.scene.ralph.loop("run")
                self.isMoving = True
        else:
            if self.isMoving:
                self.app.scene.ralph.stop()
                self.app.scene.ralph.pose("walk", 5)
                self.isMoving = False
    
    def update(self, dt):
        self.updateCamera(dt)      
        self.updateRalph(dt)
    