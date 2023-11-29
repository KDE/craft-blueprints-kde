import stat
from pathlib import Path

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["continous"] = "https://github.com/darealshinji/linuxdeploy-plugin-checkrt/releases/download/continuous/linuxdeploy-plugin-checkrt.sh"
        self.targetInstallPath["continous"] = "dev-utils/bin"
        self.description = "Have your AppImage check libgcc and libstdc++ dependencies at runtime. "
        self.webpage = "https://github.com/darealshinji/linuxdeploy-plugin-checkrt"
        self.defaultTarget = "continous"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)

    def unpack(self):
        return True

    def install(self):
        utils.createDir(self.installDir())
        for f in self.localFilePath():
            src = Path(f)
            dest = Path(self.installDir()) / src.name
            # we move the files so that on a reinstall the continous target gets redownloaded
            if not utils.moveFile(src, dest):
                return False
            dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return True
