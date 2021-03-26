import subprocess

FIRMWARE_V3_PATH    = "<%= firmware_path %>"                             
ARM_NONE_EABI_PATH  = "<%= arm_none_eabi_path %>"

def get_openocd_cfg():
    out = subprocess.Popen(["openocd", "-c", "dap"], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    if "invalid command name \"dap\"" in str(stdout):
        return f"{FIRMWARE_V3_PATH}/scripts/openocd/lpc4337_old.cfg"
    else:
        return f"{FIRMWARE_V3_PATH}/scripts/openocd/lpc4337_new.cfg"