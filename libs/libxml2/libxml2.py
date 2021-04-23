import info
from Package.AutoToolsPackageBase import *
from Package.MakeFilePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['2.9.7', '2.9.10']:
            self.targets[ver] = f'https://gitlab.gnome.org/GNOME/libxml2/-/archive/v{ver}/libxml2-v{ver}.tar.bz2'
            self.targetInstSrc[ver] = f'libxml2-v{ver}'
            if not CraftCore.compiler.isGCCLike():
                self.targetInstSrc[ver] = os.path.join(self.targetInstSrc[ver], 'win32')
        self.targetDigests['2.9.7'] = (['7cedf270ac25f61b21070f387f608d6203db11923a6c67679cc861f35290ba18'], CraftHash.HashAlgorithm.SHA256)
        self.description = "XML C parser and toolkit (runtime and applications)"
        self.patchLevel["2.9.7"] = 1
        self.defaultTarget = '2.9.10'

    def setDependencies(self):
        # autoreconf requires pkg-config, but as pkg-config needs xml2 we disabled this dependency
        #self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/iconv"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None


class PackageMSVC(MakeFilePackageBase):
    def __init__(self, **args):
        MakeFilePackageBase.__init__(self)
        self.supportsNinja = False
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.make.supportsMultijob = False

    def configure(self):
        self.enterSourceDir()
        includedir = os.path.join(CraftCore.standardDirs.craftRoot(), 'include')
        libdir = os.path.join(CraftCore.standardDirs.craftRoot(), 'lib')
        prefixdir = self.imageDir()
        builddebug = "yes" if self.buildType() == "Debug" else "no"

        return utils.system([f"cscript.exe",
                            f".\configure.js",
                            f"compiler=msvc",
                            f"include={includedir}",
                            f"lib={libdir}",
                            f"prefix={prefixdir}",
                            f"debug={builddebug}",
                            f"zlib=yes",
                            f"iconv=yes"])

    def install(self):
        if not super().install():
            return False
        data = {"prefix" : CraftCore.standardDirs.craftRoot()}
        return utils.configureFile(self.packageDir() / "libxml-2.0-msvc.pc", self.imageDir() / "lib/pkgconfig/libxml-2.0.pc", data)


    def postInstall(self):
        target = self.imageDir() / "include/libxml"
        src = self.imageDir() / "include/libxml2//libxml"
         #otherwise it isn't picked up by libxslt
         # lets fix libxslt one day...
        return utils.copyDir(src, target, linkOnly=True)

class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --without-python "
        if self.subinfo.options.buildStatic:
            self.subinfo.options.configure.args += "--enable-static=yes --enable-shared=no "
        else:
            self.subinfo.options.configure.args += "--enable-static=no --enable-shared=yes "

    def postInstall(self):
        hardCoded = [Path(self.imageDir()) / "bin/xml2-config" ]
        return self.patchInstallPrefix(hardCoded, self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot())

if CraftCore.compiler.isGCCLike():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(PackageMSVC):
        def __init__(self):
            PackageMSVC.__init__(self)
