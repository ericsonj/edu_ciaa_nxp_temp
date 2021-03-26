from pymakelib import addon
from pymakelib import project

class CIAAAddon(addon.AddonAbstract):

    def generate_download(self, is_M0App=False, laod_InRAM=False):

        default_addr = "0x1A000000"
        downlaod_target = "FLASH"
        command = "flash write_image erase"

        download_m0 = []
        download_m0_target = ""

        if is_M0App and not laod_InRAM:
            download_m0_target = ".download_m0"
            download_m0 = [
            ".download_m0: $(TARGET_BIN)\n",
            "\t@echo DOWNLOAD to M0 FLASH\n",
            "\t$(Q)$(OOCD) -f $(OOCD_SCRIPT) \\\n"
            "\t\t-c \"init\" \\\n"
            "\t\t-c \"halt 0\" \\\n"
            "\t\t-c \"flash write_image erase $< 0x1B000000 bin\" \\\n"
            "\t\t-c \"reset run\" \\\n"
            "\t\t-c \"shutdown\" 2>&1\n\n"
        ]

        if laod_InRAM:
            downlaod_target = "RAM"
            default_addr = "0x20000000"
            command = "load_image"

        return download_m0 + [
            f"download: $(TARGET_BIN) {download_m0_target}\n",
            f"\t@echo DOWNLOAD to {downlaod_target}\n",
            "\t$(Q)$(OOCD) -f $(OOCD_SCRIPT) \\\n"
            "\t\t-c \"init\" \\\n"
            "\t\t-c \"halt 0\" \\\n"
            f"\t\t-c \"{command} $< {default_addr} bin\" \\\n"
            "\t\t-c \"reset run\" \\\n"
            "\t\t-c \"shutdown\" 2>&1\n"
        ]

    def init(self):
        download_mk = open('download.mk', 'w')
        download_mk.write(f"# File auto-generate by ciaa_addon.py\n\n")

        defs = self.projectSettings['C_SYMBOLS']

        if project.define('OOCD'):
            download_mk.write(f"OOCD={defs['OOCD']}\n")
        else:
            download_mk.write(f"OOCD=openocd\n")

        if project.define('OOCD_SCRIPT'):
            download_mk.write(f"OOCD_SCRIPT={defs['OOCD_SCRIPT']}\n")
        else:
            download_mk.write(f"OOCD_SCRIPT=\n")

        download_mk.write("\n")

        download_mk.writelines(
            self.generate_download(
                is_M0App    = project.define('M0_APP') == 'y',
                laod_InRAM  = project.define('LOAD_INRAM') == 'y'
            )
        )

        download_mk.close()
