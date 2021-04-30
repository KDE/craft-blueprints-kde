import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.targets['1.0.0'] = 'https://download.kde.org/stable/kuserfeedback/kuserfeedback-1.0.0.tar.xz'
        self.targetDigests['1.0.0'] = (
            ['5a2f53ebb4b99a280757ca32bd9b686a7764a726e7e4d8bafee33acbb44b9db7'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc['1.0.0'] = 'kuserfeedback-1.0.0'

        if CraftCore.compiler.isWindows:
            self.defaultTarget = 'master'
        else:
            self.defaultTarget = '1.0.0'

        self.description = "KUserFeedback"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DENABLE_DOCS=OFF"]
