<!--
    SPDX-License-Identifier: CC0-1.0
    SPDX-FileCopyrightText: 2022 Harald Sitter <sitter@kde.org>
-->

# Branches

- `master`: update to existing stuff goes here (only supports Qt6)
- `dev`: ... unless it has chance of breaking everything and the kitchen sink then it goes here. Also, new caches go here. Only supports Qt6.
- `qt5-lts`: branch to continue support for Qt5, no major updates are expected here

# Test the build of a package / blueprint

You can test the build of a package as follows:
* Go to Build -> Pipelines
* Click the "New pipeline" button
* Select the branch you want to run the pipeline on, e.g. your MR branch
* Enter the name of the package you want to build in the Inputs section
* Click the "New pipeline" button
* Trigger any of the build-package-* jobs that you want to run for the package
