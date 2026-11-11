# themes vencord (vesktop, equibop...) : en-tete + src/ramiel.css + une palette.
# un theme vencord ne peut pas importer un fichier local, d ou un seul fichier
# par theme. renvoie { "<fichier>.theme.css" = "<contenu>"; }, sans nixpkgs :
#   import "${ramiel}/themes.nix"
let
  base = builtins.readFile ./src/ramiel.css;

  mk =
    {
      name,
      description,
      palette,
    }:
    ''
      /**
       * @name ${name}
       * @description ${description}
       * @author fyrr
       * @version 0.2.0
      */

    ''
    + base
    + "\n"
    + builtins.readFile palette;
in
{
  "ramiel.theme.css" = mk {
    name = "ramiel";
    description = "a tui-style discord theme based on system24, colored by the wallpaper (matugen). sixth angel.";
    palette = ./palettes/ramiel.css;
  };

  "ramiel-orange.theme.css" = mk {
    name = "ramiel (orange)";
    description = "ramiel with a fixed orange palette, to tell a second client apart at a glance. sixth angel.";
    palette = ./palettes/orange.css;
  };
}
