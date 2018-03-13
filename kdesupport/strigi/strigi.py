import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/exiv2"] = "default"
        self.runtimeDependencies["libs/win_iconv"] = "default"
        self.runtimeDependencies["libs/libbzip2"] = "default"
        self.runtimeDependencies["libs/libxml2"] = "default"
        self.runtimeDependencies["libs/zlib"] = "default"

    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/strigi'
        for ver in ['0.7.6', '0.7.7', '0.7.8']:
            self.svnTargets[ver] = 'git://anongit.kde.org/strigi||v%s' % ver
        self.svnTargets['komobranch'] = 'branches/work/komo/strigi'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[i] = 'tags/kdesupport-for-4.3/kdesupport/strigi'
        for i in ['4.4.0', '4.4.1', '4.4.2', '4.4.3', '4.4.4', '4.4']:
            self.svnTargets[i] = 'tags/kdesupport-for-4.4/strigi'

        for ver in ['0.7.2', '0.7.5']:
            self.targets[ver] = 'http://www.vandenoever.info/software/strigi/strigi-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'strigi-' + ver
        self.patchToApply['0.7.2'] = ("strigi-0.7.2-20101223.diff", 1)
        self.patchToApply['0.7.5'] = [("strigi-0.7.5-20120225.diff", 1),
                                      ("add-intel-compiler-to-strigi-plugin-macros.diff", 1),
                                      ("do-not-use-fpic-also-on-intel-compiler.diff", 1),
                                      ("isblank-false-positive-intel-compiler.diff", 1),
                                      ("intel-cmake-adaptations.diff", 1)]
        self.patchToApply['0.7.8'] = [("strigi-0.7.8-20130906.diff", 1),
                                      ("add-intel-compiler-to-strigi-plugin-macros-0.7.8.diff", 1),
                                      ("do-not-use-fpic-also-on-intel-compiler-0.7.8.diff", 1),
                                      ("isblank-false-positive-intel-compiler.diff", 1),
                                      ("intel-cmake-adaptations-0.7.8.diff", 1)]
        self.targetDigests['0.7.2'] = 'b4c1472ef068536acf9c5c4c8f033a97f9c69f9f'

        self.description = "a desktop search engine and indexer"

        self.defaultTarget = '0.7.8'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args = ""
        self.subinfo.options.configure.args += "-DENABLE_CLUCENE=OFF "

        if self.buildTarget == "master":
            self.subinfo.options.configure.args = (
                " -DSTRIGI_SYNC_SUBMODULES=ON "
                " -DGIT_EXECUTABLE=%s "
                % os.path.join(self.rootdir, "dev-utils", "git", "bin",
                               "git.exe"))
