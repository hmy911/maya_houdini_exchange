import os,sys,re,json
import maya.cmds as cmds
import maya.mel
import glob

def createDir(createPath):
    if not os.path.exists(createPath):
        os.makedirs(createPath)

def openmaya(fullfilename):
    cmds.file(fullfilename,force=True, open=True , prompt = False)

def export_alembic(obj,exportPath,startframe,endframe):
    objDict = {'kStart': startframe , 'kEnd': endframe , 'kRoot': '-root' , 'kExportfile': exportPath}
    objDict['kRoot'] = obj
    fmt = 'AbcExport -j "-writeVisibility -worldSpace -renderableOnly -uvWrite -frameRange %(kStart)s %(kEnd)s -root %(kRoot)s -file %(kExportfile)s"' % objDict
    maya.mel.eval(fmt)

def createManualSets(typename,strManual):
    cmds.select(clear=1)
    customtube = cmds.ls("%s" % strManual)
    cmds.select(customtube,add=1)
    cmds.sets(name='ABC_%s'% typename)

def createAssemblesSets(typename):
    cmds.select(clear=1)
    customtube = cmds.ls(assemblies=1)
    cmds.select(customtube,add=1)
    cmds.sets(name='ABC_%s'% typename)  

def maGetFilename():
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    raw_name, extension = os.path.splitext(filename)
    return raw_name

def exportABC(outputPath, abcname):
    allsets = cmds.ls(type='objectSet')
    for eachset in allsets:
        if re.search('ABC',eachset):
            createDir(outputPath)
            exportFile = '%s/%s.abc' % (outputPath, abcname)
            strSets = ' -root '.join(eachset)
            getSets = cmds.sets(eachset,q=1)
            if getSets:
                strSets = ' -root '.join(getSets)
                export_alembic(strSets,exportFile,0,0)

def mayaExportShadingGroupJson(outputPathJson):
    createDir('%s' % outputPathJson )
    fulljsonfile = '%s/%s.json' % (outputPathJson, maGetFilename())
    shading_engines = cmds.ls(type='shadingEngine')
    connections_dict = {}
    for se in shading_engines:
        connections = cmds.sets(se, q=True)
        connections_dict[se] = connections
    for se, connections in connections_dict.items():
        print(  '%s =========>  :   %s' %(se, connections) )
    with open( fulljsonfile , "w") as f:
        json.dump(connections_dict, f, indent=4)
    print('done')

def run(latest_file, rootpath, ver):
    outputPath = '%s/%s/fromMaya' % (rootpath, ver)
    outputPathJson = '%s/json' % (outputPath)
    openmaya(latest_file)
    mayaExportShadingGroupJson(outputPathJson)
    createAssemblesSets( "assemblie")
    exportABC(outputPath, maGetFilename())

def main(rootpath, ver, runfolder):
    sourcePath = '%s/%s/%s' % (rootpath, ver, runfolder)
    print(sourcePath)
    list_of_files = glob.glob('%s/*.ma' % sourcePath )
    for eachfile in list_of_files:
        print(eachfile)
        run(eachfile, rootpath, ver)


# main( 'D:/prj/ep00/sh00/', 'try1' )





