import info
import utils
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        if CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.NoPlatform

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        if not CraftCore.compiler.isMSVC():
            self.buildDependencies["dev-utils/msys"] = None
            self.runtimeDependencies["libs/lcms2"] = None
            self.runtimeDependencies["libs/freetype"] = None
            self.runtimeDependencies["libs/openjpeg"] = None
            self.runtimeDependencies["libs/libpng"] = None
            self.runtimeDependencies["libs/tiff"] = None
            self.runtimeDependencies["libs/fontconfig"] = None

    def setTargets(self):
        self.svnTargets["master"] = "git://git.ghostscript.com/ghostpdl.git"
        for ver in ["10.01.2"]:
            ver2 = ver.replace(".", "")
            self.targets[ver] = f"https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs{ver2}/ghostscript-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"ghostscript-{ver}"
            self.targetDigestUrls[ver] = (
                [f"https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs{ver2}/SHA512SUMS"],
                CraftHash.HashAlgorithm.SHA512,
            )

        self.defaultTarget = "10.01.2"


class PackageMSVC(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def configure(self):
        return True

    def make(self):
        self.enterSourceDir()

        extraArgs = []
        if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
            extraArgs.append("WIN64=")
        # because ghostscript doesn't know about msvc2015, it guesses wrong on this. But,
        # because of where we are, rc /should/ be in the path, so we'll just use that.
        if CraftCore.compiler.isMSVC():
            extraArgs.append("RCOMP=rc.exe")
        utils.system(["nmake", "-f", "psi\\msvc.mak"] + extraArgs)
        return True

    def install(self):
        src = self.sourceDir()
        dst = self.imageDir()

        _bit = CraftCore.compiler.architecture.bits
        return (
            utils.createDir(dst / "bin")
            and utils.createDir(dst / "lib")
            and utils.createDir(dst / "include")
            and utils.createDir(dst / "include/ghostscript")
            and utils.copyFile(src / f"bin/gsdll{_bit}.dll", dst / "bin", False)
            and utils.copyFile(src / f"bin/gsdll{_bit}.lib", dst / "lib", False)
            and utils.copyFile(src / f"bin/gswin{_bit}.exe", dst / "bin", False)
            and utils.copyFile(src / f"bin/gswin{_bit}c.exe", dst / "bin", False)
            and utils.copyFile(self.sourceDir() / "psi/iapi.h", self.imageDir() / "include/ghostscript/iapi.h", False)
            and utils.copyFile(self.sourceDir() / "psi/ierrors.h", self.imageDir() / "include/ghostscript/ierrors.h", False)
            and utils.copyFile(self.sourceDir() / "devices/gdevdsp.h", self.imageDir() / "include/ghostscript/gdevdsp.h", False)
            and utils.copyFile(self.sourceDir() / "base/gserrors.h", self.imageDir() / "include/ghostscript/gserrors.h", False)
            and utils.copyDir(self.sourceDir() / "lib", self.imageDir() / "lib", False)
        )


class PackageMSys(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.configure.args += [
            "--with-drivers=ALL",
            "--disable-cups",
            "--without-x",
            "--disable-contrib",
            "--enable-freetype",
            "--with-jbig2dec",
            "--enable-openjpeg",
            "--disable-gtk",
            "--enable-fontconfig",
        ]
        if not CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["--with-system-libtiff"]
        else:
            self.subinfo.options.configure.args += ["--with-libtiff"]
        self.subinfo.options.make.args += ["so", "all"]
        self.subinfo.options.install.args += ["install-so", "install"]
        self.subinfo.options.useShadowBuild = False

    def unpack(self):
        if not super().unpack():
            return False
        forceSystemLibs = ["freetype", "jpeg", "libpng", "lcms", "lcms2", "zlib"]
        if not CraftCore.compiler.isMacOS:
            forceSystemLibs += ["tiff", "openjpeg"]
        for d in forceSystemLibs:
            utils.rmtree(self.sourceDir() / d)
        return True

    def make(self):
        env = {}
        if CraftCore.compiler.isLinux:
            env["LD_LIBRARY_PATH"] = CraftCore.standardDirs.craftRoot() / "lib"
        with utils.ScopedEnv(env):
            return super().make()

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isLinux:
            # only the symlinks get installed...
            return utils.copyFile(f"{self.buildDir()}/sobin/libgs.so.10", f"{self.installDir()}/lib/libgs.so.10")

        return True


if CraftCore.compiler.isGCCLike():

    class Package(PackageMSys):
        pass

else:

    class Package(PackageMSVC):
        pass
