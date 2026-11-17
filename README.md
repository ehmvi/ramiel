# ramiel

theme discord facon tui, base sur [system24](https://github.com/refact0r/system24), pour vesktop / equibop / vencord.

## structure

- `src/ramiel.css` : toute la structure, sans couleurs. ne lit que les variables `--m-*`.
- `palettes/*.css` : une palette par variante (`--m-*`, noms des cles matugen).
  - `ramiel.css` : vert/bleu, tire du fond d ecran ramiel.
  - `orange.css` : orange fige, pour un 2e client.
- `matugen/ramiel-colors.css` : modele matugen. le fichier genere ecrase la palette
  avec `:root:root`, a activer en plus du theme.
- `themes.nix` : colle en-tete + base + palette, un fichier `.theme.css` par variante.
- `t3code/` : les memes palettes pour t3 code. `build.py` lit `palettes/*.css` et
  ecrit un `<id>.json` par variante (`ramiel`, `ramiel-orange`).

## ajouter une variante

1. `palettes/<nom>.css` avec toutes les variables `--m-*` (y compris `--m-core` et `--m-ambre`).
2. une entree de plus dans `themes.nix`.
3. une entree de plus dans `VARIANTS` de `t3code/build.py`, puis `python3 t3code/build.py`.

## t3 code

```sh
python3 t3code/build.py                 # regenere t3code/*.json depuis les palettes
cp t3code/*.json ~/.t3/userdata/themes/ # publie (puis choisir dans reglages > apparence)
t3 theme set ramiel                     # ou : en faire le theme de l environnement
```

## utilisation (nixos-config)

entree flake `ramiel` (`flake = false`), puis `import "${inputs.ramiel}/themes.nix"`.
pour tester sans pousser : `--override-input ramiel ~/code/ramiel`.
