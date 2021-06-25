import info


class subinfo(info.infoclass):

    def registerOptions(self):
        if CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):

        for ver in ["0.27.1"]:
            self.targets[ver] = f"https://github.com/Exiv2/exiv2/archive/{ver}.tar.gz"
            self.archiveNames[ver] = f"exiv2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"exiv2-{ver}"

        self.targetDigests["0.27.1"] = (['1b3766b2c203ce213a4195de14d61694017ec1a69d15d4575bccecef130990fe'], CraftHash.HashAlgorithm.SHA256)

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
        else:
            self.subinfo.options.configure.args += " -DBUILD_SHARED_LIBS=ON"
