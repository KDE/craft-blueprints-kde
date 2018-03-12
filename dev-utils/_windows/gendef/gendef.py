import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets[
            'svnHEAD'] = 'https://mingw-w64.svn.sourceforge.net/svnroot/mingw-w64/trunk/mingw-w64-tools/gendef'

        self.defaultTarget = 'svnHEAD'

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = "default"


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
