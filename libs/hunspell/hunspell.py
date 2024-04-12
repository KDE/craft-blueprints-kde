import info
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = f"https://github.com/hunspell/hunspell.git"
        for ver in ["1.7.2"]:
            if CraftCore.compiler.isMSVC():
                self.targets[ver] = f"https://github.com/hunspell/hunspell/archive/v{ver}.tar.gz"
            else:
                self.targets[ver] = f"https://github.com/hunspell/hunspell/releases/download/v{ver}/hunspell-{ver}.tar.gz"

            self.targetInstSrc[ver] = f"hunspell-{ver}"

        if CraftCore.compiler.isMSVC():
            self.targetDigests["1.7.2"] = (["69fa312d3586c988789266eaf7ffc9861d9f6396c31fc930a014d551b59bbd6e"], CraftHash.HashAlgorithm.SHA256)
        else:
            self.targetDigests["1.7.2"] = (["11ddfa39afe28c28539fe65fc4f1592d410c1e9b6dd7d8a91ca25d85e9ec65b8"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Hunspell is the spell checker of LibreOffice, OpenOffice.org, Mozilla Firefox 3 & Thunderbird, Google Chrome, and it is also used by proprietary software packages, like macOS, InDesign, memoQ, Opera and SDL Trados."
        self.webpage = "http://hunspell.github.io/"
        self.defaultTarget = "1.7.2"

    def setDependencies(self):
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["data/hunspell-dictionaries"] = None


from Package.MSBuildPackageBase import *


class PackageMSVC(MSBuildPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.projectFile = os.path.join(self.sourceDir(), "msvc", "Hunspell.sln")
        self.buildTypes = {"Release": "Release_dll", "RelWithDebInfo": "Release_dll", "Debug": "Debug_dll"}

    def configure(self):
        utils.copyFile(os.path.join(self.sourceDir(), "msvc", "config.h"), os.path.join(self.sourceDir(), "config.h"))
        out = super().configure()
        utils.deleteFile(os.path.join(self.sourceDir(), "config.h"))
        return out

    def install(self):
        if not super().install(installHeaders=False):
            return False

        for h in ["atypes.hxx", "hunspell.h", "hunspell.hxx", "hunvisapi.h", "w_char.hxx"]:
            utils.copyFile(os.path.join(self.sourceDir(), "src", "hunspell", h), os.path.join(self.imageDir(), "include", "hunspell", h))
        return True


from Package.AutoToolsPackageBase import *


class PackageGNU(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.bootstrap = True
        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared"]


if CraftCore.compiler.isGCCLike():

    class Package(PackageGNU):
        pass

else:

    class Package(PackageMSVC):
        pass
