import info

from Package.MSBuildPackageBase import MSBuildPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.2.1"]:
            if OsUtils.isWin():
                self.targets[ver] = f"https://github.com/winlibs/libffi/archive/libffi-{ver}.tar.gz"
                self.archiveNames[ver] = f"libffi-libffi-{ver}.tar.gz"
                self.targetInstSrc[ver] = f"libffi-libffi-{ver}"
                self.patchLevel[ver] = 2
            else:
                self.targets[ver] = f"ftp://sourceware.org/pub/libffi/libffi-{ver}.tar.gz"
                self.targetInstSrc[ver] = f"libffi-{ver}"

        if OsUtils.isWin():
            self.targetDigests['3.2.1'] = (
                ['9f8e1133c6b9f72b73943103414707a1970e2e9b1d332c3df0d35dac1d9917e5'], CraftHash.HashAlgorithm.SHA256)
        else:
            self.targetDigests['3.2.1'] = (
                ['d06ebb8e1d9a22d19e38d63fdb83954253f39bedc5d46232a05645685722ca37'], CraftHash.HashAlgorithm.SHA256)


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


class PackageAutoTools(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--enable-shared --disable-static"


if not OsUtils.isWin():
    class Package(PackageAutoTools):
        pass
else:
    class Package(PackageCMake):
        pass
