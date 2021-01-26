import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://invent.kde.org/libraries/kquickimageeditor.git'

        for ver in ['0.1.3']:
            self.targets[ver] = 'https://download.kde.org/stable/kquickimageeditor/0.1/kquickimageeditor-%s.tar.xz' % ver
            self.archiveNames[ver] = 'kquickimageeditor-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'kquickimageeditor-%s' % ver

        self.description = "A set of QtQuick components providing basic image editing capabilities"
        self.defaultTarget = '0.1.3'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
