import os,sys,re,json
import maya.cmds as cmds

def findFileName(searchPath,fileType,filterName):
    filesExist = []
    if os.path.exists(searchPath):
        listFiles = os.listdir(searchPath)
        for item in listFiles:
            if os.path.isfile(os.path.join(searchPath, item)):
                if item.endswith(fileType):
                    if re.search(filterName,item,re.IGNORECASE):
                        filesExist.append(item)
        return filesExist
    else:
        return filesExist

def importABCforloop(searchPath,foundFiles,mode):
    for foundFile in foundFiles:
        name_abc = '%s' % (foundFile[:-4])
        file_abc = '%s/%s'%(searchPath,foundFile)
        if mode=='import':
            cmds.file(file_abc, i=True)
        if mode=='reference':
            cmds.file(file_abc, reference=1)
        if mode=='gpuABC':
            gpu_node = cmds.createNode('gpuCache')
            cmds.setAttr(gpu_node + '.cacheFileName', file_abc, type='string')
            parent_node = cmds.listRelatives(gpu_node, parent=True, fullPath=True)[0]
            cmds.rename(parent_node, name_abc)

def getJsonData(fulljsonfile):
    with open( fulljsonfile ) as json_file:
        data = json.load(json_file)
    return data

def assignSGCompareJson(fulljsonfile):
    shaderdic = getJsonData( fulljsonfile )
    objs = cmds.ls( ap=True,type='transform')
    for obj in objs:
        for v in shaderdic.items():
            se = v[0] 
            if re.search(se, obj):
                try:
                    cmds.sets(obj, edit=True, forceElement= se)
                    print(obj)
                    print(se,'---------------------------- set !!!!!')
                except:
                    print('TRY-----------PASS , maybe no shader to be assigned')
    print('done-----------------------------ALL')

def runDirs(pathabcs, mode):
    dirs = os.listdir(pathabcs)
    print(dirs)
    for eachdir in dirs:
        houdiniABC = os.path.join(pathabcs, eachdir)
        print(houdiniABC)
        # fulljsonfile = '%s/%s.json' %  (pathjson, assetname)
        foundFiles = findFileName(houdiniABC,'abc','')
        importABCforloop( houdiniABC, foundFiles, mode )   # import, reference, gpuABC
        # assignSGCompareJson(fulljsonfile)

def runDirect(pathabcs, mode):
    houdiniABC = os.path.join(pathabcs, '')
    print(houdiniABC)
    foundFiles = findFileName(houdiniABC,'abc','')
    importABCforloop( houdiniABC, foundFiles, mode )   # import, reference, gpuABC

# pathabcs = 'J:/bijj_fx/work/progress/efx/JJ04/S01/work/S01_C083/ABC/v10/INSIDE'
# runDirect( pathabcs, 'reference')
# pathabcs = 'J:/bijj_fx/work/progress/efx/JJ04/S01/work/S01_C083/ABC/v6/floorRock'
# runDirect( pathabcs, 'gpuABC')
# pathabcs = 'J:/bijj_fx/work/progress/efx/JJ04/S01/work/S01_C083/ABC/v6/floorRock'
# runDirs( pathabcs, 'gpuABC')
