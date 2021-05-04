from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import CollideMask

class PhysicsMgr:
    def __init__(self, app) -> None:
        self.app=app
        # We will detect the height of the terrain by creating a collision
        # ray and casting it downward toward the terrain.  One ray will
        # start above ralph's head, and the other will start above the camera.
        # A ray may hit the terrain, or it may hit a rock or a tree.  If it
        # hits the terrain, we can detect the height.  If it hits anything
        # else, we rule that the move is illegal.
        self.cTrav = CollisionTraverser()

        # Uncomment this line to see the collision rays
        #self.ralphGroundColNp.show()
        #self.camGroundColNp.show()

        # Uncomment this line to show a visual representation of the
        # collisions occuring
        #self.cTrav.showCollisions(render)

    # Creates a ray-based collision result queue for a node in the scene
    def setupCollisionRay(self, node, origin=(0,0,0), direction=(0,0,0), name=None):
        ray = CollisionRay()
        ray.setOrigin(origin)
        ray.setDirection(direction)

        col = CollisionNode(name)
        col.addSolid(ray)
        col.setFromCollideMask(CollideMask.bit(0))
        col.setIntoCollideMask(CollideMask.allOff())
        colNode = node.attachNewNode(col)
        queue = CollisionHandlerQueue()
        self.cTrav.addCollider(colNode, queue)

        return queue
    
    def registerEntity(self, entity):
        if entity.physicsType == "solid":
            return self.setupCollisionRay (
                entity.actor, origin=(0, 0, 9), direction=(0, 0, -1), name="actorRay")
    
    def updateEntityPhysics(self, entity, dt):   
        if entity.physicsType != "solid": return        

        # Adjust actor's Z coordinate.  If actor's ray hit terrain,
        # update its Z. If it hit anything else, or didn't hit anything, put
        # it back where it was last frame.

        entries = list(entity.physicsData.entries)
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())

        if len(entries) > 0 and entries[0].getIntoNode().name == "terrain":
            entity.actor.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            entity.actor.setPos(entity.lastPos)        

    def update(self, render):
        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.        

        self.cTrav.traverse(render)
       