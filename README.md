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

## ajouter une variante

1. `palettes/<nom>.css` avec toutes les variables `--m-*` (y compris `--m-core` et `--m-ambre`).
2. une entree de plus dans `themes.nix`.

## utilisation (nixos-config)

entree flake `ramiel` (`flake = false`), puis `import "${inputs.ramiel}/themes.nix"`.
pour tester sans pousser : `--override-input ramiel ~/code/ramiel`.
