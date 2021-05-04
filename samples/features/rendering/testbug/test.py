from direct.showbase.ShowBase import ShowBase

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.accept("escape", base.userExit)

        self.setFrameRateMeter(True)

        self.mew = loader.loadModel("depthTest")

        collection = self.mew.findAllMatches("**/=depthOffset")
        for np in collection:
            offset = int(float(np.getTag("depthOffset")))
            np.setDepthOffset(offset)

        self.mew.reparentTo(render)
        self.mew.setY(4)


app = Game()
app.run()