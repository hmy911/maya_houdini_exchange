import maya.cmds as cmds
import os
import re

def convertASStoMa( selected_objs ,myassetpath):
    # selected_objs = cmds.ls(selection=True)
    for obj in selected_objs:
        standin_file = cmds.getAttr(obj + '.dso')
        standin_path, standin_filename = os.path.split(standin_file)
        basename, ext = os.path.splitext(standin_filename)
        searchdir = os.listdir(standin_path)
        mytranslate = cmds.getAttr('%s.translate' % obj )
        myrotate = cmds.getAttr('%s.rotate' % obj )
        myscale = cmds.getAttr('%s.scale' % obj )
        for eachfile in searchdir:
            if re.search( '.ma', eachfile ):
                if re.search( basename, eachfile):
                    ref_path = '%s/%s' % (myassetpath, eachfile)                
                    reference_node = cmds.file(ref_path, reference=True)
                    refnodes = cmds.referenceQuery(reference_node, nodes=True, dp=True)
                    print(refnodes)
                    eachref=refnodes[0]
                    mytype = cmds.nodeType(eachref)
                    if mytype=='transform':
                        print(eachref)
                        cmds.setAttr( eachref + ".translateX", mytranslate[0][0] )
                        cmds.setAttr( eachref + ".translateY", mytranslate[0][1] )
                        cmds.setAttr( eachref + ".translateZ", mytranslate[0][2] )
                        cmds.setAttr( eachref + ".rotateX", myrotate[0][0] )
                        cmds.setAttr( eachref + ".rotateY", myrotate[0][1] )
                        cmds.setAttr( eachref + ".rotateZ", myrotate[0][2] )
                        cmds.setAttr( eachref + ".scaleX", myscale[0][0] )
                        cmds.setAttr( eachref + ".scaleY", myscale[0][1] )
                        cmds.setAttr( eachref + ".scaleZ", myscale[0][2] )
        print('done----------------------')
    print('all done----------------------')


selected_objs = cmds.ls(selection=True)
myassetpath = 'D:/example/reference_asset'
convertASStoMa(selected_objs ,myassetpath)



