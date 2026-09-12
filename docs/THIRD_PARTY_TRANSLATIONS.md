# Third-party translation sources

## Maiden's MerryMaking

`overrides/kubejs/assets/maidensmerrymaking/lang/ru_ru.json` is adapted from
[MPLOCmods v40.1](https://modrinth.com/resourcepack/mploc-mods/version/EBQQC2KB),
published by the MPLOCmods project under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

Changes made for Astropolis RU:

- retained only keys present in the Maiden's MerryMaking version bundled with Astropolis 2.2;
- added translations for 24 version-specific keys absent from MPLOCmods;
- the adapted Russian language file remains available under CC BY-SA 4.0.

The same pinned MPLOCmods v40.1 archive is also used to fill exact missing keys
for other bundled mods. Existing translations and hand-reviewed Astropolis RU
overrides always take precedence. Imports are reproducible with
`tools/import_mploc_translations.py`; placeholder-incompatible strings are skipped.

## Official mod repositories

Missing keys are supplemented from the mods' own newer Russian language files.
Only exact keys or unambiguous exact English-string matches are imported. The
pinned revisions and source paths are recorded in
`tools/import_upstream_localizations.py`.

- [FancyMenu](https://github.com/Keksuccino/FancyMenu)
- [Quark](https://github.com/VazkiiMods/Quark)
- [Applied Energistics 2](https://github.com/AppliedEnergistics/Applied-Energistics-2)
- [FTB Chunks](https://github.com/FTBTeam/FTB-Chunks)
- [FTB Quests](https://github.com/FTBTeam/FTB-Quests)
- [Jade](https://github.com/Snownee/Jade)
- [Immersive Engineering](https://github.com/BluSunrize/ImmersiveEngineering)
- [Supplementaries](https://github.com/MehVahdJukaar/Supplementaries)
- [Sophisticated Core](https://github.com/P3pp3rF1y/SophisticatedCore)
- [No Chat Reports](https://github.com/Aizistral-Studios/No-Chat-Reports)
- [BlockCarpentry](https://github.com/PianoManu/BlockCarpentry)
- [CreativeCore](https://github.com/CreativeMD/CreativeCore)
- [Extended Crafting](https://github.com/BlakeBr0/ExtendedCrafting)
