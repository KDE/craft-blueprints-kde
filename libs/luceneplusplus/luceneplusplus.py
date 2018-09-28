import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/boost/boost-thread"] = None
        self.runtimeDependencies["libs/boost/boost-system"] = None
        self.runtimeDependencies["libs/boost/boost-regex"] = None
        self.runtimeDependencies["libs/boost/boost-iostreams"] = None
        self.runtimeDependencies["libs/boost/boost-date-time"] = None
        self.runtimeDependencies["libs/boost/boost-filesystem"] = None
        self.runtimeDependencies["libs/boost/boost-atomic"] = None

    def setTargets(self):
        for ver in []:
            self.targets[ver] = "https://github.com/luceneplusplus/LucenePlusPlus/archive/rel_%s.tar.gz" % ver
            self.archiveNames[ver] = "luceneplusplus-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "LucenePlusPlus-rel_%s" % ver
        self.patchToApply["master"] = ("luceneplusplus-20150916.patch", 1)

        self.svnTargets["master"] = "https://github.com/luceneplusplus/LucenePlusPlus.git"

        self.description = "Lucene++ is an up to date C++ port of the popular Java Lucene library, a high-performance, full-featured text search engine."
        self.webpage = "https://github.com/luceneplusplus/LucenePlusPlus/"
        self.defaultTarget = "master"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DENABLE_TEST=OFF -DENABLE_DEMO=OFF"
