from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import CollideMask

class RalphPhysics:
    def __init__(self, app) -> None:
        self.app=app
        # We will detect the height of the terrain by creating a collision
        # ray and casting it downward toward the terrain.  One ray will
        # start above ralph's head, and the other will start above the camera.
        # A ray may hit the terrain, or it may hit a rock or a tree.  If it
        # hits the terrain, we can detect the height.  If it hits anything
        # else, we rule that the move is illegal.
        self.cTrav = CollisionTraverser()

        self.ralphGroundRay = CollisionRay()
        self.ralphGroundRay.setOrigin(0, 0, 9)
        self.ralphGroundRay.setDirection(0, 0, -1)
        self.ralphGroundCol = CollisionNode('ralphRay')
        self.ralphGroundCol.addSolid(self.ralphGroundRay)
        self.ralphGroundCol.setFromCollideMask(CollideMask.bit(0))
        self.ralphGroundCol.setIntoCollideMask(CollideMask.allOff())
        self.ralphGroundColNp = self.app.scene.ralph.attachNewNode(self.ralphGroundCol)
        self.ralphGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.ralphGroundColNp, self.ralphGroundHandler)

        self.camGroundRay = CollisionRay()
        self.camGroundRay.setOrigin(0, 0, 9)
        self.camGroundRay.setDirection(0, 0, -1)
        self.camGroundCol = CollisionNode('camRay')
        self.camGroundCol.addSolid(self.camGroundRay)
        self.camGroundCol.setFromCollideMask(CollideMask.bit(0))
        self.camGroundCol.setIntoCollideMask(CollideMask.allOff())
        self.camGroundColNp = self.app.camera.attachNewNode(self.camGroundCol)
        self.camGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.camGroundColNp, self.camGroundHandler)

        # Uncomment this line to see the collision rays
        self.ralphGroundColNp.show()
        self.camGroundColNp.show()

        # Uncomment this line to show a visual representation of the
        # collisions occuring
        self.cTrav.showCollisions(render)
    
    def update(self, render):
        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.        

        self.cTrav.traverse(render)
        # Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
        # update his Z. If it hit anything else, or didn't hit anything, put
        # him back where he was last frame.

        entries = list(self.ralphGroundHandler.entries)
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())

        if len(entries) > 0 and entries[0].getIntoNode().name == "terrain":
            self.app.scene.ralph.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self.app.scene.ralph.setPos(self.app.startpos)