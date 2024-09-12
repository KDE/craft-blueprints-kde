import info
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        ## tests in 2.81.0 fail to build
        self.options.dynamic.setDefault("buildTests", False)

    def setTargets(self):
        for ver in ["2.79.0", "2.81.0"]:
            majorMinorStr = ".".join(ver.split(".")[0:2])
            self.targets[ver] = f"https://download.gnome.org/sources/glib/{majorMinorStr}/glib-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"glib-{ver}"
        self.targetDigests["2.79.0"] = (["d7ebde5505f5c4741a04ffe32f6927bd165b13caaabe18e962ddc58c811f84c9"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.81.0"] = (["1665188ed9cc941c0a189dc6295e6859872523d1bfc84a5a84732a7ae87b02e4"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.81.0"

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
        if not CraftCore.compiler.isWindows:
            self.runtimeDependencies["libs/iconv"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.subinfo.options.isActive("libs/dbus"):
            self.subinfo.options.configure.cflags += (
                f"-I{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot() / 'include/dbus-1.0')}"
                f" -I{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot() / 'lib/dbus-1.0/include')}"
            )
        self.subinfo.options.configure.args += ["--wrap-mode=nodownload", "-Dgtk_doc=false", "-Dinstalled_tests=false", "-Dman=false"]
        if CraftCore.compiler.isUnix:
            self.subinfo.options.configure.ldflags += f" -lintl -liconv"
        if CraftCore.compiler.isFreeBSD:
            self.subinfo.options.configure.args += ["-Dxattr=false", "-Dlibmount=disabled", "-Dselinux=disabled", "-Db_lundef=false"]

        if not self.subinfo.options.dynamic.buildTests:
            self.subinfo.options.configure.args += ["-Dtests=false"]
