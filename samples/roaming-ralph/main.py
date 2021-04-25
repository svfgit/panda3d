#!/usr/bin/env python

# Author: Ryan Myers
# Models: Jeff Styers, Reagan Heller
#
# Last Updated: 2015-03-13
#
# This tutorial provides an example of creating a character
# and having it walk around on uneven terrain, as well
# as implementing a fully rotatable camera.

from direct.showbase.ShowBase import ShowBase

import random
import os
import math

from ralph_helpers import ui, input, physics, scene, camera

class RoamingRalphDemo(ShowBase):
    def __init__(self):
        # Set up the window, camera, etc.
        ShowBase.__init__(self)

        # Set the background color to black
        self.win.setClearColor((0, 0, 0, 1)) 

        self.scene      = scene.RalphScene(self)        
        self.ui         = ui.RalphUI()
        self.input      = input.RalphInput(self)        
        self.cameraMgr  = camera.RalphCameraMgr(self)
        self.physics    = physics.RalphPhysics(self)

        taskMgr.add(self.move, "moveTask")

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):

        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        dt = globalClock.getDt()

        self.input.update(dt)      
        self.physics.update(render)
        self.cameraMgr.update()

        return task.cont

demo = RoamingRalphDemo()
demo.run()
