from direct.actor.Actor import Actor
from panda3d.core import Filename, AmbientLight, DirectionalLight

class Entity:
    def __init__(self, app, media=None, anims=None, pos=(0,0,0), scale=1.0, physicsType=None):
        self.app=app
        self.actor = Actor(media, anims)

        self.actor.reparentTo(render)
        self.actor.setScale(scale)
        self.actor.setPos(pos)

        self.physicsType=physicsType
        self.lastPos=None
        self.wasMoving = False
        self.physicsData = self.app.physics.registerEntity(self)              

    def update(self, dt):  
        if self.lastPos==None: self.lastPos=self.actor.getPos()

        isMoving = (self.lastPos - self.actor.getPos()).length() > 0

        self.app.physics.updateEntityPhysics(self, dt)        
        
        if isMoving:
            if self.wasMoving is False:
                self.actor.loop("run")
                self.wasMoving = True
        else:
            if self.wasMoving:
                self.actor.stop()
                self.actor.pose("walk", 5)
                self.wasMoving = False
        
        self.lastPos=self.actor.getPos()

class SceneMgr:
    def __init__(self) -> None:
        self.entities=[]

    def setupSimpleLighting(self, ambientLightLevel=.3, directionalLightLevel=1):
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((ambientLightLevel, ambientLightLevel, ambientLightLevel, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection((-5, -5, -5))
        directionalLight.setColor((directionalLightLevel, directionalLightLevel, directionalLightLevel, 1))
        directionalLight.setSpecularColor((directionalLightLevel, directionalLightLevel, directionalLightLevel, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))

        return [ambientLight, directionalLight]
    
    def update(self, dt):
        for i in self.entities:
            i.update(dt)
    
    def addEntity(self, entity):
        self.entities.append(entity)
        return entity


