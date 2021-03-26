import os
from os.path import basename
from pymakelib import git
from pymakelib import MKVARS
from pymakelib import toolchain as tool
from pymakelib import addon
from pymakelib.eclipse_addon import EclipseAddon
from scripts import vscode_addon
from pymakelib import Define as D
from scripts import config
from scripts import ciaa_addon

# Add addons for Eclipse and vscode
addon.add(EclipseAddon)
addon.add(vscode_addon.vscode_init)
addon.add(ciaa_addon.CIAAAddon)


PROJECT_NAME = basename(os.getcwd())
FOLDER_OUT = 'Release/ciaa_app/'
TARGET_ELF = FOLDER_OUT + PROJECT_NAME + ".elf"
TARGET_MAP = FOLDER_OUT + PROJECT_NAME + ".map"
TARGET_HEX = FOLDER_OUT + PROJECT_NAME + ".hex"
TARGET_BIN = FOLDER_OUT + PROJECT_NAME + ".bin"
TARGET_SIZE = FOLDER_OUT + PROJECT_NAME + ".size"
TARGET_LST = FOLDER_OUT + PROJECT_NAME + ".lst"
TARGET_CSV = FOLDER_OUT + PROJECT_NAME + "names.csv"


def getProjectSettings():
    return {
        'PROJECT_NAME': PROJECT_NAME,
        'FOLDER_OUT':   FOLDER_OUT
    }


def getTargetsScript():
    TARGETS = {
        'TARGET': {
            'LOGKEY':  'ELF',
            'FILE':    TARGET_ELF,
            'SCRIPT':  [MKVARS.LD, '-o', '$@', MKVARS.OBJECTS, MKVARS.LDFLAGS, MKVARS.STATIC_LIBS]
        },
        'TARGET_HEX': {
            'LOGKEY':   'HEX',
            'FILE':     TARGET_HEX,
            'SCRIPT':   [MKVARS.OBJCOPY, '-O', 'ihex', MKVARS.TARGET, TARGET_HEX]
        },
        'TARGET_BIN': {
            'LOGKEY':   'BIN',
            'FILE':     TARGET_BIN,
            'SCRIPT':   [MKVARS.OBJCOPY, '-O', 'binary', MKVARS.TARGET, TARGET_BIN]
        },
        'TARGET_LST': {
            'LOGKEY':   'LST',
            'FILE':     TARGET_LST,
            'SCRIPT':   ['$(OBJDUMP)', '-xdS', MKVARS.TARGET, '>', TARGET_LST]
        },
        'TARGET_NM': {
            'LOGKEY':   'NM',
            'FILE':     TARGET_CSV,
            'SCRIPT':   [MKVARS.NM, '-nAsSCpl', MKVARS.TARGET, '>', TARGET_CSV]
        },
        'TARGET_SIZE': {
            'LOGKEY':   'SIZE',
            'FILE':     TARGET_SIZE,
            'SCRIPT':   [MKVARS.SIZE, '-Ax', MKVARS.TARGET, '>', TARGET_SIZE]
        },
        'RESUME':   {
            'LOGKEY':   '>>',
            'FILE':     'RESUME',
            'SCRIPT':   ['@pybuildanalyzer2', MKVARS.TARGET]
        }
    }

    return TARGETS


def getCompilerSet():
    toolset = tool.confARMeabiGCC(binLocation=config.ARM_NONE_EABI_PATH)
    return toolset


LIBRARIES = []


def getCompilerOpts():

    PROJECT_DEF = {
        '__USE_LPCOPEN':    None,
        'CHIP_LPC43XX':     None,
        'ARM_MATH_CM4':     None,
        '__USE_NEWLIB':     None,
        'CORE_M4':          None,
        '__FPU_PRESENT':    1,
        'USE_SAPI':         None,
        'BOARD':            D('edu_ciaa_nxp'),
        'OOCD_SCRIPT':      config.get_openocd_cfg(),
        'LOAD_INRAM':       D('n'),
        'M0_APP':           D('n')
    }

    return {
        'MACROS': PROJECT_DEF,
        'MACHINE-OPTS': [
            '-mcpu=cortex-m4',
            '-mthumb',
            '-mfloat-abi=hard',
            '-mfpu=fpv4-sp-d16',
        ],
        'OPTIMIZE-OPTS': [
        ],
        'OPTIONS': [
            '-ffunction-sections',
            '-fstack-usage'
        ],
        'DEBUGGING-OPTS': [
            '-ggdb3',
            '-Og'
        ],
        'PREPROCESSOR-OPTS': [
            '-MP',
            '-MMD'
        ],
        'WARNINGS-OPTS': [
        ],
        'CONTROL-C-OPTS': [
            '-std=c99'
        ],
        'GENERAL-OPTS': [
        ],
        'LIBRARIES': LIBRARIES
    }


def getLinkerOpts():
    return {
        'LINKER-SCRIPT': [
            f"-L{config.FIRMWARE_V3_PATH}/libs/lpc_open/lib",
            f"-T{config.FIRMWARE_V3_PATH}/libs/lpc_open/lib/link.ld"
        ],
        'MACHINE-OPTS': [
            '-mcpu=cortex-m4',
            '-mthumb',
            '-mfloat-abi=hard',
            '-mfpu=fpv4-sp-d16',
        ],
        'GENERAL-OPTS': [
            '--specs=nano.specs',
        ],
        'LINKER-OPTS': [
            '-nostartfiles',
            '-Wl,-gc-sections',
            '-Wl,-Map='+TARGET_MAP,
            '-Wl,--cref',
        ],
        'LIBRARIES': LIBRARIES
    }
