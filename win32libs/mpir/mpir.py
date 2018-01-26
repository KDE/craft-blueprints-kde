# copyright:
# Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>

import info
import re


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['3.0.0']:
            self.targets[ver] = 'http://www.mpir.org/mpir-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = "mpir-" + ver
        self.targetDigests['3.0.0'] = (['52f63459cf3f9478859de29e00357f004050ead70b45913f2c2269d9708675bb'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc['3.0.0'] = 'mpir-3.0.0'

        self.description = "Library for arbitrary precision integer arithmetic derived from version 4.2.1 of gmp"
        self.defaultTarget = '3.0.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"
        else:
            self.buildDependencies["dev-util/yasm"] = "default"


from Package.AutoToolsPackageBase import *
from Package.MSBuildPackageBase import *


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        abi = "ABI=64"
        if CraftCore.compiler.isX86():
            abi = "ABI=32"
            self.platform = ""
        self.subinfo.options.configure.args = "--enable-shared --disable-static --enable-gmpcompat --enable-cxx " + abi


class PackageMSVC(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)
        if CraftCore.compiler.getInternalVersion() == 14:
            self.mpirBuildDir = os.path.join(self.sourceDir(), "build.vc14")
        else:
            self.mpirBuildDir = os.path.join(self.sourceDir(), "build.vc15")

        if CraftCore.compiler.isX86():
            self.subinfo.options.configure.args = " /p:Platform=win32"

        self.subinfo.options.configure.args = self.subinfo.options.configure.args + " /p:WindowsTargetPlatformVersion=" + os.getenv('WINDOWSSDKVERSION')[:-1]
        self.subinfo.options.configure.projectFile = os.path.join(self.mpirBuildDir, "mpir.sln")
        self.msbuildTargets = ["dll_mpir_gc", "lib_mpir_cxx"]

    def adjustProjectFile(self):
        path = self.subinfo.options.configure.projectFile
        targets = self.msbuildTargets
        #open project file to add default build targets
        f = open(str(path), "r+")
        projectFileContents = f.readlines()
        IDS = [[] for _ in range(len(targets))]
        for i in range(len(projectFileContents)):
            for j in range(len(targets)):
                #fetch target ids, to add them latter for building
                m = re.search(targets[j] + "[^{]*{(?P<ID>[^{}]*)", projectFileContents[i])
                if m is not None:
                    IDS[j] = m.group('ID')

            if "ProjectConfigurationPlatforms" in projectFileContents[i]:
                for ID in IDS:
                    projectFileContents.insert(i + 1,
                                            "{"+ ID + "}.Release|Win32.Build.0 = Release|Win32\n")  #3.0.0 version needs those lines, otherwise it won't compile anything
                    projectFileContents.insert(i + 1,
                                            "{"+ ID + "}.Release|x64.Build.0 = Release|x64\n")
                break

        f.seek(0)
        f.write(''.join(projectFileContents))
        f.close()

    def make(self):
        utils.putenv('YASMPATH', os.path.join(self.rootdir, 'dev-utils', 'bin'))
        self.adjustProjectFile()
        return MSBuildPackageBase.make(self)

    def install(self):
        if not MSBuildPackageBase.install(self, buildDirs=[os.path.join(self.mpirBuildDir, target) for target in
                                                           self.msbuildTargets]):
            return False
        # a dirty workaround the fact that FindGMP.cmake will only look for gmp.lib
        utils.copyFile(os.path.join(self.installDir(), "lib", "mpir.lib"),
                       os.path.join(self.installDir(), "lib", "gmp.lib"))
        return True


if CraftCore.compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(PackageMSVC):
        def __init__(self):
            PackageMSVC.__init__(self)
