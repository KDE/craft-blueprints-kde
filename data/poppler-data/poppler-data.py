import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "the poppler CJK encoding data"
        self.svnTargets['master'] = "git://git.freedesktop.org/git/poppler/poppler-data"

        # use poppler data matching the latest poppler release used in poppler.py
        v = '0.4.9'
        self.defaultTarget = v
        self.targets[v] = 'http://poppler.freedesktop.org/poppler-data-' + v + '.tar.gz'
        self.targetInstSrc[v] = 'poppler-data-' + v
        self.targetDigests[v] = (['1f9c7e7de9ecd0db6ab287349e31bf815ca108a5a175cf906a90163bdbe32012'], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
