import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets[ "master"] = f"https://github.com/hunspell/hunspell.git"
        for ver in ["1.6.2", "1.7.0"]:
            self.targets[ver] = f"https://github.com/hunspell/hunspell/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"hunspell-{ver}"
        self.targetDigests["1.6.2"] = (['3cd9ceb062fe5814f668e4f22b2fa6e3ba0b339b921739541ce180cac4d6f4c4'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.7.0"] = (['bb27b86eb910a8285407cf3ca33b62643a02798cf2eef468c0a74f6c3ee6bc8a'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Hunspell is the spell checker of LibreOffice, OpenOffice.org, Mozilla Firefox 3 & Thunderbird, Google Chrome, and it is also used by proprietary software packages, like macOS, InDesign, memoQ, Opera and SDL Trados."
        self.webpage = "http://hunspell.github.io/"
        self.defaultTarget = "1.7.0"

    def setDependencies( self ):
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["data/hunspell-dictionaries"] = None

from Package.MSBuildPackageBase import *


class PackageMSVC(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)
        self.subinfo.options.configure.projectFile = os.path.join(self.sourceDir(), "msvc", "Hunspell.sln")
        self.buildTypes = {"Release" : "Release_dll", "RelWithDebInfo" : "Release_dll", "Debug" : "Debug_dll" }

    def compile(self):
        utils.copyFile(os.path.join(self.sourceDir(), "msvc", "config.h"), os.path.join(self.sourceDir(), "config.h"))
        out = super().compile()
        utils.deleteFile(os.path.join(self.sourceDir(), "config.h"))
        return out


    def install(self):
        if not MSBuildPackageBase.install(self, installHeaders=False):
            return False

        for h in ["atypes.hxx", "hunspell.h", "hunspell.hxx", "hunvisapi.h", "w_char.hxx"]:
            utils.copyFile(os.path.join(self.sourceDir(), "src", "hunspell", h), os.path.join(self.imageDir(), "include", "hunspell", h))
        return True

from Package.AutoToolsPackageBase import *


class PackageGNU(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared"]

if CraftCore.compiler.isGCCLike():
    class Package(PackageGNU):
        pass
else:
    class Package(PackageMSVC):
        pass
