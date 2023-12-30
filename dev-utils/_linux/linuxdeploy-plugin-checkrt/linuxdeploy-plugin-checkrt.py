import stat
from pathlib import Path
import info
from Package.BinaryPackageBase import BinaryPackageBase
import utils


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["continous"] = "https://github.com/darealshinji/linuxdeploy-plugin-checkrt/releases/download/continuous/linuxdeploy-plugin-checkrt.sh"
        self.targetInstallPath["continous"] = "dev-utils/bin"
        self.description = "Have your AppImage check libgcc and libstdc++ dependencies at runtime. "
        self.webpage = "https://github.com/darealshinji/linuxdeploy-plugin-checkrt"
        self.defaultTarget = "continous"
        self.patchLevel["continous"] = 1

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **args):
        super().__init__()

    def unpack(self):
        patches = self.subinfo.patchesToApply()
        for patch in patches:
            patchfile = self.blueprintDir() / patch[0]
            utils.applyPatch(self.localFilePath()[0].parent, patchfile, patch[1])
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
