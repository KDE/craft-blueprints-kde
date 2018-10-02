import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None
            self.runtimeDependencies["libs/lcms"] = None
            self.runtimeDependencies["libs/lcms2"] = None
            self.runtimeDependencies["libs/freetype"] = None
            self.runtimeDependencies["libs/libjpeg-turbo"] = None
            self.runtimeDependencies["libs/libpng"] = None
            self.runtimeDependencies["libs/tiff"] = None

    def setTargets(self):
        self.svnTargets['master'] = 'git://git.ghostscript.com/ghostpdl.git'
        for ver in ['9.19', '9.21']:
            self.targets[
                ver] = "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs%s/ghostscript-%s.tar.gz" % (
            ver.replace(".", ""), ver)
            self.targetInstSrc[ver] = 'ghostscript-%s' % ver
            self.targetDigestUrls[ver] = ([
                                              "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs%s/SHA1SUMS" % ver.replace(
                                                  ".", "")], CraftHash.HashAlgorithm.SHA1)

        if CraftCore.compiler.isMinGW():
            self.patchToApply['9.19'] = [
                # ("mingw-build.patch", 1),# origin: https://github.com/Alexpux/MINGW-packages/tree/master/mingw-w64-ghostscript
                # ("ghostscript-sys-zlib.patch", 1),# origin: https://github.com/Alexpux/MINGW-packages/tree/master/mingw-w64-ghostscript
                ("ghostscript-9.18-20151217.diff", 1),
                ("ghostscript-exports-fix.diff", 1),
                ("libspectre.patch", 1)
                # origin: https://github.com/Alexpux/MINGW-packages/tree/master/mingw-w64-ghostscript
            ]
        else:
            self.patchToApply['9.19'] = [("ghostscript-exports-fix.diff", 1)]
        self.patchLevel['9.19'] = 1
        self.defaultTarget = '9.19'


from Package.CMakePackageBase import *


class PackageMSVC(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def configure(self):
        return True

    def make(self):
        self.enterSourceDir()

        extraArgs = []
        if CraftCore.compiler.isX64():
            extraArgs.append("WIN64=")
        # because ghostscript doesn't know about msvc2015, it guesses wrong on this. But,
        # because of where we are, rc /should/ be in the path, so we'll just use that.
        if CraftCore.compiler.isMSVC():
            extraArgs.append("RCOMP=rc.exe")
        if CraftCore.compiler.isMSVC2017():
            # work-around: https://bugs.ghostscript.com/show_bug.cgi?id=698426
            vcInstallDir = os.environ['VCINSTALLDIR'].rstrip('\\')
            extraArgs+= ["MSVC_VERSION=15", f"DEVSTUDIO=\"{vcInstallDir}\""]
        utils.system(["nmake", "-f",  "psi\\msvc.mak"] + extraArgs)
        return True

    def install(self):
        src = self.sourceDir()
        dst = self.imageDir()

        if not os.path.isdir(dst):
            os.mkdir(dst)
        if not os.path.isdir(os.path.join(dst, "bin")):
            os.mkdir(os.path.join(dst, "bin"))
        if not os.path.isdir(os.path.join(dst, "lib")):
            os.mkdir(os.path.join(dst, "lib"))
        if not os.path.isdir(os.path.join(dst, "include")):
            os.mkdir(os.path.join(dst, "include"))
        if not os.path.isdir(os.path.join(dst, "include", "ghostscript")):
            os.mkdir(os.path.join(dst, "include", "ghostscript"))

        if CraftCore.compiler.isX64():
            _bit = "64"
        else:
            _bit = "32"
        utils.copyFile(os.path.join(src, "bin", "gsdll%s.dll" % _bit), os.path.join(dst, "bin"), False)
        utils.copyFile(os.path.join(src, "bin", "gsdll%s.lib" % _bit), os.path.join(dst, "lib"), False)
        utils.copyFile(os.path.join(src, "bin", "gswin%s.exe" % _bit), os.path.join(dst, "bin"), False)
        utils.copyFile(os.path.join(src, "bin", "gswin%sc.exe" % _bit), os.path.join(dst, "bin"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "psi", "iapi.h"),
                       os.path.join(self.imageDir(), "include", "ghostscript", "iapi.h"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "psi", "ierrors.h"),
                       os.path.join(self.imageDir(), "include", "ghostscript", "ierrors.h"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "devices", "gdevdsp.h"),
                       os.path.join(self.imageDir(), "include", "ghostscript", "gdevdsp.h"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "base", "gserrors.h"),
                       os.path.join(self.imageDir(), "include", "ghostscript", "gserrors.h"), False)
        utils.copyDir(os.path.join(self.sourceDir(), "lib"), os.path.join(self.imageDir(), "lib"), False)

        return True


from Package.AutoToolsPackageBase import *


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.package.packageName = 'ghostscript'
        self.subinfo.options.package.packSources = False
        self.subinfo.options.configure.defiens = " --with-drivers=ALL --disable-cups --with-system-libtiff --with-jbig2dec --enable-openjpeg --enable-fontconfig --enable-freetype --disable-contrib --without-x"
        self.subinfo.options.make.arg = "so"
        self.subinfo.options.useShadowBuild = False

    def unpack(self):
        if not AutoToolsPackageBase.unpack(self):
            return False
        for d in ["freetype", "jpeg", "libpng", "lcms", "lcms2", "tiff"]:  # , "zlib"]: #openjpeg]
            utils.rmtree(os.path.join(self.sourceDir(), d))
        return True

    def make(self, dummyBuildType=None):
        # Normal build first
        if not super().make(dummyBuildType):
            return False

        # Now build the library
        buildDirectory = self.buildDir()
        if not self.subinfo.options.useShadowBuild:
            buildDirectory = self.sourceDir()

        if not self.shell.execute(self.sourceDir(), self.makeProgram, "so"):
            print("while Make'ing. cmd: %s" % command)
            return False

        return True

    def install(self):
        if not AutoToolsPackageBase.cleanImage(self):
            return False
        os.makedirs(os.path.join(self.imageDir(), "bin"))
        os.makedirs(os.path.join(self.imageDir(), "lib"))
        os.makedirs(os.path.join(self.imageDir(), "include", "ghostscript"))
        utils.copyDir(os.path.join(self.sourceDir(), "sobin"), os.path.join(self.imageDir(), "bin"), False)
        utils.moveFile(os.path.join(self.imageDir(), "bin", "libgs.dll.a"),
                       os.path.join(self.imageDir(), "lib", "libgs.dll.a"))
        utils.copyFile(os.path.join(self.sourceDir(), "psi", "iapi.h"),
                       os.path.join(self.imageDir(), "include", "ghostscript", "iapi.h"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "psi", "ierrors.h"),
                       os.path.join(self.imageDir(), "include", "ghostscript", "ierrors.h"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "devices", "gdevdsp.h"),
                       os.path.join(self.imageDir(), "include", "ghostscript", "gdevdsp.h"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "base", "gserrors.h"),
                       os.path.join(self.imageDir(), "include", "ghostscript", "gserrors.h"), False)
        utils.copyDir(os.path.join(self.sourceDir(), "lib"), os.path.join(self.imageDir(), "lib"), False)
        return True


if CraftCore.compiler.isGCCLike():
    class Package(PackageMSys):
        pass
else:
    class Package(PackageMSVC):
        pass
