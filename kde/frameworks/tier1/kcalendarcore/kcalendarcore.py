import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "The KDE calendar access library"

        self.patchToApply["5.247.0"] = [
            # Fix "no return statement in function returning non-void"
            # https://invent.kde.org/frameworks/kcalendarcore/-/merge_requests/164
            ("164.patch", 1),
            # Fix undefined reference to qMain(int, char**)
            ("0b0dcad3c5664f8499eaf9c9385a8120f178b451.patch", 1),
        ]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/libical"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
