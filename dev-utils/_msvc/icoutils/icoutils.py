import info


class subinfo(info.infoclass):
    def setTargets(self):
        build = "56"
        for ver in ["0.32.3"]:
            self.targets[ ver ] = f"https://files.kde.org/craft/autotools/packages/icoutils-{ver}-{build}-windows-mingw_{CraftCore.compiler.bits}-gcc.7z"
            self.targetDigestUrls[ ver ] = f"https://files.kde.org/craft/autotools/packages/icoutils-{ver}-{build}-windows-mingw_{CraftCore.compiler.bits}-gcc.7z.sha256"
            self.targetInstallPath[ ver ] = "dev-utils/icoutils"

        self.description = "The icoutils are a set of command-line programs for extracting and converting images in Microsoft Windows(R) icon and cursor files."
        self.webpage = "http://www.nongnu.org/icoutils/"
        self.defaultTarget = "0.32.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)


    def install(self):
        if not super().install():
            return False
        return (utils.createShim(os.path.join(self.imageDir(), "bin", "icotool.exe"), os.path.join(self.installDir(), "bin", "icotool.exe")) and
                utils.createShim(os.path.join(self.imageDir(), "bin", "wrestool.exe"), os.path.join(self.installDir(), "bin", "wrestool.exe")) )
