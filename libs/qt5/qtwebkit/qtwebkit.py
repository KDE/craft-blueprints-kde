# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in self.versionInfo.branches():
            self.patchToApply[ver] = [("build-with-mysql.diff", 1),
                                      ("disable-icu-test.diff", 1)]

        # there is not 5.10 branch, jet
        self.svnTargets["5.10"] = self.svnTargets["5.9"]

        # replace tarbals by git branches
        branchRegEx = re.compile("\d\.\d+\.\d+")
        for ver in self.versionInfo.tarballs():
            branch = branchRegEx.findall(ver)[0][:-2]
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
        self.runtimeDependencies["libs/sqlite"] = "default"
        self.runtimeDependencies["libs/icu"] = "default"
        self.runtimeDependencies["libs/libxslt"] = "default"
        self.runtimeDependencies["libs/libxml2"] = "default"
        self.runtimeDependencies["libs/zlib"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtscript"] = "default"
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = "default"
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebchannel"] = "default"
        self.runtimeDependencies["libs/qt5/qtsensors"] = "default"
        self.buildDependencies["dev-util/ruby"] = "default"
        self.buildDependencies["dev-util/winflexbison"] = "default"
        self.buildDependencies["gnuwin32/gperf"] = "default"


from Package.Qt5CorePackageBase import *


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
        self.subinfo.options.configure.args += """ "WEBKIT_CONFIG-=geolocation" """

    def fetch(self):
        print(self.sourceDir())
        if os.path.exists(self.sourceDir()):
            utils.system(["git", "reset", "--hard"], cwd=self.sourceDir())
        return Qt5CorePackageBase.fetch(self)

    def configure(self, configureDefines=""):
        with utils.ScopedEnv({"SQLITE3SRCDIR" : CraftPackageObject.get("libs/sqlite").instance.sourceDir()}):
            if not len(self.subinfo.buildTarget) == 3:  # 5.9
                with open(os.path.join(self.sourceDir(), ".qmake.conf"), "rt+") as conf:
                    text = conf.read()
                text = re.sub(re.compile(r"MODULE_VERSION = \d\.\d+\.\d+"), f"MODULE_VERSION = {self.subinfo.buildTarget}",
                              text)
                with open(os.path.join(self.sourceDir(), ".qmake.conf"), "wt+") as conf:
                    conf.write(text)
            return Qt5CorePackageBase.configure(self)

class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)
