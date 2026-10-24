import os
import re
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(page_title="Sketch2App AI", page_icon="✏️", layout="wide")

st.markdown("""
<style>
.stApp {background: #0b1020; color: #edf2ff;}
section[data-testid="stSidebar"] {background: #121a2e;}
.hero {padding: 1.5rem 1.6rem; border: 1px solid #293653; border-radius: 20px;
       background: linear-gradient(120deg,#182746,#111827); margin-bottom: 1rem;}
.hero h1 {margin: 0; font-size: 2.35rem;}
.hero p {color:#bac7e5; margin-bottom:0;}
.pill {display:inline-block; padding:4px 10px; border-radius:99px;
       background:#24365c; color:#b8d0ff; font-size:0.8rem; margin-bottom:8px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="pill">HACKFEST 2.0 · TRACK 2</div>
  <h1>✏️ Sketch2App AI</h1>
  <p>Turn a hand-drawn UI sketch into a working web page with Gemma 4.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("How it works")
    st.write("1. Upload a sketch photo")
    st.write("2. Gemma 4 studies the layout")
    st.write("3. Generate HTML + CSS")
    st.write("4. Preview and download the result")
    st.divider()
    st.caption("Built for the HackFest 2.0 Sketch-to-App Screen challenge.")

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.warning("API key not found. Add GOOGLE_API_KEY to your .env file, then restart the app.")

left, right = st.columns([0.9, 1.1], gap="large")
with left:
    st.subheader("① Upload your sketch")
    uploaded = st.file_uploader("Choose a photo (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    style = st.selectbox("Visual style", ["Modern and minimal", "Colorful and playful", "Professional dashboard", "Dark mode"])
    extra = st.text_input("Extra instructions (optional)", placeholder="e.g. Use purple buttons and rounded cards")
    if uploaded:
        st.image(uploaded, caption="Your uploaded sketch", use_container_width=True)

    generate = st.button("✨ Generate my app", type="primary", use_container_width=True, disabled=not uploaded)

if "html_code" not in st.session_state:
    st.session_state.html_code = ""

if generate:
    if not api_key:
        st.error("Missing GOOGLE_API_KEY. Follow the setup steps in README.md.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            image_bytes = uploaded.getvalue()
            mime_type = uploaded.type or "image/jpeg"
            prompt = f"""
You are an expert frontend developer participating in a student hackathon.
Analyze the attached hand-drawn UI sketch and create a faithful, polished, responsive web page.
Visual style: {style}.
Additional user instructions: {extra or "Follow the sketch closely."}

Return ONLY one complete HTML document. Include all CSS inside a <style> tag and any JavaScript inside a <script> tag.
Do not use Markdown fences. Do not use external libraries, external images, remote fonts, or external network resources.
Use semantic HTML, accessible labels, responsive layout, and realistic placeholder content.
Preserve the major positions, boxes, labels, navigation, and proportions visible in the sketch.
The page should look polished but remain recognizably based on the sketch.
"""
            with st.spinner("Gemma 4 is reading your sketch and writing the interface..."):
                response = client.models.generate_content(
                    model="gemma-4-26b-a4b-it",
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                        prompt
                    ],
                    config=types.GenerateContentConfig(temperature=0.3)
                )
            raw = (response.text or "").strip()
            raw = re.sub(r"^```(?:html)?\s*", "", raw, flags=re.I)
            raw = re.sub(r"\s*```$", "", raw)
            if "<html" not in raw.lower() and "<!doctype" not in raw.lower():
                st.error("The model did not return a full HTML page. Try a clearer sketch photo.")
            else:
                st.session_state.html_code = raw
                st.success("Your first version is ready!")
        except Exception as e:
            st.error(f"Generation failed: {e}")
            st.info("Check your API key, internet connection, model access, and quota. You can still use the demo mode below.")

with right:
    st.subheader("② Live app preview")
    if st.session_state.html_code:
        components.html(st.session_state.html_code, height=560, scrolling=True)
        st.download_button(
            "⬇️ Download generated HTML",
            data=st.session_state.html_code,
            file_name="sketch2app_generated.html",
            mime="text/html",
            use_container_width=True
        )
    else:
        st.info("Your generated page will appear here.")
        st.markdown("**Demo mode:** You can test the preview panel even before adding an API key.")
        demo = """<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font-family:Arial,sans-serif;background:#f4f6fb;color:#172033;padding:24px}
.card{background:white;border-radius:18px;padding:22px;box-shadow:0 8px 28px #1d2a4414;max-width:600px;margin:auto}
nav{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #eee;padding-bottom:14px}
button{background:#6258e8;color:white;border:0;border-radius:10px;padding:11px 16px}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:20px}
.tile{background:#f0efff;border-radius:12px;padding:18px}small{color:#68728a}</style></head><body>
<div class="card"><nav><b>✦ My Dashboard</b><button>Get started</button></nav>
<h1>Your idea, made real.</h1><p>Here is a sample interface preview.</p>
<div class="grid"><div class="tile"><small>PROJECTS</small><h2>08</h2></div>
<div class="tile"><small>PROGRESS</small><h2>76%</h2></div></div></div></body></html>"""
        components.html(demo, height=400, scrolling=True)

st.divider()
st.caption("Prototype note: Generated HTML is previewed in an isolated component. Review generated code before using it in a real production site.")
