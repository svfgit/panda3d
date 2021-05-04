
from helpers import input, camera

class ThirdPersonController:
    def __init__(self, app, playerNode, inputMgr=None) -> None:
        self.app=app
        self.playerNode = playerNode
        
        if inputMgr is not None:
            self.input = inputMgr
        else:
            self.input = input.InputMgr(app)
        
        self.cameraMgr = camera.ThirdPersonCameraMgr(app, playerNode, inputMgr=self.input)
        self.isMoving=False
        self.app.disableMouse()
    
    def updatePlayer(self, dt):
        # If a move-key is pressed, move ralph in the specified direction.

        if self.input.keyMap["turnLeft"]:
            self.playerNode.setH(self.playerNode.getH() + 300 * dt)
        if self.input.keyMap["turnRight"]:
            self.playerNode.setH(self.playerNode.getH() - 300 * dt)
        if self.input.keyMap["moveForward"]:
            self.playerNode.setY(self.playerNode, -25 * dt)
    
    def update(self, dt):
        self.updatePlayer(dt)
        self.cameraMgr.update(dt)
