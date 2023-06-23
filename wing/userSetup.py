import maya.cmds as cmds
import pymel.core as pm
import maya.utils

COMMAND_PORT = ':6000'

def open_maya_port():
    try:   
        if not cmds.commandPort(COMMAND_PORT, q = True):
            cmds.commandPort(n = COMMAND_PORT)
            print( "Opened Command Port:{0}".format(COMMAND_PORT) )
    except:
        print('couldnt open command port')


def make_wing_menu():
    print("building Wing Menu!")
    from wing import make_menu
    make_menu.run()

maya.utils.executeDeferred(make_wing_menu)
open_maya_port()


