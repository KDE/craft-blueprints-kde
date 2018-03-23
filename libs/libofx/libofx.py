import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.9.12'] = "http://downloads.sourceforge.net/project/libofx/libofx/libofx-0.9.12.tar.gz"
        self.targetDigests['0.9.12'] = (['c15fa062fa11e759eb6d8c7842191db2185ee1b221a3f75e9650e2849d7b7373'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc['0.9.12'] = "libofx-0.9.12"
        self.patchToApply['0.9.12'] = [("libofx-0.9.5-20120131.diff", 1)]
        self.patchToApply['0.9.12'] += [("libofx-0.9.12-20180127.diff", 1)]

        if CraftCore.compiler.isMSVC():
            self.patchToApply['0.9.12'] += [("patch_daylight.diff", 1)]
        if CraftCore.compiler.isMinGW():
            self.patchToApply['0.9.12'] += [("libofx-0.9.12-20180127-mingw.diff", 1)]

        self.description = "a parser and an API for the OFX (Open Financial eXchange) specification"
        self.defaultTarget = '0.9.12'

    def setDependencies(self):
        self.runtimeDependencies["libs/libopensp"] = "default"
        self.runtimeDependencies["libs/iconv"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        # we use subinfo for now too
        CMakePackageBase.__init__(self)
