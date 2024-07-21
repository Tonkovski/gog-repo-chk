# gogrepochk
(Wip)

This self-use purpose widget checks for GOG's offline resources updates.

Nowadays, while most GOG users prefer GOG GALAXY for software updates, a few old-school mates still shares the "to have is to own" belief, by maintaining a separated offline resource repo. On the other hand, manually checking for offline packages updates can be painful, which gives inspiration to this little project.

## GGGSS - How to manage a GOG offline repo

GGGSS aka General GOG-Game Saving Strategy aims to maintain an easy-to-read offline repo both for human and autoscripts, this is what a GGGSS-compatible repo looks like:

```tree
├── title_slug_1`102394264
│   ├── v1.2.355`win
│   │   ├── setup_title_slug_1_v1.2.355.exe
│   │   └── setup_title_slug_1_v1.2.355-1.bin
│   ├── v1.1`win
│   │   ├── setup_title_slug_1_v1.1.exe
│   │   └── setup_title_slug_1_v1.1-1.bin
│   ├── `bonus
│   │   ├── avatar.zip
│   │   └── artbook.pdf
│   ├── `dlc
│   │   ├── dlc_slug_1`109834537
│   │   │   ├── v1.3`win
│   │   │   │   └── setup_dlc_slug_1_v1.3.exe
│   │   │   └── `bonus
│   │   │       └── official_toolkit_setup.exe
│   │   └── dlc_slug_2`102947857
│   │       └── `bonus
│   │           └── original_soundtrack.zip
│   └── `misc
│       ├── Patch_v1.2_v1.3.exe
│       ├── Unofficial_bug_patch.exe
│       └── Mod_mapkit.zip
└── `title_slug_2`100936485
    ├── gog-1`win
    │   └── setup_title_slug_2_gog-1.exe
    ├── _`linux
    │   └── title_slug_2_gog_1.sh
    └── v3_1`osx
        └── title_slug_2_gog_1_.pkg
```

Human words: 

* Keep every title under a unique folder named by ``` [Slug]`[Product ID] ```, which can be acquired through GOGDB site.
  * Keep **installer related files** under ```[Version]`[Platform]``` folder, use multiple folders for different combinations of version & platform.
    * If the version string contains forbids chars `\/:*?"<>|`, replace them with `_`.
    * If the version displays as `N/A` in GOGDB website (which means a `null` in json data), leave the version string as `_`.
  * Keep **bonus contents** under ``` `bonus ``` folder, *gogrepochk* doesn't check for any bonus content updates, for these contents usually remain untouched since release.
  * Keep **DLCs** under ``` `dlc ``` folder, each DLC should be treated same as a title under its own ``` [Slug]`[Product ID] ```-named folder, with its own **installer related files** and/or **bonus contents**.
  * Keep other things under ``` `misc ``` folder, no matter it is an official patch, a mod file, or a cheatsheet.
* Keep no empty folders, e.g. leave no ``` `dlc ``` folder for titles without DLCs owned.
* Bundles and Game packs are not supported, the repo only serves for games and DLCs
* Adding a ``` ` ``` before the title/DLC folder to manually skip checking for update, useful when the title is already confirmed out-dated, or a DLC is undocumented in GOGDB.
