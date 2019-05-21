import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['3.9.2', '4.0.3', '4.0.4', '4.0.9', '4.0.10']:
            self.targets[ver] = "http://download.osgeo.org/libtiff/tiff-" + ver + ".tar.gz"
            self.targetInstSrc[ver] = "tiff-" + ver
        self.patchToApply['3.9.2'] = [('tiff-3.9.2-20100418.diff', 1)]
        self.patchToApply['4.0.3'] = [('tiff-4.0.3-rename-test.diff', 1), ('tiff-4.0.3-20130124.diff', 1)]
        self.patchToApply['4.0.4'] = [('tiff-4.0.4-20130124.diff', 1)]
        self.targetDigests['3.9.2'] = '5c054d31e350e53102221b7760c3700cf70b4327'
        self.targetDigests['4.0.3'] = '652e97b78f1444237a82cbcfe014310e776eb6f0'
        self.targetDigests['4.0.9'] = (['6e7bdeec2c310734e734d19aae3a71ebe37a4d842e0e23dbb1b8921c0026cfcd'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["4.0.9"] = 2

        self.description = "a library to manipulate TIFF image files"
        self.webpage = "http://www.simplesystems.org/libtiff/"
        self.defaultTarget = '4.0.10'

    def setDependencies(self):
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # both examples and tests can be run here
        self.subinfo.options.configure.args = "-DBUILD_TESTS=OFF -DBUILD_TOOLS=OFF"
