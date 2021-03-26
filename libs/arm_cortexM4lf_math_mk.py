import subprocess
from pymakelib import module
from pymakelib.toolchain import confARMeabiGCC
from pathlib import Path
from scripts import config

LIBARM_CORTEXM4LF_MATH = config.FIRMWARE_V3_PATH + '/libs/cmsis_dsp/lib/libarm_cortexM4lf_math.hexlib'
LIB_FOLDER_OUT = 'Release/ciaa_app/' + config.FIRMWARE_V3_PATH + '/libs/lpc_open/lib'

def init(mh: module.ModuleHandle):
    """
    Create static library libarm_cortexM4lf_math.a
    """
    staticLib = module.StaticLibrary(name='arm_cortexM4lf_math', outputDir=LIB_FOLDER_OUT)
    try:
        if mh.getGoal() == 'all':
            
            toolset = confARMeabiGCC(binLocation=config.ARM_NONE_EABI_PATH)
            staticLib.setRebuild(True)
            Path(LIB_FOLDER_OUT).mkdir(parents=True, exist_ok=True)
            subprocess.call([
                toolset['OBJCOPY'],
                '-I', 'ihex',
                '-O', 'binary',
                LIBARM_CORTEXM4LF_MATH,
                LIB_FOLDER_OUT + '/libarm_cortexM4lf_math.a'])

    except Exception as e:
            print(e)
    return staticLib

def getSrcs(m):
    return None

def getIncs(m):
    return None