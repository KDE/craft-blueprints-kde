import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Libkdepim library"

    def registerOptions(self):
        # FIXME: Xapian is currently broken on Windows, provides wrong CMake config files(?). Thus akonadi-search does not build.
        #   Error:
        #     ninja: error: 'Z:/CraftRoot/lib/libxapian.lib', needed by 'bin/KF5AkonadiSearchXapian.dll', missing and no known rule to make it
        #     Action: compile for kde/pim/akonadi-search:19.12.3 FAILED
        self.options.dynamic.registerOption("useDesignerPlugin", True)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]

        if not self.subinfo.options.dynamic.useDesignerPlugin:
            self.subinfo.options.configure.args += ["-DBUILD_DESIGNERPLUGIN=OFF"]
