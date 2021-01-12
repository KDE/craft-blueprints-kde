import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "the poppler CJK encoding data"
        self.svnTargets['master'] = "git://git.freedesktop.org/git/poppler/poppler-data"

        # use poppler data matching the latest poppler release used in poppler.py
        v = '0.4.10'
        self.defaultTarget = v
        self.targets[v] = 'https://poppler.freedesktop.org/poppler-data-' + v + '.tar.gz'
        self.targetInstSrc[v] = 'poppler-data-' + v
        self.targetDigests[v] = (['6e2fcef66ec8c44625f94292ccf8af9f1d918b410d5aa69c274ce67387967b30'], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
