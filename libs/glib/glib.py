import info

from Package.MSBuildPackageBase import MSBuildPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.49.4"]:
            if OsUtils.isWin():
                self.targets[ver] = f"https://github.com/winlibs/glib/archive/glib-{ver}.tar.gz"
                self.archiveNames[ver] = f"glib-glib{ver}.tar.gz"
                self.targetInstSrc[ver] = f"glib-glib-{ver}"
            else:
                majorMinorStr = '.'.join(ver.split('.')[0:2])
                self.targets[ver] = f"https://ftp.gnome.org/pub/gnome/sources/glib/{majorMinorStr}/glib-{ver}.tar.xz"
                self.targetInstSrc[ver] = f"glib-{ver}"

        if OsUtils.isWin():
            self.patchToApply['2.49.4'] = [("glib-glib-2.49.4-20161114.diff", 1),
                                      ("fix-libname.diff", 1)]
            self.targetDigests['2.49.4'] = (['936e124d1d147226acd95def54cb1bea5d19dfc534532b85de6727fa68bc310f'], CraftHash.HashAlgorithm.SHA256)
        else:
            self.patchToApply['2.49.4'] = [("disable-docs-tests.diff", 1)]
            self.targetDigests['2.49.4'] = (['9e914f9d7ebb88f99f234a7633368a7c1133ea21b5cac9db2a33bc25f7a0e0d1'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.49.4"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/python3"] = None
        self.runtimeDependencies["libs/libffi"] = None
        self.runtimeDependencies["libs/pcre"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/gettext"] = None
        if not OsUtils.isWin():
            self.runtimeDependencies["libs/iconv"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None


class PackageCMake(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)
        self.toolset = "vs14"
        self.subinfo.options.configure.args = "/p:useenv=true"
        self.subinfo.options.configure.projectFile = \
            os.path.join(self.sourceDir(), "build", "win32", self.toolset, "glib.sln")


    def make(self):
        with utils.ScopedEnv({
            "LIB" : f"{os.environ['LIB']};{os.path.join(CraftStandardDirs.craftRoot() , 'lib')}",
            "INCLUDE" : f"{os.environ['INCLUDE']};{os.path.join(CraftStandardDirs.craftRoot() , 'include')}"}):
            return MSBuildPackageBase.make(self)

    def install(self):
        self.cleanImage()
        arch = "win32"
        if CraftCore.compiler.isX64():
            arch = "x64"
        utils.mergeTree(
            os.path.join(self.sourceDir(), "..", self.toolset, arch, "lib", "glib-2.0", "include"),
            os.path.join(self.sourceDir(), "..", self.toolset, arch, "include", "glib-2.0"))
        utils.copyDir(os.path.join(self.sourceDir(), "..", self.toolset, arch), self.imageDir(), False)
        return True


from Package.AutoToolsPackageBase import *


class PackageAutoTools(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)

    def configure(self):
        self.subinfo.options.configure.autoreconf = False
        root = self.shell.toNativePath(CraftCore.standardDirs.craftRoot())
        self.subinfo.options.configure.args += f"--enable-shared --disable-static --with-pcre=internal" \
                                               f" --with-python={self.shell.toNativePath(CraftCore.cache.findApplication('python3'))}"
        if OsUtils.isMac():
            # If we use --with-libiconv=gnu glib will try to find libiconv_open instead of iconv_open.
            # We could fix that by building libiconv, however it conflicts with the system libiconv.dylib.
            # Forcing glib to build against the native libiconv fixes this problem.
            self.subinfo.options.configure.args += " --with-libiconv=native"
        else:
            self.subinfo.options.configure.args += " --with-libiconv=gnu"
        self.subinfo.options.configure.cflags = "-Wno-format-nonliteral"

        if not CraftCore.cache.findApplication("pkg-config"):
            version = CraftPackageObject.get("libs/libffi").subinfo.buildTarget
            self.subinfo.options.configure.args += f" LIBFFI_LIBS=-lffi LIBFFI_CFLAGS='-I{root}/lib/libffi-{version}/include'"
        return super().configure()

    def install(self):
        if not AutoToolsBuildSystem.install(self):
            return False
        utils.copyFile(os.path.join(self.buildDir(), "glib", "glibconfig.h"),
                       os.path.join(self.imageDir(), "include", "glib-2.0", "glibconfig.h"), False)
        return True


if CraftCore.compiler.isGCCLike():
    class Package(PackageAutoTools):
        pass
else:
    class Package(PackageCMake):
        pass
