import info
import os
import shutil
from distutils.dir_util import copy_tree
from Package.MakeFilePackageBase import *
from shells import BashShell

nss_ver = "3.74"
nspr_ver = "4.32"

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.isMSVC() or CraftCore.compiler.isLinux

    def setTargets(self):
        self.description = "Network Security Services (NSS) is a set of libraries designed to support cross-platform development of security-enabled client and server applications."

        # always try to use latest nss with all security fixes
        ver = nss_ver
        self.targets[ver] = f"https://ftp.mozilla.org/pub/security/nss/releases/NSS_3_74_RTM/src/nss-{ver}-with-nspr-{nspr_ver}.tar.gz"
        self.targetInstSrc[ver] = f"nss-{ver}"
        self.targetDigests[ver] = (['27be1720f93270c7869b0013ed7f60ff5abd74f2612be0ad935a340599a4ec3c'], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.isMSVC():
            self.patchToApply[ver] = [("install-instead-of-nsinstall.diff", 1), ("cygwin-is-windows.diff", 1)]
        self.defaultTarget = ver

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["python-modules/gyp-next"] = None

class Package(MakeFilePackageBase):
    def __init__(self):
        MakeFilePackageBase.__init__(self)
        
    @property
    def makeProgram(self):
        if CraftCore.compiler.isWindows:
            return "make"
        else:
            return super().makeProgram
        
    def make(self):
        self.enterBuildDir()
        
        self._shell = BashShell()
        self._shell.environment["MAKE"] = self.makeProgram

        if CraftCore.compiler.isMSVC():
            #When you say --system-sqlite it just tries to find it in the path, that doesn't work for MSVC
            configgypi = self.sourceDir() / "nss/coreconf/config.gypi"
            with open(configgypi, "rt") as f:
                content = f.read()

            content = content.replace("'sqlite_libs%': ['-lsqlite3']", "'sqlite_libs%': ['" + str(CraftCore.standardDirs.craftRoot()) + "/lib/sqlite3.lib']")
        
            with open(configgypi, "wt") as f:
                f.write(content)

            clPath = CraftCore.cache.findApplication("cl")
            msvcPath = Path(clPath).parent
            while not os.path.isdir(msvcPath / 'VC' / 'Tools'):
                newPath = Path(msvcPath).parent
                if newPath == msvcPath:
                    print("Could not figure out which is your MSVC install path")
                    return False
                msvcPath = newPath
        
            msvcVersionPath = msvcPath
            while not Path(msvcVersionPath).name.isnumeric():
                newPath = Path(msvcVersionPath).parent
                if newPath == msvcVersionPath:
                    print("Could not figure out which is your MSVC version number")
                    return False
                msvcVersionPath = newPath
            
            self._shell.environment["GYP_MSVS_OVERRIDE_PATH"] = str(msvcPath)
            self._shell.environment["GYP_MSVS_VERSION"] = Path(msvcVersionPath).name
        
        build = Arguments([self.sourceDir() / "nss/build.sh"])
        return self._shell.execute(self.buildDir(), build, ["--disable-tests", "--opt", "--system-sqlite", "-Dsign_libs=0"])
    
    def install(self):
        if not BuildSystemBase.install(self):
            return False

        copy_tree(self.sourceDir() / 'dist/Release', str(self.installDir()))
        copy_tree(self.sourceDir() / 'dist/public', str(self.installDir() / 'include'))
        
        #NSS has a .pc.in file but doesn't do anything with it
        nsspcSource = os.path.join(self.sourceDir(), "nss/pkg/pkg-config/nss.pc.in")
        nsspcDest = os.path.join(self.installDir(), "lib/pkgconfig/nss.pc")
        shutil.copyfile(nsspcSource, nsspcDest)
        
        with open(nsspcDest, "rt") as f:
            content = f.read()

        content = content.replace("%libdir%", "${prefix}/lib")
        content = content.replace("%prefix%", str(CraftCore.standardDirs.craftRoot()).replace('\\', '/'))
        content = content.replace("%exec_prefix%", "${prefix}")
        content = content.replace("%includedir%", "${prefix}/include/nss")
        content = content.replace("%NSPR_VERSION%", nspr_ver)
        content = content.replace("%NSS_VERSION%", nss_ver)

        with open(nsspcDest, "wt") as f:
            f.write(content)
        
        return True

    def postInstall(self):
        BuildSystemBase.patchInstallPrefix(self, [(self.installDir() / 'lib/pkgconfig/nspr.pc')], [os.path.dirname(self.installDir()) + '/work/nss-3.74/dist/Release'])
        if CraftCore.compiler.isMSVC():
        
            # The nspr libs are created as libnspr4.lib so we need to adapt the pc file
            nsprpc = self.installDir() / 'lib/pkgconfig/nspr.pc'
            with open(nsprpc, "rt") as f:
                content = f.read()

            content = content.replace('-l', '-llib')
        
            with open(nsprpc, "wt") as f:
                f.write(content)
        
            # Fix the .lib files names (i.e. foo.dll.lib instead of foo.lib)
            for f in os.listdir(self.installDir() / 'lib'):
                full_path = os.path.join(self.installDir() / 'lib', f)
                if os.path.isfile(full_path):
                    if not full_path.endswith(".dll.lib"):
                        continue
                
                    new_name = full_path.replace(".dll.lib", ".lib")
                    os.rename(full_path, new_name)
        
            # Fix the .dll file sbeing in lib instead of bin
            for f in os.listdir(self.installDir() / 'lib'):
                full_path = os.path.join(self.installDir() / 'lib', f)
                if os.path.isfile(full_path):
                    if not full_path.endswith(".dll"):
                        continue
                
                    new_name = full_path.replace("\\lib\\", "\\bin\\")
                    os.rename(full_path, new_name)
                
        return True
