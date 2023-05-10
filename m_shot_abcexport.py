import os,sys,re,json
import maya.cmds as cmds
import maya.mel
import glob

def createDir(createPath):
    if not os.path.exists(createPath):
        print 'os.makedirs(%s)'% createPath
        os.makedirs(createPath)

def openmaya(fullfilename):
    cmds.file(fullfilename,force=True, open=True , prompt = False)

def deleteSetABC():
    allsets = cmds.ls(type='objectSet')
    for eachset in allsets:
        if re.search('ABC',eachset):
            cmds.delete(eachset)
    print '--------DELETE-------ABC SET---------'

def export_alembic(obj,exportPath,startframe,endframe):
    objDict = {'kStart': startframe , 'kEnd': endframe , 'kRoot': '-root' , 'kExportfile': exportPath}
    objDict['kRoot'] = obj
    fmt = 'AbcExport -j "-writeVisibility -worldSpace -renderableOnly -uvWrite -frameRange %(kStart)s %(kEnd)s -root %(kRoot)s -file %(kExportfile)s"' % objDict
    maya.mel.eval(fmt)
    print '%s\n'% fmt    
    print '%s------------------ok\n'% fmt

def hideHair(onoff):
    hairGrps = cmds.ls("*:hair_geoGp")
    for eachHair in hairGrps:
        cmds.setAttr("%s.visibility" % eachHair, onoff)

def createSets(assetType,refObject):
    print 'createSets------------------------------ start'
    if refObject==1:
        allObjects = cmds.ls( referencedNodes=True, assemblies = 1 ) 
    else:
        allObjects = cmds.ls(assemblies=1,visible=1)
    print 'createSets: %s size: %s'%(allObjects,len(allObjects))
    if allObjects:
        cmds.select(clear=1)
        for eachone in allObjects:
            reffullpath = cmds.referenceQuery( eachone, filename=True)
            print '%s------------------------------ eachoneeachoneeachoneeachoneeachone' % reffullpath
            if re.search(assetType,reffullpath):                
                cmds.select(eachone,add=1)
                # print '%s------------------------------ got it'%eachone
        cmds.sets(name='ABC_%s'%assetType)
    else:
        print 'no object to export ABC'



def writeDetailJson(shotcode, outputPath):
    mayafile = cmds.file(q=True, loc=True)
    cutIn = cmds.playbackOptions( q=True,min=True )
    cutOut  = cmds.playbackOptions( q=True,max=True )
    cams = cmds.ls(type='camera')
    allsets = cmds.ls(type='objectSet')
    allObjects = cmds.ls( referencedNodes=True, assemblies = 1 ) 
    allRefFiles = []
    for eachone in allObjects:
        reffullpath = cmds.referenceQuery( eachone, filename=True)
        #print reffullpath
        allRefFiles.append(reffullpath)
    print allRefFiles
    json_string = [mayafile, shotcode, cutIn, cutOut, cams, allRefFiles, allsets]
    # Directly from dictionary
    with open('%s/detail_%s.json' % (outputPath, shotcode), 'w') as outfile:
        json.dump(json_string, outfile)
    print '--------------------------------------writeDetailJson'

def exportABC(outputPath, framerange):
    if framerange=='startend':
        in_frame = cmds.playbackOptions( q=True,min=True )-1
        out_frame  = cmds.playbackOptions( q=True,max=True )+1
    if framerange=='single':
        in_frame = cmds.playbackOptions( q=True,min=True )
        out_frame  = in_frame    
    allsets = cmds.ls(type='objectSet')
    for eachset in allsets:
        if re.search('ABC',eachset):
            createDir(outputPath)
            exportFile = '%s/%s.abc' % (outputPath,eachset)
            strSets = ' -root '.join(eachset)
            getSets = cmds.sets(eachset,q=1)
            print 'getSets:  %s'%getSets
            if getSets:
                strSets = ' -root '.join(getSets)                
                print exportFile,strSets
                print exportFile            
                export_alembic(strSets,exportFile,in_frame,out_frame)

def createManualSets(typename, strManual):
    cmds.select(clear=1)
    customtube = cmds.ls("%s" % strManual)
    cmds.select(customtube,add=1)
    cmds.sets(name='ABC_%s'% typename)

def createManualTypeSets(typename, filtername):
    cmds.select(clear=1)
    customtube = cmds.ls(type="%s" % typename)
    for each in customtube:
        if re.search( filtername , each ):
            print each
            b=cmds.listRelatives(each, parent=1,f=1)
            print b
            cmds.select(b,add=1)
            cmds.sets(name='ABC_%s'% typename)

def batchshot(shotcode, sourcePath, outputPath, framerange, openFile, mode, doExport, ver, check):
    list_of_files = glob.glob('%s/*.ma' % sourcePath )
    # print list_of_files
    # print list_of_files[-1]
    if len(list_of_files) >= 2:
        latest_file = max(list_of_files, key=os.path.getctime)
    else:
        latest_file = list_of_files[0]
    print (latest_file, outputPath)
    if check == 'checking':
        'checking.......................ok'
    if check == 'running':
        'running.......................'
        if openFile=='open':
            openmaya(latest_file)
        print 'starting------------------->>>>>>'
        if mode == 'CH':
            deleteSetABC()
            createSets('CH',True)
        if mode == 'BG':
            deleteSetABC()
            createSets('BG',True)
        if mode == 'CAM':
            deleteSetABC()
            createManualTypeSets('camera','camera')
            # createManualTypeSets('transform','camera_s02_c080')
            # createManualSets('camera', 'camera_s000')
        if mode == 'PR':
            deleteSetABC()
            createSets('PR',True)
        if mode == 'MP':
            deleteSetABC()
            createSets('MP',True)
        if doExport=='export':
            exportABC(outputPath, framerange)
        writeDetailJson(shotcode, outputPath)
    print '>>>>>------------------------->>>end'

def mayaABCexport(shotlist, ver, fullrange, openfile, srcdep, dstdep, check):
    for shotcode in shotlist:
        tmp = shotcode.split('_')
        ep, shot = tmp[0], tmp[1]
        sourceSearchPath = 'J:/xkx/work/prod/%s/%s/%s' % (srcdep, ep, shot )
        outputPath = 'J:/xkx/work/prod/%s/%s/%s/work/auto/alembic/%s' % (dstdep, ep, shot, ver)
        print sourceSearchPath
        print outputPath        
        createDir(outputPath)
        # # ---------------------------------------------------------------------------------------------------------------- CH
        # hideHair(0)
        batchshot( shotcode, sourceSearchPath, outputPath, fullrange, openfile, 'CH', 'export', ver, check )
        # # ---------------------------------------------------------------------------------------------------------------- BG  
        batchshot( shotcode, sourceSearchPath, outputPath, 'startend', 'nopen', 'CAM', 'export', ver, check )
        batchshot(shotcode, sourceSearchPath, outputPath, 'startend', 'nopen', 'PR', 'export', ver, check)
        batchshot(shotcode, sourceSearchPath, outputPath, 'startend', 'nopen', 'BG', 'export', ver, check)
    print '------------------------END---------------------------'

#----------------------------------------------------------------------------------------------------------------------------------------------

# shots   = ['s02_c080']
# J:/xkx/work/prod/ani/s02/c080
# J:/xkx/work/prod/blk/s02/c080
# ['s02_c050','s02_c060','s02_c080','s02_c090','s02_c100','s02_c110','s02_c130','s02_c150','s02_c160']
# shots=['s02_c080','s02_c150']

shots=['s02_c110']  # v9, 4/27
mayaABCexport(shots, 'v9', 'startend', 'open', 'ani' ,'efx', 'running')

