# Sketch2App AI — HackFest 2.0

A fast prototype for Track 2: Best Use of Gemma 4. Upload a hand-drawn interface sketch, generate a single-file HTML/CSS page, preview it, and download it.

## Requirements
- Windows laptop
- Python 3.10 or newer
- VS Code
- Internet connection
- Google AI Studio API key with access/quota for Gemma 4

## Setup on Windows

1. Extract the ZIP file.
2. Open the extracted `sketch2app_hackfest` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

5. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt terminal and run:

   ```bat
   .venv\Scripts\activate.bat
   ```

6. Install packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

7. Copy `.env.example` to a new file named `.env`. Paste your API key after `GOOGLE_API_KEY=`. Do not share this file or upload it to GitHub.

8. Start the app:

   ```powershell
   python -m streamlit run app.py
   ```

9. Streamlit should open a local browser page. Upload a clear sketch photo and click **Generate my app**.

## API key
Create/get a key in Google AI Studio: https://aistudio.google.com/apikey

The app calls `gemma-4-26b-a4b-it`. If the model is unavailable to your key, check current model access, quota, and the official Gemma API documentation before changing the model name.

## Demo plan (2 minutes)
1. Show the paper sketch and explain the problem: turning a design idea into code takes time.
2. Upload the sketch.
3. Generate the page and show the live preview.
4. Download the HTML file and explain that it can be opened in a browser.
5. Explain the AI pipeline: image input → visual layout understanding → HTML/CSS generation → preview.

## Important limitations
- This is a hackathon MVP, not production-grade code.
- Generated pages can differ from the sketch; clearer photos and specific instructions help.
- Review generated HTML before deploying it publicly.
- Never hard-code or commit your API key.
