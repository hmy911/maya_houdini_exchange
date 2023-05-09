import maya.cmds as cmds    
import re    

def XgenExportASS( characterName, version ):
    strCurrentScene = cmds.file( q=True, sn=True )
    strSceneName = ""
    if strCurrentScene:
        strScenePath = os.path.dirname( strCurrentScene )
        strSceneFile = os.path.basename( strCurrentScene )
        strSceneName = os.path.splitext( strSceneFile )[0];
    projPath = strScenePath.replace("scenes","")
    abcFolderPath = projPath + "/cache/ass"
    cutIn = cmds.playbackOptions( q=True,min=True ) -1 
    cutOut  = cmds.playbackOptions( q=True,max=True ) +1

    listXgen = cmds.ls(type='xgmPalette')
    for eachXgen in listXgen:
        if re.search( characterName ,eachXgen ):
            print(eachXgen)
            obj = eachXgen
            ns, objname = obj.split(':')
            fullFilePath = '%s/%s/%s/%s.ass' % ( abcFolderPath, version ,objname, objname)
            cmds.select(listXgen)
            cmds.arnoldExportAss(f = fullFilePath, 
                s = True, 
                sf = cutIn, 
                ef = cutOut,
                # ef = cutIn+5,        
                frameStep = 1.0,
                compressed = True,
                expandProcedurals = True,
                fullPath = True )
            print(fullFilePath)

# XgenExportASS( 'filter_name', 'v1' )

