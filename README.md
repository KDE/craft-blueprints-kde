<!--
    SPDX-License-Identifier: CC0-1.0
    SPDX-FileCopyrightText: 2022 Harald Sitter <sitter@kde.org>
    SPDX-FileCopyrightText: 2026 Ingo Klöcker <kloecker@kde.org>
-->

# Branches

- `master`: update to existing stuff goes here (only supports Qt6)
- `dev`: ... unless it has chance of breaking everything and the kitchen sink then it goes here. Also, new caches go here. Only supports Qt6.
- `qt5-lts`: branch to continue support for Qt5, no major updates are expected here

# Test the build of a package / blueprint

All MR pipelines have several `build-package-*` jobs which you can use to test the build of a package for the different platforms supported by Craft.
The jobs need to know which package to build. There are several ways to achieve this.

## Automatic package selection

If the title of your MR (or the title of the latest commit in the MR) starts with `PACKAGE_NAME: ` or with `[PACKAGE_NAME] ` then the `build-package-*` jobs
will run the jobs for package `PACKAGE_NAME`, i.e. you can simply click the ▶️ button of the build job you want to run. (The prefix `Draft:` of draft MRs will be ignored.)

## Manual specification of package for all jobs of a pipeline

1. Open the Pipelines tab of your MR.
2. Click the arrow next to *Run pipeline* and select *Run pipeline with modified values*.
3. Enter the name of the package you want to build as value for the *package* input.
4. Click *New pipeline*.
5. Click the new pipeline.
6. Now you can start the builds for the package you specified by clicking the ▶️ button of the corresponding jobs.

## Manual specification of package for a single job

1. Open a pipeline of your MR.
2. Click the name of the build job you want to run.
3. If the job wasn't run yet then you'll see a form where you can enter variables for the job. Otherwise, you have to click the arrow next to the *Retry* button and select
*Retry job with modified values*.
4. Expand the *Variables* section.
5. Enter `CRAFT_PACKAGE` as key and the name of the package you want to build as value.
6. Click *Run job* (or *Run job again*).
