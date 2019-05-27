import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.descriptions = "audio meta-data library"

    def setTargets(self):
        for ver in ["1.9.1", "1.11.1"]:
            self.targets[ver] = f"https://taglib.github.io/releases/taglib-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"taglib-{ver}"
            self.patchLevel[ver] = 1
        self.targetDigests["1.9.1"] = "4fa426c453297e62c1d1eff64a46e76ed8bebb45"
        self.targetDigests["1.11.1"] = (['b6d1a5a610aae6ff39d93de5efd0fdc787aa9e9dc1e7026fa4c961b26563526b'], CraftHash.HashAlgorithm.SHA256)
        self.description = "audio metadata library"
        self.webpage = "http://taglib.org/"
        self.defaultTarget = "1.11.1"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_SHARED_LIBS=ON"
        #        self.subinfo.options.configure.args += " -DBUILD_TESTS=ON"
        #        self.subinfo.options.configure.args += " -DBUILD_EXAMPLES=ON"
        #        self.subinfo.options.configure.args += " -DNO_ITUNES_HACKS=ON"
        self.subinfo.options.configure.args += " -DWITH_ASF=ON"
        self.subinfo.options.configure.args += " -DWITH_MP4=ON"


    def postInstall(self):
        hardCoded = []
        if not CraftCore.compiler.isWindows:
            hardCoded += [os.path.join(self.installDir(), x) for x in ["bin/taglib-config"]]
        return self.patchInstallPrefix(hardCoded, self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot())
