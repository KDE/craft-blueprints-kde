import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.78.1"]:
            majorMinorStr = ".".join(ver.split(".")[0:2])
            self.targets[ver] = f"https://download.gnome.org/sources/glib/{majorMinorStr}/glib-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"glib-{ver}"
        self.targetDigests["2.78.1"] = (["915bc3d0f8507d650ead3832e2f8fb670fce59aac4d7754a7dab6f1e6fed78b2"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.78.1"

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
        self.runtimeDependencies["libs/pcre2"] = None
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
        self.subinfo.options.configure.args += ["--wrap-mode=nodownload"]
        if CraftCore.compiler.isUnix:
            self.subinfo.options.configure.ldflags += f" -lintl -liconv"
        if CraftCore.compiler.isFreeBSD:
            self.subinfo.options.configure.args += ["-Dxattr=false", "-Dlibmount=disabled", "-Dselinux=disabled", "-Db_lundef=false"]
        elif CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["-Dtests=false"]
