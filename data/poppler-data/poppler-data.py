import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "git://git.freedesktop.org/git/poppler/poppler-data"
        for v in ['0.4.6', '0.4.7', '0.4.9']:
            self.targets[v] = 'http://poppler.freedesktop.org/poppler-data-' + v + '.tar.gz'
            self.targetInstSrc[v] = 'poppler-data-' + v
        self.patchToApply['0.4.7'] = [("poppler-data-0.4.7-20170810.diff", 1)]
        self.targetDigests['0.4.7'] = '556a5bebd0eb743e0d91819ba11fd79947d8c674'
        self.targetDigests['0.4.9'] = (['1f9c7e7de9ecd0db6ab287349e31bf815ca108a5a175cf906a90163bdbe32012'], CraftHash.HashAlgorithm.SHA256)

        self.description = "the poppler CJK encoding data"
        self.defaultTarget = '0.4.9'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
