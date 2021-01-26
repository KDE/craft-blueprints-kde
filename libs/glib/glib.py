import info

from Package.MSBuildPackageBase import MSBuildPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.66.4"]:
            majorMinorStr = '.'.join(ver.split('.')[0:2])
            self.targets[ver] = f"https://download.gnome.org/sources/glib/{majorMinorStr}/glib-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"glib-{ver}"
        if CraftCore.compiler.isMSVC():
            self.patchToApply["2.66.3"] = [("glib-2.66.3-20201204.diff", 1)]
        self.targetDigests["2.66.3"] = (['79f31365a99cb1cc9db028625635d1438890702acde9e2802eae0acebcf7b5b1'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.66.4"] = (['97df8670e32f9fd4f7392b0980e661dd625012015d58350da1e58e343f4af984'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.66.4"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/python3"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["python-modules/meson"] = None
        self.runtimeDependencies["libs/libffi"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/dbus"] = None
        self.runtimeDependencies["libs/gettext"] = None
        if not OsUtils.isWin():
            self.runtimeDependencies["libs/iconv"] = None

from Package.MesonPackageBase import *


class Package(MesonPackageBase):
    def __init__(self):
        MesonPackageBase.__init__(self)
        self.subinfo.options.configure.cflags += (f"-I{OsUtils.toUnixPath(CraftStandardDirs.craftRoot() / 'include/dbus-1.0')}"
                                                  f" -I{OsUtils.toUnixPath(CraftStandardDirs.craftRoot() / 'lib/dbus-1.0/include')}")
        # cmake pcre does not provide .pc files
        self.subinfo.options.configure.args += ["-Dinternal_pcre=true", "-Diconv=external"]
        if CraftCore.compiler.isUnix:
            self.subinfo.options.configure.ldflags += " -lintl"
