import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/KDStateMachineEditor.git"
        self.svnTargets["1.2"] = "https://github.com/KDAB/KDStateMachineEditor.git|1.2"
        for ver in ["1.2.8"]:
            self.targets[ver] = f"https://github.com/KDAB/KDStateMachineEditor/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"kdstatemachineeditor-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"KDStateMachineEditor-{ver}"

        self.targetDigests["1.2.8"] = (["cbb3fcec7b5c6d16354aeb6c376c67a6ced32fce7bd937da0d4f591373acd374"], CraftHash.HashAlgorithm.SHA256)

        self.description = "The KDAB State Machine Editor Library is a framework that can be used to help develop full-featured State Machine Editing graphical user interfaces and tools."
        self.webpage = "https://www.kdab.com/"
        self.displayName = "KDStateMachineEditor"

        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtscxml"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DWITH_INTERNAL_GRAPHVIZ=OFF", "-DCMAKE_DISABLE_FIND_PACKAGE_Graphviz=ON"]
        self.subinfo.options.configure.args += ["-DBUILD_QT6=ON"]
