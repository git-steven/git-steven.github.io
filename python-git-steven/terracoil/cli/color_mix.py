from __future__ import annotations
from coloraide import Color
from coloraide.css.color_names import name2val_map
from freyja import FreyjaCLI


class ColorMix:
  """Color manipulation commands backed by coloraide."""

  def mix_grayscale(self, colors: str, ratios: str, grayscale: float=-1) -> None:
     color_list: list[str] = [c.strip() for c in colors.split(',') if c.strip()]
     gray_list: list[str]

     for color in color_list:
       c:color = Color(color)
       g:color = c.filter('grayscale', 1, out_space='hsl')
       g.luminance()

     Color(c).filter('grayscale', 1, out_space='hsl')



     Color.average(color_list, ratios)

  def mix(self, colors: str, ratios: str) -> None:
    """
    Weighted mix of two or more colors.

    :param colors: Comma-separated colors (named or hex), e.g. ``orange,purple,white``.
    :param ratios: Comma-separated weights in [0,1]. If one fewer than ``colors``,
                   the trailing weight is computed as ``1.0 - sum(ratios)``.
    """
    color_list: list[str] = [c.strip() for c in colors.split(',') if c.strip()]
    ratio_list: list[float] = [float(r) for r in ratios.split(',') if r.strip()]
    if len(ratio_list) == len(color_list) - 1:
      ratio_list.append(1.0 - sum(ratio_list))
    if len(ratio_list) != len(color_list):
      raise ValueError(
        f"ratios length ({len(ratio_list)}) must equal colors length "
        f"({len(color_list)}) or be one fewer"
      )
    mixed: Color = Color.weighted_mix(color_list, ratio_list)
    print(repr(mixed))
    print(mixed.convert('srgb').to_string(hex=True))

  def ls(self, name: str | None = None) -> None:
    """
    List CSS named colors, optionally filtered by substring.

    :param name: Substring filter; if given, only names containing it are shown.
    """
    all_names: list[str] = sorted(name2val_map.keys())
    shown: list[str] = [n for n in all_names if name in n] if name else all_names
    qualifier: str = f" (containing '{name}')" if name else ""
    print(f"Total Named Colors{qualifier}: {len(shown)}")
    for nm in shown:
      hex_value: str = Color(nm).to_string(hex=True)
      print(f"Color({nm}) = Color({hex_value})")

  @staticmethod
  def _main() -> None:
    """Poetry entrypoint; private so Freyja's default filter omits it from --help."""
    FreyjaCLI(ColorMix).run()
