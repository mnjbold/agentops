"""Generate agentops PWA icons: rounded-rect #0b1220 background with a centered white handset glyph.

Outputs:
  ui/icons/icon-192.png  (192x192)
  ui/icons/icon-512.png  (512x512)
"""
from pathlib import Path
from PIL import Image, ImageDraw

BG = (11, 18, 32, 255)  # #0b1220
FG = (255, 255, 255, 255)

OUT_DIR = Path(__file__).resolve().parent.parent / "ui" / "icons"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def rounded_rect(draw, bbox, radius, fill):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill)


def draw_handset(img: Image.Image, size: int) -> None:
    """Draw a simple, recognizable telephone-handset glyph centered on the canvas.

    Approach: two ellipses for the earpiece and mouthpiece, connected by a thick
    curved bar (the handle). Clean, monochrome, no fine detail — reads at 48px.
    """
    draw = ImageDraw.Draw(img)
    s = size

    # 1. The handle: a thick rotated rectangle. We approximate the tilt
    #    by drawing a polygon for the bar, then putting ellipses on each end.
    cx, cy = s / 2, s / 2
    bar_w = s * 0.085
    bar_len = s * 0.30
    # Tilt the handset ~30 degrees so it looks like a phone icon, not a barbell.
    import math
    angle = math.radians(30)

    def rotated_rect(center_x, center_y, w, h, deg):
        # Build a rotated rectangle as a polygon.
        cos_a = math.cos(math.radians(deg))
        sin_a = math.sin(math.radians(deg))
        pts = []
        for dx, dy in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
            x = center_x + dx * cos_a - dy * sin_a
            y = center_y + dx * sin_a + dy * cos_a
            pts.append((x, y))
        draw.polygon(pts, fill=FG)

    # Handle bar
    rotated_rect(cx, cy, bar_len, bar_w, angle)

    # Earpiece (top-left of the rotated handset) and mouthpiece (bottom-right)
    ear_r = s * 0.115
    mouth_r = s * 0.115
    # Offsets along the rotated bar's long axis
    dx = (bar_len / 2) * math.cos(angle)
    dy = (bar_len / 2) * math.sin(angle)
    ear_x, ear_y = cx - dx, cy - dy
    mouth_x, mouth_y = cx + dx, cy + dy

    # Slightly larger end caps so they read as the ear/mouth piece, not a dumbbell.
    draw.ellipse(
        [ear_x - ear_r, ear_y - ear_r, ear_x + ear_r, ear_y + ear_r],
        fill=FG,
    )
    draw.ellipse(
        [mouth_x - mouth_r, mouth_y - mouth_r, mouth_x + mouth_r, mouth_y + mouth_r],
        fill=FG,
    )

    # Carve small notches at the center of each end cap to suggest the speaker grill.
    notch_r = s * 0.045
    draw.ellipse(
        [ear_x - notch_r, ear_y - notch_r, ear_x + notch_r, ear_y + notch_r],
        fill=BG,
    )
    draw.ellipse(
        [mouth_x - notch_r, mouth_y - notch_r, mouth_x + notch_r, mouth_y + notch_r],
        fill=BG,
    )


def make_icon(size: int, path: Path, corner_radius_ratio: float = 0.18) -> None:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Rounded-rect background fills the entire canvas
    radius = int(size * corner_radius_ratio)
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=BG)

    # Subtle inner border (1px stroke) so the dark-on-dark icon doesn't vanish
    # on a dark taskbar. Use a slightly lighter blue.
    accent = (32, 48, 80, 255)
    draw.rounded_rectangle(
        [2, 2, size - 3, size - 3],
        radius=max(1, radius - 2),
        outline=accent,
        width=max(1, size // 192),
    )

    draw_handset(img, size)
    img.save(path, "PNG", optimize=True)
    print(f"wrote {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    make_icon(192, OUT_DIR / "icon-192.png")
    make_icon(512, OUT_DIR / "icon-512.png")
