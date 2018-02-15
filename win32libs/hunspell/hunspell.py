import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets[ "master"] = f"https://github.com/hunspell/hunspell.git"
        for ver in ["1.6.2"]:
            self.targets[ver] = f"https://github.com/hunspell/hunspell/archive/v1.6.2.tar.gz"
            self.archiveNames[ver] = f"hunspell-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"hunspell-{ver}"
        self.targetDigests["1.6.2"] = (['3cd9ceb062fe5814f668e4f22b2fa6e3ba0b339b921739541ce180cac4d6f4c4'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Hunspell is the spell checker of LibreOffice, OpenOffice.org, Mozilla Firefox 3 & Thunderbird, Google Chrome, and it is also used by proprietary software packages, like macOS, InDesign, memoQ, Opera and SDL Trados."
        self.webpage = "http://hunspell.github.io/"
        self.defaultTarget = "1.6.2"

    def setDependencies( self ):
        self.buildDependencies["dev-util/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/gettext"] = "default"
        self.runtimeDependencies["win32libs/win_iconv"] = "default"

from Package.MSBuildPackageBase import *

class PackageMSVC(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)

        if CraftCore.compiler.isX86():
            self.subinfo.options.configure.args = " /p:Platform=Win32"
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
        self.subinfo.options.configure.args += " --disable-static --enable-shared"

if CraftCore.compiler.isGCCLike():
    class Package(PackageGNU):
        pass
else:
    class Package(PackageMSVC):
        pass
