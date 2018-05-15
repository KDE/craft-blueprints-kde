import info

from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.4.5"]:
            self.targets[ver] = f"http://oligarchy.co.uk/xapian/{ver}/xapian-core-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"xapian-core-{ver}"
        self.targetDigests["1.4.5"] = (['85b5f952de9df925fd13e00f6e82484162fd506d38745613a50b0a2064c6b02b'], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.isWindows:
            self.patchToApply["1.4.5"] = [("xapian-core-1.4.5-20180515.diff", 1)]
        self.description = "Open Source Search Engine library"
        self.webpage = "https://xapian.org/"
        self.defaultTarget = "1.4.5"

    def setDependencies(self):
        self.runtimeDependencies["libs/libxslt"] = "default"
        self.runtimeDependencies["libs/zlib"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared "


    def postInstall(self):
        if not self.copyToMsvcImportLib():
            return False
        return (self.patchInstallPrefix([os.path.join(self.installDir(), "lib" , "cmake", "xapian", "xapian-config.cmake")],
                                        OsUtils.toMSysPath(self.subinfo.buildPrefix),
                                        OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())) and
                self.patchInstallPrefix([os.path.join(self.installDir(), "bin", "xapian-config")],
                                        OsUtils.toMSysPath(self.subinfo.buildPrefix),
                                        OsUtils.toMSysPath(CraftCore.standardDirs.craftRoot())))

