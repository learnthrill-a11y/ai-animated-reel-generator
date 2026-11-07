from pathlib import Path
import re
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip

W, H = 1080, 1920
OUT = Path("output")
OUT.mkdir(exist_ok=True)

STYLES = [
    "Stick Figure", "2D Cartoon", "3D Cinematic", "Motion Graphics",
    "Kinetic Typography", "Whiteboard Explainer", "Minimal Infographic"
]
LANGUAGES = ["Malayalam", "English", "Malayalam + English"]

PALETTES = {
    "Midnight": ("#101827", "#F8FAFC", "#F5C451"),
    "Light": ("#F5F2EA", "#172033", "#C15B3C"),
    "Warm": ("#2A1D1A", "#FFF7ED", "#F4A261"),
    "Purple": ("#211631", "#FFFFFF", "#D7B8FF"),
    "Green": ("#102D28", "#F3FFF9", "#B8D98A"),
}

def get_font(size, bold=False, custom=None):
    candidates = []
    if custom:
        candidates.append(custom)
    candidates += [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for p in candidates:
        if p and Path(p).exists():
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                pass
    return ImageFont.load_default()

def split_scenes(script):
    scenes = [x.strip() for x in re.split(r"\n\s*---+\s*\n", script) if x.strip()]
    return scenes or [script.strip()]

def wrap(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        try:
            width = draw.textbbox((0, 0), candidate, font=font)[2]
        except Exception:
            width = len(candidate) * 22
        if width <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw_stick_figure(draw, cx, cy, scale, colour, pose=0):
    r = int(62 * scale)
    width = max(10, int(18 * scale))
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=colour, width=width)
    draw.line((cx, cy+r, cx, cy+int(300*scale)), fill=colour, width=width)
    # arms vary slightly by scene
    if pose % 2 == 0:
        draw.line((cx, cy+int(125*scale), cx-int(145*scale), cy+int(225*scale)), fill=colour, width=width)
        draw.line((cx, cy+int(125*scale), cx+int(145*scale), cy+int(225*scale)), fill=colour, width=width)
    else:
        draw.line((cx, cy+int(125*scale), cx-int(155*scale), cy+int(70*scale)), fill=colour, width=width)
        draw.line((cx, cy+int(125*scale), cx+int(155*scale), cy+int(70*scale)), fill=colour, width=width)
    draw.line((cx, cy+int(300*scale), cx-int(125*scale), cy+int(480*scale)), fill=colour, width=width)
    draw.line((cx, cy+int(300*scale), cx+int(125*scale), cy+int(480*scale)), fill=colour, width=width)

def render_scene(topic, text, index, total, style, language, theme, subtitles, font_path):
    bg, fg, accent = PALETTES[theme]
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    title_font = get_font(64, True, font_path)
    body_font = get_font(54, False, font_path)
    small_font = get_font(30, True, font_path)

    # visual style elements
    if style in ("Stick Figure", "2D Cartoon", "Whiteboard Explainer"):
        if style == "Whiteboard Explainer":
            im = Image.new("RGB", (W, H), "#FFFEFA")
            d = ImageDraw.Draw(im)
            fg, accent = "#202020", "#2878B5"
        draw_stick_figure(d, W//2, 510, 1.0, accent, index)
        d.rounded_rectangle((75, 90, W-75, H-90), radius=38, outline=accent, width=5)
    elif style == "3D Cinematic":
        # Stylized cinematic gradient-like bands; replace with AI scene images in the API-enabled build.
        for y in range(H):
            t = y / H
            c1 = tuple(int(bg.lstrip("#")[i:i+2], 16) for i in (0,2,4))
            c2 = tuple(max(0, min(255, int(v*(1-t*0.45)))) for v in c1)
            d.line((0, y, W, y), fill=c2)
        d.ellipse((170, 260, 910, 1000), fill=accent)
        d.ellipse((300, 390, 780, 870), fill=bg)
    elif style in ("Motion Graphics", "Minimal Infographic"):
        d.rounded_rectangle((100, 270, 980, 1040), radius=70, outline=accent, width=14)
        for j in range(4):
            x = 230 + j*205
            d.ellipse((x-55, 590-55, x+55, 590+55), fill=accent if j == index % 4 else fg)
        d.line((190, 800, 890, 800), fill=accent, width=12)
    elif style == "Kinetic Typography":
        for j in range(6):
            y = 300 + j*145
            d.rounded_rectangle((95, y, 985, y+90), radius=18, fill=accent if j == index % 6 else fg)

    # Header and slide number
    label = f"{style.upper()}  •  {language.upper()}"
    d.text((105, 145), label, font=small_font, fill=accent)
    title_lines = wrap(d, topic, title_font, 850)
    y = 1120
    for line in title_lines[:2]:
        d.text((100, y), line, font=title_font, fill=fg)
        y += 82

    # Caption panel
    if subtitles:
        panel_top = 1390
        d.rounded_rectangle((75, panel_top, W-75, 1745), radius=34, fill="#000000")
        lines = wrap(d, text, body_font, 820)
        ty = panel_top + 45
        for line in lines[:4]:
            d.text((125, ty), line, font=body_font, fill="#FFFFFF")
            ty += 72
    else:
        lines = wrap(d, text, body_font, 850)
        ty = 1380
        for line in lines[:5]:
            d.text((100, ty), line, font=body_font, fill=fg)
            ty += 75

    d.text((105, H-145), "CREATED WITH AI ANIMATED REEL STUDIO", font=small_font, fill=accent)
    d.text((W-210, H-145), f"{index+1}/{total}", font=small_font, fill=fg)
    return im

def generate_reel(topic, script, style="Stick Figure", language="Malayalam + English",
                  seconds_per_scene=4, theme="Midnight", subtitles=True,
                  font_path=None, music_path=None):
    scenes = split_scenes(script)
    clips = []
    for i, scene_text in enumerate(scenes):
        frame = render_scene(topic, scene_text, i, len(scenes), style, language,
                             theme, subtitles, font_path)
        # Gentle zoom/pan animation rather than static slides.
        base = np.asarray(frame)
        duration = seconds_per_scene
        clip = ImageClip(base).with_duration(duration)
        # MoviePy v2 resize effect for subtle motion
        try:
            from moviepy import vfx
            clip = clip.with_effects([vfx.Resize(lambda t: 1.0 + 0.025 * (t / max(duration, 0.1)))])
            clip = clip.with_position("center")
        except Exception:
            pass
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")
    if music_path:
        audio = AudioFileClip(music_path)
        if audio.duration > video.duration:
            audio = audio.subclipped(0, video.duration)
        video = video.with_audio(audio)

    output = OUT / "animated_reel.mp4"
    video.write_videofile(str(output), fps=24, codec="libx264", audio_codec="aac",
                          preset="medium", threads=4)
    video.close()
    for c in clips:
        c.close()
    return str(output)
