import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/rkward'
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.buildDependencies["extragear/rkward/rkward-translations"] = None
        self.runtimeDependencies["binary/r-base"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kdewebkit"] = "default"
        # not strictly runtimeDependencies, but should be included in the package
        self.runtimeDependencies["kde/applications/kate"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = "default"

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.translations = CraftPackageObject.get("extragear/rkward/rkward-translations").instance

        if OsUtils.isWin():
            if CraftCore.compiler.isX64():
                self.r_dir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "bin", "x64")
            else:
                self.r_dir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "bin", "i386")
            self.subinfo.options.configure.args = " -DR_EXECUTABLE=" + OsUtils.toUnixPath(os.path.join(self.r_dir, "R.exe"))
        # NOTE: On Mac, we'll let RKWard try to auto-detect R (installed with officilal installer, or MacPorts, or something else)
        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args = " -DR_EXECUTABLE=" + os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "R.framework", "Resources", "R")

        if self.subinfo.hasSvnTarget:
            self.subinfo.options.configure.args += f" -DTRANSLATION_SRC_DIR={OsUtils.toUnixPath(self.translations.sourceDir())}"

    def fetch(self):
        # Temporary workaround for failure to pull due to local modification of ver.R. Remove the line below around June, 2018.
        utils.deleteFile(os.path.join(self.checkoutDir(), "rkward", "rbackend", "rpackages", "rkward", "R", "ver.R"))

        if not CMakePackageBase.fetch(self):
            return False
        if self.subinfo.hasSvnTarget:
            return self.translations.fetch(noop=False)
        return True

    def install(self):
        ret = CMakePackageBase.install(self)
        if OsUtils.isWin():
            # Make installation movable, by providing rkward.ini with relative path to R
            rkward_ini = open(os.path.join(self.imageDir(), "bin", "rkward.ini"), "w")
            if CraftCore.compiler.isX64():
                rkward_ini.write("R executable=../lib/R/bin/x64/R.exe\n")
            else:
                rkward_ini.write("R executable=../lib/R/bin/i386/R.exe\n")
            rkward_ini.close()
        return ret

    def configure(self):
        if CraftCore.compiler.isMSVC():
            # Need to create a .lib-file for R.dll, first
            dump = subprocess.check_output(["dumpbin", "/exports", os.path.join(self.r_dir, "R.dll")]).decode(
                "latin1").splitlines()
            exports = []
            for line in dump:
                fields = line.split()
                if len(fields) != 4:
                    continue
                exports.append(fields[3])
            self.enterBuildDir()
            with open(os.path.join(self.buildDir(), "R.def"), "wt+") as deffile:
                deffile.write("EXPORTS\n")
                deffile.write("\n".join(exports))
            subprocess.call(["lib", "/def:R.def", "/out:R.lib", f"/machine:{CraftCore.compiler.architecture}"])
        return super().configure()

    def createPackage(self):
        self.defines["productname"] = "RKWard"
        self.defines["executable"] = "bin\\rkward.exe"
        self.defines["icon"] = os.path.join(self.sourceDir(), "rkward", "icons", "app-icon", "rkward.ico")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("data/hunspell-dictionaries")

        if OsUtils.isMac():
            return self.debugCreatePackageMac()
        else:
            return TypePackager.createPackage(self)

    # HACK: Remove me. This is a copy of MacDMGPackager, for the purpose of pinning down just what exactly causes
    #       the .dmg detach to hang on the binary factory.
    def debugCreatePackageMac(self):
        """ create a package """
        CraftCore.log.debug("packaging using the MacDMGPackager")

        self.internalCreatePackage()
        self.preArchive()

        self._setDefaults()


        archive = self.archiveDir()
        appPath = self.defines['apppath']
        if not appPath:
            apps = glob.glob(os.path.join(archive, f"**/{self.defines['appname']}.app"), recursive=True)
            if len(apps) != 1:
                CraftCore.log.error(f"Failed to detect *.app for {self}, please provide self.defines['apppath']")
                return False
            appPath = apps[0]
        appPath = os.path.join(archive, appPath)
        CraftCore.log.info(f"Packaging {appPath}")
        if os.path.exists(os.path.join(archive, "lib/plugins")):
            utils.mergeTree(os.path.join(archive, "lib/plugins"), os.path.join(appPath, "Contents/PlugIns/"))
        targetLibdir = os.path.join(appPath, "Contents/Frameworks/")
        if not os.path.exists(targetLibdir):
            os.makedirs(targetLibdir)
        if os.path.exists(os.path.join(archive, "lib")):
            utils.mergeTree(os.path.join(archive, "lib"), targetLibdir)
        if os.path.exists(os.path.join(archive, "share")):
            utils.mergeTree(os.path.join(archive, "share"), os.path.join(appPath, "Contents/Resources/"))
        utils.mergeTree(os.path.join(archive, "bin"), os.path.join(appPath, "Contents/MacOS/"))

        with utils.ScopedEnv({'DYLD_LIBRARY_PATH' : os.path.join(CraftStandardDirs.craftRoot(), "lib")}):
            if not utils.system(["dylibbundler",
                                 "--overwrite-files",
                                 "--bundle-deps",
                                 "--install-path", "@executable_path/../Frameworks",
                                 "--dest-dir", targetLibdir,
                                 "--fix-file", f"{appPath}/Contents/MacOS/{self.defines['appname']}"]):
                return False

            if not utils.system(["macdeployqt", appPath,  "-always-overwrite", "-verbose=1"]):
                return False

            utils.system(["ls", "-Rl", appPath], True);
            utils.system(["du", "-s", appPath], True);

            name = self.binaryArchiveName(fileType="", includeRevision=True)
            dmgDest = os.path.join(self.packageDestinationDir(), f"{name}.dmg")
            if os.path.exists(dmgDest):
                utils.deleteFile(dmgDest)
            if not utils.system(["create-dmg", "--volname", name, dmgDest, appPath]):
                return False

            CraftHash.createDigestFiles(dmgDest)

            return True
