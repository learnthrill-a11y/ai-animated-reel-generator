import streamlit as st
from pathlib import Path
from reel_engine import generate_reel, STYLES, LANGUAGES

st.set_page_config(page_title="AI Animated Reel Studio", page_icon="🎬", layout="wide")
st.title("🎬 AI Animated Reel Studio")
st.caption("Create vertical animated explainer videos in Malayalam, English, or both.")

with st.sidebar:
    st.header("Video settings")
    style = st.selectbox("Animation style", STYLES)
    language = st.selectbox("Language", LANGUAGES)
    duration = st.slider("Seconds per scene", 2, 8, 4)
    theme = st.selectbox("Colour theme", ["Midnight", "Light", "Warm", "Purple", "Green"])
    show_subtitles = st.checkbox("Show subtitles", value=True)
    st.caption("Output: MP4 · 1080 × 1920 · 9:16")

st.subheader("1. Your idea")
topic = st.text_input("Topic / Reel title", placeholder="Example: How does the human brain remember things?")
script = st.text_area(
    "Script or scene text",
    placeholder=(
        "Write your narration and divide scenes using a line containing ---\\n\\n"
        "Scene 1 text...\\n---\\nScene 2 text..."
    ),
    height=230,
)
st.caption("For this starter version, provide the script and separate scenes with ---.")

st.subheader("2. Optional assets")
col1, col2 = st.columns(2)
with col1:
    font_file = st.file_uploader("Upload a Malayalam-compatible TTF/OTF font (recommended)", type=["ttf", "otf"])
with col2:
    music_file = st.file_uploader("Upload licensed background music", type=["mp3", "wav", "m4a"])

st.info(
    "The first build creates animated scenes and captions locally. "
    "AI-generated images and natural AI voice are planned as optional API integrations; "
    "they may require an API key and paid usage."
)

if st.button("✨ Generate animated reel", type="primary", use_container_width=True):
    if not topic.strip() or not script.strip():
        st.error("Please enter a topic and script.")
    else:
        Path("output").mkdir(exist_ok=True)
        font_path = None
        music_path = None
        if font_file:
            font_path = Path("output") / font_file.name
            font_path.write_bytes(font_file.getvalue())
            font_path = str(font_path)
        if music_file:
            music_path = Path("output") / music_file.name
            music_path.write_bytes(music_file.getvalue())
            music_path = str(music_path)

        with st.spinner("Rendering your animated reel. Please wait..."):
            try:
                output = generate_reel(
                    topic=topic,
                    script=script,
                    style=style,
                    language=language,
                    seconds_per_scene=duration,
                    theme=theme,
                    subtitles=show_subtitles,
                    font_path=font_path,
                    music_path=music_path,
                )
                st.success("Your reel is ready.")
                st.video(output)
                with open(output, "rb") as f:
                    st.download_button(
                        "⬇ Download MP4",
                        f,
                        file_name="animated_reel.mp4",
                        mime="video/mp4",
                        use_container_width=True,
                    )
            except Exception as e:
                st.exception(e)

st.divider()
st.caption("Build roadmap: AI script assistance → AI scene images → voice generation → word-timed subtitles → character consistency → batch generation.")
