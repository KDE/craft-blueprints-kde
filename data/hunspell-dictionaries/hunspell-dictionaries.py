import glob

import info


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
        self.runtimeDependencies["virtual/bin-base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        srcDir = self.sourceDir()
        if CraftCore.compiler.isWindows:
            destDir = os.path.join(self.installDir(), "bin", "data")
        else:
            destDir = os.path.join(self.installDir(), "share")
        files = []
        for pattern in ["**/*.dic", "**/*.aff", "**/*.txt"]:
            files.extend(glob.glob(os.path.join(srcDir, pattern), recursive=True))
        for f in files:
            if not utils.copyFile(f, os.path.join(destDir, "hunspell", os.path.basename(f)), linkOnly=False):
                return False
        return True
