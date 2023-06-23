"""
executeWingCode.py
Original Author : Eric Pavey - 2011-03-23
Module that Maya calls to when Wing tells Maya (via a socket)
to execute the commands in the temp file as either Python or mel code.
"""
import __main__
import os
import tempfile
import sys
import importlib
import time


try:
    #python2
    reload
except:
    #python3
    from importlib import reload

import maya.OpenMaya as om

def import_and_run(module_name, file_path=''):
    print('\n')
    imported = module_name in sys.modules
    if imported:
        print('reloading module:{0}'.format(module_name))
        reload( sys.modules[module_name] )
    else:
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError:
            if file_path:
                print('loading module from path:{0}'.format(module_name))
                main('python', file_path=file_path)
        
    if module_name in sys.modules and hasattr(sys.modules[module_name], 'run'):
        print('running module:{0}'.format(module_name))
        sys.modules[module_name].run()    


def main(codeType, file_path = ''):
    """
    Evaluate the temp file on disk, made by Wing, in Maya.

    codeType : string : Supports either 'python' or 'mel'
    """
    print_lines = False
    if not file_path:
        # Cross-platform way to get a temp dir:
        print_lines = True
        tempDir = tempfile.gettempdir()        
        file_path = os.path.join(tempDir, 'wingData.txt').replace("\\", "/")
         
    print ("WING: executing code from file {}\n".format(file_path)) 
    if os.access(file_path , os.F_OK):
        if print_lines:
            #temp data is likely highlighted code from Wing
            #so let's print it for review.
            with open(file_path, "rb") as f:
                for line in f.readlines():
                    print (line.rstrip())
            print ("\n"),

        if codeType == "python":
            # execute the file contents in Maya:            
            with open(file_path , "rb") as f:
                data = f.read()
                data =  data.decode()
                exec(data, __main__.__dict__, __main__.__dict__)
                
        elif codeType == "mel":
            melCmd = 'source "%s"'%file_path
            # This causes the "// Result: " line to show up in the Script Editor:
            om.MGlobal.executeCommand(melCmd, True, True)
    else:
        print ("No Wing-generated temp file exists: " + file_path)