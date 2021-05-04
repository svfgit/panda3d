#!/usr/bin/env python

# Author: svf
# This tutorial provides an example of creating a character
# and having it walk around on uneven terrain, as well
# as implementing a fully rotatable camera.

from random import random
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Filename, AmbientLight, DirectionalLight

from helpers import ui, physics, scene, controllers, input

# Here is an example AI entity for the scene.  
# It will randomly move around the scene, pausing and turning periodically
class ExampleAIEntity(scene.Entity):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self.nextState=None
        self.states=["walk", "turn", "wait"]
        self.turnRate = 100
        self.state=None

    def update(self, dt):
        super().update(dt)
        #print (self.state, self.nextState)
        if self.nextState==None or self.nextState <= 0.0:
            self.nextState = random() * 5
            self.state = self.states[int(random() * 3)]
        
        if self.state == "turn":
            self.actor.setH(self.actor.getH() + 100 * dt)
        elif self.state=="walk":
            self.actor.setY(self.actor, -25 * dt)
        elif self.state=="wait":
            pass

        self.nextState -= dt


class ThirdPersonScene(scene.SceneMgr):
    def __init__(self, app) -> None:
        super().__init__()

        self.app = app

        # Set the background color to black
        app.win.setClearColor((0, 0, 0, 1))

        # Set up the environment

        # Note! see file: models/world.egg.pz.txt for info on how collision works in this model
        self.environ = loader.loadModel("models/world")
        self.environ.reparentTo(render)

        # Find the starting point from within the level media
        playerStartPos = self.environ.find("**/start_point").getPos()

        playerModel = "models/ralph"  
        playerAnimations = {"run": "models/ralph-run", "walk": "models/ralph-walk"}

        self.playerEntity = self.addEntity(
            scene.Entity(
                app, 
                media=playerModel,
                anims=playerAnimations,
                scale=.2, pos=playerStartPos + (0, 0, 0.5), physicsType="solid"
            )
        )

        # Setup some AI entities, just for demonstration purposes.
        # For now, using the player model and animations
        for i in range(100):
            self.addEntity(
                ExampleAIEntity(
                    app, 
                    media=playerModel,
                    anims=playerAnimations,
                    scale=.2, pos=playerStartPos + (2, 2, 0.5), physicsType="solid"
                )
            )

        # Create some lighting
        self.setupSimpleLighting(ambientLightLevel=.6)

class ThirdPersonDemo(ShowBase):
    def __init__(self):
        # Set up the window, camera, etc.
        ShowBase.__init__(self)

        self.physics = physics.PhysicsMgr(self)
        self.scene = ThirdPersonScene(self)        

        self.ui = ui.UIMgr(
            helpTitle = "Panda3D Tutorial: Third Person Sample",
            helpBody = """
                [ESC]: Quit

                [W]: Move Player Avatar Forward
                [A]: Rotate Player Avatar Left
                [D]: Rotate Player Avatar Right
                
                [Q]: Rotate Camera Left
                [E]: Rotate Camera Right
            """)

        self.controller = controllers.ThirdPersonController(
            app=self, 
            playerNode=self.scene.playerEntity.actor,
            inputMgr=input.InputMgr(
                app=self,
                toggleKeyConfig = {
                    "moveForward":"w",
                    "turnLeft":"a",
                    "moveBackward":"s",
                    "turnRight":"d",                    
                    "turnCameraLeft":"e",
                    "turnCameraRight":"q"
                }
            )
        )

        taskMgr.add(self.updateTask, "updateTask")

    def updateTask(self, task):

        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        dt = globalClock.getDt()        

        self.controller.update(dt)
        self.physics.update(render)
        self.scene.update(dt)
        

        return task.cont

demo = ThirdPersonDemo()
demo.run()
