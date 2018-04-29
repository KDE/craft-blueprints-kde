import info

import glob

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "git://anongit.freedesktop.org/libreoffice/dictionaries"
        for ver in ["6.0.1.1"]:
            mainVersion = ".".join(ver.split(".")[:3])
            self.targets[ver] = f"https://download.documentfoundation.org/libreoffice/src/{mainVersion}/libreoffice-dictionaries-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"http://download.documentfoundation.org/libreoffice/src/{mainVersion}/libreoffice-dictionaries-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"libreoffice-{ver}"
        self.patchLevel["6.0.1.1"] = 1

        self.webpage = "https://cgit.freedesktop.org/libreoffice/dictionaries/"
        self.description = "Hunspell Dictionaries by LibreOffice"

        self.defaultTarget = "6.0.1.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def make(self):
        self.cleanBuild()
        if not utils.globCopyDir(os.path.join(self.sourceDir(), "dictionaries"), self.buildDir(), ["**/*.dic", "**/*.aff"]):
            return False
        cwd = os.path.join(self.buildDir())
        return (utils.system(["rcc", "--project", "-o", os.path.join(self.buildDir(), "hunspell.qrc")], cwd=cwd) and
                utils.system(["rcc", "--binary", "-o", os.path.join(self.buildDir(), "hunspell.rcc"), os.path.join(self.buildDir(), "hunspell.qrc")],cwd=cwd))

    def install(self):
        if CraftCore.compiler.isWindows:
            destDir = os.path.join(self.installDir(), "bin", "data")
        else:
            destDir = os.path.join(self.installDir(), "share")
        self.cleanImage()
        if not utils.globCopyDir(os.path.join(self.sourceDir(), "dictionaries"), os.path.join(destDir, "hunspell"), ["**/*.txt"]):
            return False
        return utils.copyFile(os.path.join(self.buildDir(), "hunspell.rcc"), os.path.join(destDir, "hunspell", "hunspell.rcc"), linkOnly=False)
