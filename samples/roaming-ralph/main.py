#!/usr/bin/env python

# Author: Ryan Myers
# Models: Jeff Styers, Reagan Heller
#
# Last Updated: 2015-03-13
#
# This tutorial provides an example of creating a character
# and having it walk around on uneven terrain, as well
# as implementing a fully rotatable camera.

from random import random
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Filename, AmbientLight, DirectionalLight

from helpers import ui, physics, scene, controllers, input

# Here is Ralph's friends' AI.  They randomly walk and turn 
# Looking for someone to play with!
class RalphsFriend(scene.Entity):
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


class RalphScene(scene.SceneMgr):
    def __init__(self, app) -> None:
        super().__init__()

        self.app = app

        # Set the background color to black
        app.win.setClearColor((0, 0, 0, 1))

        # Set up the environment

        # Note! see file: models/world.egg.pz.txt for info on how collision works in this model
        self.environ = loader.loadModel("models/world")
        self.environ.reparentTo(render)

        # Create the main character, Ralph
        ralphStartPos = self.environ.find("**/start_point").getPos()        

        self.ralph = self.addEntity(
            scene.Entity(
                app, 
                media="models/ralph",
                anims={"run": "models/ralph-run", "walk": "models/ralph-walk"},
                scale=.2, pos= ralphStartPos + (0, 0, 0.5), physicsType="solid"
            )
        )

        # Give Ralph some friends!!!

        for i in range(100):
            self.addEntity(
                RalphsFriend(
                    app, 
                    media="models/ralph",
                    anims={"run": "models/ralph-run", "walk": "models/ralph-walk"},
                    scale=.2, pos= ralphStartPos + (2, 2, 0.5), physicsType="solid"
                )
            )

        # Create some lighting
        self.setupSimpleLighting()

class RoamingRalphDemo(ShowBase):
    def __init__(self):
        # Set up the window, camera, etc.
        ShowBase.__init__(self)

        self.physics = physics.RalphPhysics(self)
        self.scene = RalphScene(self)        

        self.ui = ui.UIMgr(
            helpTitle = "Panda3D Tutorial: Roaming Ralph (Walking on Uneven Terrain)",
            helpBody = """
                [ESC]: Quit

                [W]: Run Ralph Forward
                [A]: Rotate Ralph Left
                [D]: Rotate Ralph Right
                
                [Q]: Rotate Camera Left
                [E]: Rotate Camera Right
            """)
        
        self.controller = controllers.ThirdPersonController(
            app=self, 
            playerNode=self.scene.ralph.actor,
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

demo = RoamingRalphDemo()
demo.run()
