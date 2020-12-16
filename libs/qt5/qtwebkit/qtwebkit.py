# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def registerOptions(self):
        if CraftCore.compiler.isMinGW():
            self.options.dynamic.setDefault("buildType", "Release")

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.svnTargets["5.212"] = "https://code.qt.io/qt/qtwebkit.git|5.212"

        for ver in self.versionInfo.branches():
            if CraftVersion(ver) < "5.212":
                self.patchToApply[ver] = [("build-with-mysql.diff", 1),
                                          ("disable-icu-test.diff", 1)]

        self.patchToApply["5.212"] = [("qtwebkit-20181022.patch", 1),
                                      ("0001-gettickcount64-compatibility-xp.patch", 1),# https://raw.githubusercontent.com/Alexpux/MINGW-packages/2cfdf054df2c826d7c61237ee5ac2453b0f3964d/mingw-w64-qtwebkit/0001-gettickcount64-compatibility-xp.patch
                                      ("0004-msvc-bug-not-mingw.patch", 1),# https://raw.githubusercontent.com/Alexpux/MINGW-packages/2cfdf054df2c826d7c61237ee5ac2453b0f3964d/mingw-w64-qtwebkit/0004-msvc-bug-not-mingw.patch
                                      ("fix_mac.diff", 1) # https://raw.githubusercontent.com/OSGeo/homebrew-osgeo4mac/742b2afb6b85f9ba52d457ef63b1bb947f3dfcc0/Formula/qt5-webkit.rb
                                      ]
        self.patchToApply["dev"] = [("qtwebkit-20181022.patch", 1)]

        for ver in ["5.12", "5.15"]:
            self.svnTargets[ver] = self.svnTargets["5.212"]
            self.patchToApply[ver] = self.patchToApply["5.212"]

        # replace tarbals by git branches
        branchRegEx = re.compile(r"(\d\.\d+)\.\d+")
        for ver in self.versionInfo.tarballs():
            branch = branchRegEx.findall(ver)[0]
            del self.targets[ver]
            if ver in self.targetInstSrc:
                del self.targetInstSrc[ver]
            self.svnTargets[ver] = self.svnTargets[branch]
            self.patchToApply[ver] = self.patchToApply[branch]

        for ver in self.versionInfo.tags():
            branch = branchRegEx.findall(ver)[0][:-2]
            self.svnTargets[ver] = self.svnTargets[branch]
            self.patchToApply[ver] = self.patchToApply[branch]


    def setDependencies(self):
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/icu"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/webp"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtscript"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt5/qtwebchannel"] = None
        self.runtimeDependencies["libs/qt5/qtsensors"] = None
        self.runtimeDependencies["libs/qt5/qtlocation"] = None
        self.buildDependencies["dev-utils/ruby"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.buildDependencies["dev-utils/gperf"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["dev-utils/python2"] = None
        self.buildDependencies["dev-utils/nasm"] = None


from Package.Qt5CorePackageBase import *
from Package.CMakePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
        self.subinfo.options.configure.args = ""
        if OsUtils.isWin():
            self.subinfo.options.configure.args += """ "QT_CONFIG+=no-pkg-config" """
        if CraftCore.compiler.isMinGW():
            # things get too big
            # disable warnings as the project is unmaintained an the log files where getting too big
            self.subinfo.options.configure.args += """ "QMAKE_CXXFLAGS += -g0 -O3 -w" """
        elif CraftCore.compiler.isMSVC():
            # don't run out of heap during
            self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.configure.args += """ "WEBKIT_CONFIG-=geolocation" """

    def fetch(self):
        if os.path.exists(self.sourceDir()):
            utils.system(["git", "reset", "--hard"], cwd=self.sourceDir())
        return super().fetch()

class CMakePackage(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DPORT=Qt -DENABLE_API_TESTS=OFF -DENABLE_TOOLS=OFF " \
                                               "-DENABLE_NETSCAPE_PLUGIN_API=OFF -DUSE_GSTREAMER=OFF " \
                                               "-DUSE_QT_MULTIMEDIA=ON -DUSE_MEDIA_FOUNDATION=OFF -DUSE_LIBHYPHEN=OFF"
        if CraftCore.compiler.isMSVC():
            if not CraftCore.compiler.isMSVC2019():
                # TODO: find out why this is failing
                self.subinfo.options.configure.args += " -DENABLE_WEBKIT2=OFF"
            # TODO: why?
            self.subinfo.options.configure.args += """ -DCMAKE_CXX_FLAGS="-D_ENABLE_EXTENDED_ALIGNED_STORAGE" """
        elif CraftCore.compiler.isGCC():
            # don't spam warnings
            self.subinfo.options.configure.args += """ -DCMAKE_CXX_FLAGS="-w" """
            if CraftCore.compiler.isMinGW():
                self.subinfo.options.configure.args += """ -DCMAKE_CXX_FLAGS_RELEASE="-g0 -O3" """



class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        base = QtPackage
        if CraftVersion(CraftPackageObject.get("libs/qt5/qtbase").version) > "5.12":
            base = CMakePackage
        Qt5CoreSdkPackageBase.__init__(self, classA=base)
