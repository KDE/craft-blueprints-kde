import info

from Package.MSBuildPackageBase import MSBuildPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.2.1"]:
            self.targets[ver] = "https://github.com/winlibs/libffi/archive/libffi-%s.tar.gz" % ver
            self.archiveNames[ver] = "libffi-libffi-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "libffi-libffi-%s" % ver
        self.targetDigests['3.2.1'] = (
            ['9f8e1133c6b9f72b73943103414707a1970e2e9b1d332c3df0d35dac1d9917e5'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.2.1"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = "default"


class PackageCMake(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)

        folderSuffix = "x64"
        if CraftCore.compiler.isX86():
            folderSuffix = "x86"
        self.subinfo.options.configure.projectFile = os.path.join(self.sourceDir(), "win32", f"vc14_{folderSuffix}",
                                                                  "libffi-msvc.sln")

    def install(self):
        if not MSBuildPackageBase.install(self, installHeaders=False):
            return False
        utils.copyFile(os.path.join(self.sourceDir(), "include", "ffi.h"),
                       os.path.join(self.imageDir(), "include", "ffi.h"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "include", "ffi_common.h"),
                       os.path.join(self.imageDir(), "include", "ffi_common.h"), False)
        if CraftCore.compiler.isX86():
            utils.copyFile(os.path.join(self.sourceDir(), "src", "x86", "ffitarget.h"),
                           os.path.join(self.imageDir(), "include", "ffitarget.h"), False)
        else:
            utils.copyFile(os.path.join(self.sourceDir(), "src", "ia64", "ffitarget.h"),
                           os.path.join(self.imageDir(), "include", "ffitarget.h"), False)
        return True


from Package.AutoToolsPackageBase import *


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--enable-shared --disable-static "


if CraftCore.compiler.isMinGW():
    class Package(PackageMSys):
        pass
else:
    class Package(PackageCMake):
        pass
