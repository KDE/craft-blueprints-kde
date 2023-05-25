import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "(URW)++ base 35 font set"
        self.svnTargets['master'] = "https://github.com/ArtifexSoftware/urw-base35-fonts"

        v = '20200910'
        self.defaultTarget = v
        self.targets[v] = 'https://github.com/ArtifexSoftware/urw-base35-fonts/archive/refs/tags/' + v + '.tar.gz'
        self.targetInstSrc[v] = 'urw-base35-fonts-' + v
        self.targetDigests[v] = (['71fb27baadf5abc4ff624cdede02038681acd5fffdc728a5b2e7808713b80cb2f2174f90a1862e69d390c4434c49d5167ab095100032fa3ba80b586eb8ae51d1'], CraftHash.HashAlgorithm.SHA512)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.SourceOnlyPackageBase import *


class Package(SourceOnlyPackageBase):
    def __init__(self):
        SourceOnlyPackageBase.__init__(self)

    def install(self):
        fontsSrcDir = os.path.join(self.sourceDir(), "fonts")
        fontsDestDir = os.path.join(self.imageDir(), "share", "fonts");
        utils.globCopyDir(fontsSrcDir, fontsDestDir, ["*.otf"], linkOnly=False)
        return True
