import info

import glob

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "git://anongit.freedesktop.org/libreoffice/dictionaries"
        self.webpage = "https://cgit.freedesktop.org/libreoffice/dictionaries/"
        self.description = "Hunspell Dictionaries by LibreOffice"

        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        srcDir = self.sourceDir()
        destDir = os.path.join(self.installDir(), "bin", "data", "hunspell")
        files = []
        for pattern in ["**/*.dic", "**/*.aff", "**/*.txt"]:
            files.extend(glob.glob(os.path.join(srcDir, pattern), recursive=True))
        for f in files:
            if not utils.copyFile(f, f.replace(srcDir, destDir), linkOnly=False):
                return False
        return True
