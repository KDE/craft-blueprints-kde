# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.patchToApply["17.04.0"] = [("akonadi-17.04.0-20170530.diff", 1)]
        self.patchToApply["17.04.1"] = [("akonadi-17.04.0-20170530.diff", 1)]
        self.patchToApply["17.04.2"] = [("akonadi-17.04.0-20170530.diff", 1)]
        self.patchToApply["17.08.3"] = [("akonadi-17.08.3-20171204.diff", 1), #workaround for locked log crash https://phabricator.kde.org/T7538#119826
                                        ("akonadi-17.08.3-20171204-1.diff", 1),
                                        ("akonadi-17.08.3-20171204-2.diff", 1)]
        self.patchToApply["17.12.0"] = [("akonadi-17.12.0-20171220.diff", 1),
                                        ("0001-Win-Create-local-socket-named-pipes-based-on-the-ins.patch", 1)]
        self.patchToApply["18.12.2"] = [("akonadi-18.12.2-macos.diff", 1),
                                        ("akonadi-18.12.2-errorstring.diff", 1)]
        self.patchLevel["18.12.2"] = 2
        self.patchToApply["18.12.3"] = [("akonadi-18.12.2-macos.diff", 1),
                                        ("akonadi-18.12.2-errorstring.diff", 1)]
        self.patchLevel["18.12.3"] = 2
        self.patchToApply["19.04.1"] = [("akonadi-19.04-macos.diff", 1),
                                        ("akonadi-18.12.2-errorstring.diff", 1),
                                        ("akonadi-19.04.1-shorter-sockets.diff", 1)] # macos temp path are so long that if a user has a long nick it bypass the limited socket file path length of 104chars.
        self.patchLevel["19.04.1"] = 3
        self.patchToApply["19.04.2"] = [("akonadi-19.04-macos.diff", 1),
                                        ("akonadi-18.12.2-errorstring.diff", 1),
                                        ("akonadi-19.04.1-shorter-sockets.diff", 1)] # macos temp path are so long that if a user has a long nick it bypass the limited socket file path length of 104chars.

        self.description = "A storage service for PIM data and meta data"

    def registerOptions(self):
        self.options.dynamic.registerOption("useDesignerPlugin", True)

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/boost/boost-graph"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/shared-mime-info"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        if self.options.dynamic.useDesignerPlugin:
            self.runtimeDependencies["kde/frameworks/tier3/kdesignerplugin"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DDATABASE_BACKEND=SQLITE -DAKONADI_RUN_MYSQL_ISOLATED_TESTS=OFF -DBUILD_TESTING=OFF "

        if not self.subinfo.options.dynamic.useDesignerPlugin:
            self.subinfo.options.configure.args += "-DBUILD_DESIGNERPLUGIN=OFF "
