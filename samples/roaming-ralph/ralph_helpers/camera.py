from panda3d.core import PandaNode, NodePath

class RalphCameraMgr:
    def __init__(self, app) -> None:
        self.app=app

        # Set up the camera        
        self.app.camera.setPos(self.app.scene.ralph.getX(), self.app.scene.ralph.getY() + 10, 2)

        # Create a floater object, which floats 2 units above ralph.  We
        # use this as a target for the camera to look at.

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(self.app.scene.ralph)
        self.floater.setZ(2.0)
    
    def update(self):
        # If the camera is too far from ralph, move it closer.
        # If the camera is too close to ralph, move it farther.

        camvec = self.app.scene.ralph.getPos() - self.app.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if camdist > 10.0:
            self.app.camera.setPos(self.app.camera.getPos() + camvec * (camdist - 10))
            camdist = 10.0
        if camdist < 5.0:
            self.app.camera.setPos(self.app.camera.getPos() - camvec * (5 - camdist))
            camdist = 5.0
        
        # Keep the camera at one foot above the terrain,
        # or two feet above ralph, whichever is greater.

        entries = list(self.app.physics.camGroundHandler.entries)
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())

        if len(entries) > 0 and entries[0].getIntoNode().name == "terrain":
            self.app.camera.setZ(entries[0].getSurfacePoint(render).getZ() + 1.0)
        if self.app.camera.getZ() < self.app.scene.ralph.getZ() + 2.0:
            self.app.camera.setZ(self.app.scene.ralph.getZ() + 2.0)

        # The camera should look in ralph's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above ralph's head.
        self.app.camera.lookAt(self.floater)
    