from __future__ import annotations

from enum import IntEnum, StrEnum


# Type aliases
HexColorType = str | list[float] | list[int]

BLUE_LIGHT = "#B2CAD4"
BLUE_LIGHT2 = 0xB2CAD4
RED_LIGHT = '0xF2CAD4'

class PalColor(StrEnum):
  """Palette colors stored as integer hex values."""

  BLUE_LIGHT = '#B2CAD4'
  BLUE_STEEL = '0x698894'
  BLUE_NAVY = '0x264653'
  TEAL = '0x62C9C9'


class PaletteColor(IntEnum):
  """Palette colors stored as integer hex values."""

  BLUE_LIGHT = 0xB2CAD4
  BLUE_STEEL = 0x698894
  BLUE_NAVY = 0x264653
  TEAL = 0x62C9C9
  TEAL_LIGHT = 0x73EBEB
  TEAL_DARK = 0x204141
  TEAL_DEEP = 0x0D3D3D
  TEAL_MEDIUM = 0x346A6A
  TEAL_MEDIUM_PLUS = 0x306363
  GREEN_LIGHT = 0x33BC3C
  GREEN = 0x4DAA2A
  GREEN_MEDIUM = 0x4CAF50
  GREEN_MEDIUM2 = 0x2A9A31
  GREEN_DARK = 0x388E3C
  GREEN_DARKER = 0x17561B
  GREEN_DARKER_ALT = 0x195E1E
  GREEN_DEEP = 0x081C09
  ORANGE = 0xFF9800
  COPPER_LIGHT = 0xE89048
  COPPER_ORANGE = 0xF4A261
  COPPER_RED = 0xE76F51
  COPPER_DARK = 0x6A3210
  BRONZE_DEEP = 0x504D47
  BRONZE_DARK = 0x5A3A12
  BRONZE_LIGHT = 0xE0B060
  BRONZE_GOLD = 0xE9C46A
  YELLOW = 0xFFEB3B
  PARCHMENT_LIGHT = 0xFCF5E5
  PARCHMENT = 0xF4EDDE
  PARCHMENT_MEDIUM = 0xD2CCBF
  PARCHMENT_DARK = 0xB0ABA0
  PARCHMENT_DEEP = 0x8E8A81
  PURPLE_LIGHT = 0x8A4A9A
  PURPLE = 0x7B2D8E
  PURPLE_HAZE = 0x7F00FF
  PURPLE_MEDIUM = 0x572064
  PURPLE_DARK = 0x2A0A3A
  RED_LIGHT = 0xF44336
  RED = 0xC1121F
  RED_MEDIUM = 0xB71C1C
  RED_DARK = 0x981515
  RED_DARKER = 0x6F0F0F
  RED_DEEP = 0x4D0B0B
  RED_DEEPER = 0x3A0808


class ColorFormat(StrEnum):
  """Color format identifiers."""

  NONE = '?'
  HASH = '#'
  HEX = '0x'
  FLOAT = 'float'
  INT = 'int'


class RGBA:
  """Makes a PaletteColor available in different output formats."""

  COLOR_NAMES: set[str] = {c.name for c in PaletteColor}
  RGBA_PROP: list[str] = ['red', 'green', 'blue', 'alpha']

  def __init__(self, color: PaletteColor, alpha: float = 0.0):
    """
    Initialize with a PaletteColor and optional alpha.

    :param color: A PaletteColor enum member.
    :param alpha: Alpha channel value (0.0-1.0).
    """
    if color.name not in self.COLOR_NAMES:
      raise ValueError(
        f"Specified color {color} is not in COLOR_NAMES; "
        f"choose one of {sorted(self.COLOR_NAMES)}"
      )

    self.alpha: float = alpha
    self._color: PaletteColor = color

  @property
  def color_name(self) -> str:
    """The enum member name of this color."""
    return self._color.name

  @property
  def color_value(self) -> str:
    """The hex string representation of this color (e.g. '0x264653')."""
    return hex(self._color.value)

  def detect_color_format(self, value: str) -> ColorFormat:
    """
    Detect the color format of a given string value.

    :param value: A color string to inspect.
    :returns: The detected ColorFormat.
    """
    result: ColorFormat = ColorFormat.NONE
    if value.startswith(ColorFormat.HASH):
      result = ColorFormat.HASH
    elif value.startswith(ColorFormat.HEX):
      result = ColorFormat.HEX
    elif '[' in value:
      result = ColorFormat.FLOAT if '.' in value else ColorFormat.INT
    return result

  def hex_str(self, alt_prefix: str = '#') -> str:
    """
    Return hex color string with an alternative prefix.

    :param alt_prefix: Prefix to use instead of '0x' (default '#').
    :returns: The color as a hex string with the given prefix.
    """
    return self.color_value.replace('0x', alt_prefix)

  def as_int_list(self) -> list[int]:
    """Return the color as a list of [R, G, B, A] integer values (0-255)."""
    return RGBA._rgba_color(self.color_value, normalize=False)

  def as_float_list(self) -> list[float]:
    """Return the color as a list of [R, G, B, A] float values (0.0-1.0)."""
    return RGBA._rgba_color(self.color_value, normalize=True)

  def hex_color(self, color: PaletteColor, fmt: ColorFormat = ColorFormat.HASH,
                force_alpha: float = 0.0) -> HexColorType:
    """
    Convert a PaletteColor to the specified format.

    :param color: The PaletteColor to convert.
    :param fmt: Target ColorFormat.
    :param force_alpha: If nonzero, append alpha channel to 6-digit hex.
    :returns: Color in the requested format.
    """
    clr: str = hex(color.value)
    if force_alpha and len(clr) == 6:
      clr = f"{clr}{round(force_alpha * 255.0):02x}"

    is_float: bool = fmt == ColorFormat.FLOAT
    res: HexColorType = clr
    if fmt == ColorFormat.FLOAT or fmt == ColorFormat.INT:
      res = RGBA._rgba_color(clr, is_float)
    elif fmt == ColorFormat.HASH:
      res = clr.replace('0x', '#')
    return res

  @staticmethod
  def _rgba_color(hex_clr: str, normalize: bool = True) -> list[float] | list[int]:
    """
    Parse a hex color string into RGBA components.

    :param hex_clr: An RGBA color as hex string prefixed with '0x'.
    :param normalize: If True, return floats (0.0-1.0); otherwise ints (0-255).
    :returns: List of [R, G, B] or [R, G, B, A] values.
    """
    # Strip '0x' prefix
    raw: str = hex_clr[2:] if hex_clr.startswith('0x') else hex_clr
    rgba: list[str] = [raw[i:i + 2] for i in range(0, len(raw), 2)]
    for n, v in enumerate(rgba[:3]):
      assert len(v) > 0, f"Value for `{RGBA.RGBA_PROP[n]}` should be a hex string"

    colors: list[int] = [int(c, 16) for c in rgba if c]
    return [float(c) / 255.0 for c in colors] if normalize else colors
