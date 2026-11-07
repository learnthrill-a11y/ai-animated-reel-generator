# AI Animated Reel Generator — Starter Build

A Python + Streamlit starter app for creating vertical animated explainer reels.

## Current starter features
- Seven selectable visual styles: Stick Figure, 2D Cartoon, 3D Cinematic-inspired,
  Motion Graphics, Kinetic Typography, Whiteboard Explainer and Minimal Infographic
- Malayalam, English and Malayalam + English language setting
- Script-to-scenes using `---`
- 9:16 vertical MP4 output (1080 × 1920)
- Optional uploaded music
- Optional custom TTF/OTF font upload for Malayalam text
- Simple animated zoom effect

## Important limitation
This first build creates stylized graphics locally. The "3D Cinematic" option is a
placeholder visual treatment, not true AI-generated 3D character animation.
Natural AI narration, generated scene artwork, lip-sync, consistent characters and
word-level subtitle timing need external AI services and will be added as separate
optional integrations. API usage may cost money.

## Run on Windows
1. Install Python 3.11 or 3.12.
2. Extract this ZIP.
3. Open Command Prompt in the extracted folder.
4. Run:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

5. Open the local address shown in the terminal.

## Script format
Separate each scene with a line containing three hyphens:

```text
Opening hook for the reel.
---
Explain the first point.
---
End with a memorable takeaway.
```

## Malayalam font
For reliable Malayalam rendering, upload a Malayalam-capable TTF/OTF font in the app.
A font with Malayalam glyphs is required. Pillow's text shaping support depends on
the installed Pillow build and libraqm support; if conjunct letters render incorrectly,
use a libraqm-enabled Pillow build or render text through a browser/HTML renderer.

## GitHub
Create a new repository named `ai-animated-reel-generator`, upload the project files,
and commit. Do not upload API keys or passwords. Use environment secrets for future
API integrations.
