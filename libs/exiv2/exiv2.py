import info


class subinfo(info.infoclass):

    def registerOptions(self):
        if CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        for ver in ['0.24', '0.25']:
            self.targets[ver] = 'http://www.exiv2.org/releases/exiv2-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'exiv2-%s' % ver

        for ver in ["0.27.0a"]:
            self.targets[ver] = f"http://www.exiv2.org/releases/exiv2-{ver}-Source.tar.gz"
            self.targetInstSrc[ver] = f"exiv2-{ver[0:-1]}-Source"

        for ver in ["0.27.1"]:
            self.targets[ver] = f"https://github.com/Exiv2/exiv2/archive/{ver}.tar.gz"
            self.archiveNames[ver] = f"exiv2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"exiv2-{ver}"

        self.targetDigests['0.24'] = '2f19538e54f8c21c180fa96d17677b7cff7dc1bb'
        self.patchToApply['0.24'] = ('exiv2-0.22-20120117.diff', 1)
        self.patchToApply['0.25'] = ('exiv2-0.25-20150826.diff', 1)
        self.targetDigests['0.25'] = 'adb8ffe63916e7c27bda9792e690d1330ec7273d'
        self.patchToApply["0.27.0a"] = [('exiv2-0.27.0a-20190105.diff', 1),
                                        ("exiv2-0.27.0a-20190201.diff", 1)]
        self.targetDigests["0.27.0a"] = (['a4adfa7aaf295b0383adead476f8e0493b9d6c6c7570d5884d2ebf8a2871902f'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.27.1"] = (['1b3766b2c203ce213a4195de14d61694017ec1a69d15d4575bccecef130990fe'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["0.27.0a"] = 1

        self.svnTargets['master'] = 'https://github.com/Exiv2/exiv2.git'

        self.description = "an image metadata library"
        self.defaultTarget = '0.27.1'

    def setDependencies(self):
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/expat"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libcurl"] = None
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DEXIV2_BUILD_SAMPLES=OFF -DEXIV2_ENABLE_NLS=OFF -DIconv_IS_BUILT_IN=OFF"
        if CraftCore.compiler.isWindows:
            self.subinfo.options.configure.args += " -DICONV_ACCEPTS_CONST_INPUT=ON -DEXIV2_ENABLE_WIN_UNICODE=OFF"
        if CraftCore.compiler.isMinGW() and self.buildTarget == "0.27.0a":
            # https://github.com/Exiv2/exiv2/issues/421
            self.subinfo.options.configure.args += " -DBUILD_SHARED_LIBS=OFF"
        else:
            self.subinfo.options.configure.args += " -DBUILD_SHARED_LIBS=ON"
