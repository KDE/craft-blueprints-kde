import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/KDStateMachineEditor.git"
        self.svnTargets["1.2"] = "https://github.com/KDAB/KDStateMachineEditor.git|1.2"
        for ver in ["1.2.0", "1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.7"]:
            self.targets[ver] = f"https://github.com/KDAB/KDStateMachineEditor/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"kdstatemachineeditor-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"KDStateMachineEditor-{ver}"

        self.patchToApply["1.2.3"] = [("kdstatemachineeditor-1.2.3-20180618.diff", 1)]
        self.patchToApply["1.2.7"] = [("46a32712a328aa7ec461713534f0fe27be563bcf.patch", 1)]

        self.targetDigests['1.2.0'] = (['c43b864e60c025b1d4eb03f0b3073e00ebb642aecf10dd8b5b29f4a2da2b1c07'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.2.1'] = (['a97597aa3c67356bba7f6c1503018ddf3369ada5534f33129adab29a53f6ed11'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.2.2'] = (['d616acc9cea6dc6ad4731d3a2fe12e19cf9ce6d3a59b4cd685cf719bd1b82637'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.2.4'] = (['3c71d564b424b498c0f5999d5133db394ae000e774734d19e2640b28908f07b1'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.2.7'] = (['8b2ae1775201b1f97cd332f5aec23ed5bb943531c6583690c4130ff517f75b2c'], CraftHash.HashAlgorithm.SHA256)

        self.description = "The KDAB State Machine Editor Library is a framework that can be used to help develop full-featured State Machine Editing graphical user interfaces and tools."
        self.webpage = "https://www.kdab.com/"
        self.displayName = "KDStateMachineEditor"
        self.defaultTarget = "1.2.7"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DWITH_INTERNAL_GRAPHVIZ=OFF"


