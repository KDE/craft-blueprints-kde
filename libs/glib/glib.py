import info
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # tests in 2.81.0 fail to build
        self.options.dynamic.setDefault("buildTests", False)

    def setTargets(self):
        self.description = "GLib is a general-purpose, portable utility library, which provides many useful data types, macros, type conversions, string utilities, file utilities, a mainloop abstraction, and so on."
        self.webpage = "https://docs.gtk.org/glib/"
        self.releaseManagerId = 10024

        for ver in ["2.86.0", "2.89.0"]:
            majorMinorStr = ".".join(ver.split(".")[0:2])
            self.targets[ver] = f"https://download.gnome.org/sources/glib/{majorMinorStr}/glib-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"glib-{ver}"

        self.targetDigests["2.86.0"] = (["b5739972d737cfb0d6fd1e7f163dfe650e2e03740bb3b8d408e4d1faea580d6d"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.89.0"] = (["205bf5dab175de68f11e33be7bb36d4ad4c5a5097d8c0c88a8682b257b6293dc"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.89.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["libs/python"] = None
        self.buildDependencies["dev-utils/system-python3"] = None
        self.buildDependencies["dev-utils/pkgconf"] = None
        self.buildDependencies["python-modules/meson"] = None
        self.buildDependencies["python-modules/packaging"] = None
        self.runtimeDependencies["libs/libffi"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/dbus"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/pcre2"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.subinfo.options.isActive("libs/dbus"):
            self.subinfo.options.configure.cflags += (
                f"-I{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot() / 'include/dbus-1.0')}"
                f" -I{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot() / 'lib/dbus-1.0/include')}"
            )
        self.subinfo.options.configure.args += ["--wrap-mode=nodownload", "-Ddocumentation=false", "-Dinstalled_tests=false", "-Dman-pages=disabled"]
        if CraftCore.compiler.isUnix:
            self.subinfo.options.configure.ldflags += " -liconv"
        if CraftCore.compiler.isFreeBSD:
            self.subinfo.options.configure.args += ["-Dxattr=false", "-Dlibmount=disabled", "-Dselinux=disabled", "-Db_lundef=false"]

        self.subinfo.options.configure.args += [f'-Dtests={"true" if self.subinfo.options.dynamic.buildTests else "false"}']
