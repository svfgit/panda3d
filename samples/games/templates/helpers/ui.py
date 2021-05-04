from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.07,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.09), shadow=(0, 0, 0, 1))

class UIMgr():
    def __init__(self, helpTitle=None, helpBody=None) -> None:
        if helpTitle is not None or helpBody is not None:
            self.createInstructionalUI(helpTitle, helpBody)

    def createInstructionalUI(self, title, body) -> None:
        # Post the instructions to the screen

        if title is not None:
            self.title = addTitle(title)
        
        if body is not None:
            # Iterate the string passed by the user and put onscreen
            lines=body.strip().replace("\t","").split("\n")        
            self.instructions=[]
            pos=0.06
            for i in lines:
                self.instructions.append(addInstructions(pos, i.strip()))
                pos += 0.06

