#Spip install flask
#Spip install pdfplumber
#Spip install requests

from flask import Flask, request, render_template_string
import fitz  # PyMuPDF
import requests

app = Flask(__name__)

# Prefer to simply Enter email and confirm mail, will get api in mail https://ocr.space/ocrapi/freekey
OCR_API_KEY = "YOUR_OCR_API_KEY"
# Prefer to simply login on this site and click on *Create key* https://openrouter.ai/settings/keys
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"

HTML_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Recurio – Study Smart, Not Hard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    :root {
      --primary: #4a90e2;
      --accent: #2ecc71;
      --bg: #f0f4f8;
      --white: #ffffff;
      --dark: #2c3e50;
    }

    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
    }

    .container {
      margin:20px;
      background: var(--white);
      padding: 1rem 2rem;
      max-width: 700px;
      width: 90%;
      border-radius: 16px;
      box-shadow: 0 5px 35px rgba(0,0,0,0.08);
      position: relative;
      z-index: 2;
      animation: fadeIn 2s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    h1 {
      font-size: 2rem;
      color: var(--primary);
      margin:0;
      text-align: center;
    }

    h3{
        margin:0;
    }

    .slogan {
      color: #555;
      font-style: italic;
      font-size: 1rem;
      margin: 0px 0px 15px 0px;
      text-align: center;
    }

    ol{
        margin-left: -15px;
    }

    .instructions, .note {
      text-align: left;
      background: #eef6ff;
      padding: 1rem ;
      border-left: 5px solid var(--primary);
      border-radius: 8px;
      margin-bottom: 1.5rem;
    }

    li {
      margin-bottom: 0.5rem;
    }

    form {
      margin-bottom: 1.5rem;
    }

    input[type="file"] {
        display: block;
        padding: 12px;
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        background-color: #f9fafb;
        cursor: pointer;
        margin-bottom: 10px;
        text-align: center;
        font-size:16px;
        width:60%;
    }

    form{
        display: flex;
        flex-direction: column;
        align-items:center;
    
    }
    
    input[type="submit"], button {
      background: var(--primary);
      color: white;
      border: none;
      padding: 0.6rem 1.2rem;
      font-size: 1rem;
      border-radius: 10px;
      cursor: pointer;
      margin: 0.5rem 0.4rem;
    }

    #fileInput::file-selector-button {
            padding: 5px 10px;
            border: transparent;
            margin-right: 10px;
            border-radius: 4px;
        }

    button:hover, input[type="submit"]:hover {
      background: #3b7bd4;
    }

    .loader {
      display: none;
      margin: 2rem auto;
      border: 8px solid #f3f3f3;
      border-top: 8px solid var(--primary);
      border-radius: 50%;
      width: 60px;
      height: 60px;
      animation: spin 1s linear infinite;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    .RESPONSE {
      background: #f1fff4;
      border-left: 5px solid var(--accent);
      padding: 1.2rem;
      border-radius: 8px;
      margin-top: 1.5rem;
      animation: fadeIn 1s ease;
    }

    .result-title {
      font-size: 1.4rem;
      color: var(--accent);
      margin-top: 2rem;
    }

    .toolbar {
      margin-top: 1rem;
      display: flex;
      justify-content: end;
    }

    footer {
      margin: 2rem;
      font-size: 0.9rem;
      color: #aaa;
      text-align: center;
    }

    @media (max-width: 600px) {
      .container {
        margin:0;
        padding:1.2rem;
      }

      input[type="submit"], button {
        display: block;
        width: 100%;
        margin: 0.4rem 0;
      }

      input[type="file"] {
        width: -webkit-fill-available;
      }

      .toolButton {
        width: 25%;
        margin: 10px 0 0 20px;
        justify-self: center;
       }
    }
  </style>
  <script>
    function showLoader() {
      document.querySelector('.loader').style.display = 'block';
    }

    function copyQuestions() {
      const container = document.querySelector('.RESPONSE');
      if (!container) return;

      const tempEl = document.createElement("textarea");
      tempEl.value = container.innerText;
      document.body.appendChild(tempEl);
      tempEl.select();
      document.execCommand("copy");
      document.body.removeChild(tempEl);
      alert("✅ Questions copied to clipboard!");
    }

    function clearResults() {
      document.querySelector('form').reset();
      const result = document.querySelector('.RESPONSE');
      const title = document.querySelector('.result-title');
      const toolbar = document.querySelector('.toolbar');

      if (result) result.remove();
      if (title) title.remove();
      if (toolbar) toolbar.remove();
    }
  </script>
</head>
<body>
  <div class="container">
    <h1>Recurio</h1>
    <p class="slogan">Study Smart, Not Hard.</p>

    <div class="note">
      <strong>🎯 Solution: </strong>Sometimes students struggle to find commonly asked questions in term-end exam papers for preparation. Here is a simple AI-based solution that analyzes multiple PDF and image files, scans them, and identifies common, repeated, and twisted versions of questions. It also suggests possible questions that may appear in upcoming exams.<br>(Supports multiple file uploads: PDFs and images)
    </div>

    <div class="instructions">
      <h3>📘 How to Use:</h3>
      <ol>
        <li>Select one or more PDFs or image files (PNG, JPG, JPEG).</li>
        <li>Click <strong>Analyze</strong> to extract and compare content.</li>
        <li>Get a clear, grouped list of repeated or common questions.</li>
        <li>Copy them to revise or share easily.</li>
      </ol>
    </div>

    <form method="POST" enctype="multipart/form-data" onsubmit="showLoader()">
      <input type="file" name="files" id="fileInput" accept=".pdf,.png,.jpeg,.jpg" multiple required>
      <input type="submit" value="Analyze">
    </form>

    <div class="loader"></div>

    {% if response %}
      <h3 class="result-title">✅Scan Completed. Here is your Result.</h3>
      <div class="RESPONSE">{{ response|safe }}</div>
      <div class="toolbar">
        <button class="toolButton" onclick="copyQuestions()">Copy</button>
        <button class="toolButton" onclick="clearResults()">Clear</button>
      </div>
    {% endif %}

    <footer>
      &copy; 2025 <strong>Recurio</strong> – Built for smart learners.<br>Urvish & Drushti
    </footer>

  </div>
</body>
</html>
'''


def extract_text_from_pdf(file_stream):
    text = ""
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_image_api(file):
    response = requests.post(
        "https://api.ocr.space/parse/image",
        files={"file": (file.filename, file.stream, file.content_type)},
        data={"apikey": OCR_API_KEY, "language": "eng", "OCREngine": "2"},
    )
    result = response.json()
    if result.get("IsErroredOnProcessing"):
        return "[OCR Error]"
    return result["ParsedResults"][0]["ParsedText"]

def call_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",  # fast + free
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    if response.status_code != 200:
        return f"<p>Error from OpenRouter: {response.status_code}</p>"
    result = response.json()
    return result["choices"][0]["message"]["content"]

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    extracted_text = ""
    openrouter_response = ""

    if request.method == 'POST':
        files = request.files.getlist('files')
        for file in files:
            filename = file.filename.lower()
            if filename.endswith('.pdf'):
                content = extract_text_from_pdf(file.stream)
            elif filename.endswith(('.png', '.jpg', '.jpeg')):
                content = extract_text_from_image_api(file)
            else:
                content = "[Unsupported file type]"
            extracted_text += f"{file.filename}\n{content.strip()}\n\n"

        # Build prompt
        prompt = ( extracted_text +
            "\n\n\nPROMPT : Here are multiple documents with their text content.\n"
            "compare all different texts, and list Similar types of questions, Repeating or duplicate questions, Commonly asked questions\n\n"
            "Format only all that questions like this : <ol><li>question</li></ol>\n\nDo not add any other text, Only question list is required.\n\n"
            
        )
        openrouter_response = call_openrouter(prompt)

    return render_template_string(HTML_FORM, extracted_text=extracted_text, response=openrouter_response)

if __name__ == '__main__':
    app.run(debug=True)
