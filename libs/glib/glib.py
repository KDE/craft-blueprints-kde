import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.68.4"]:
            majorMinorStr = ".".join(ver.split(".")[0:2])
            self.targets[ver] = f"https://download.gnome.org/sources/glib/{majorMinorStr}/glib-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"glib-{ver}"
        self.targetDigests["2.68.4"] = (["62fd061d08a75492617e625a73e2c05e259f831acbb8e1f8b9c81f23f7993a3b"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.68.4"] = [("glib-2.68.4-20231105.diff", 1)]
        self.patchLevel["2.68.4"] = 1

        self.defaultTarget = "2.68.4"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/python3"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["python-modules/meson"] = None
        self.buildDependencies["python-modules/packaging"] = None
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
        if self.subinfo.options.isActive("libs/dbus"):
            self.subinfo.options.configure.cflags += (
                f"-I{OsUtils.toUnixPath(CraftStandardDirs.craftRoot() / 'include/dbus-1.0')}"
                f" -I{OsUtils.toUnixPath(CraftStandardDirs.craftRoot() / 'lib/dbus-1.0/include')}"
            )
        # cmake pcre does not provide .pc files
        self.subinfo.options.configure.args += ["-Dinternal_pcre=true", "-Diconv=external", "--wrap-mode=nodownload"]
        if CraftCore.compiler.isUnix:
            self.subinfo.options.configure.ldflags += f" -lintl -liconv"
        if CraftCore.compiler.isFreeBSD:
            self.subinfo.options.configure.args += ["-Dxattr=false", "-Dlibmount=disabled", "-Dselinux=disabled", "-Db_lundef=false"]
