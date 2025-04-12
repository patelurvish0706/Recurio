# Recurio 🤖
**AI-based solution that analyzes multiple PDF and image files, scans them, and identifies common, repeated, and twisted versions of questions. It also suggests possible questions that may appear in upcoming exams.**
## 📝 Description

Students often struggle to find frequently asked questions from previous term-end exam papers. **RECURIO** solves this problem with AI!

It analyzes multiple **PDF** and **image** files to detect:

- Repeated or twisted questions  
- Most common questions  
- Predictions for upcoming exam questions  

✅ Supports multiple file uploads (PDFs & Images)

## 🚀 Run Locally

### Step 1: Install Python  
Make sure Python is installed on your device.

### Step 2: Install Required Packages  
```bash
pip install flask PyMuPDF requests
```

### Step 3: Get Your API Keys  

🔍 **OCR API** (for image text extraction)  
- Visit: [ocr.space](https://ocr.space/ocrapi/freekey)  
- Enter your email and subscribe (Free)  
- Verify your email and copy your key  
```python
OCR_API_KEY = "YOUR_OCR_API_KEY"
```

🧠 **OpenRouter AI API** (for question analysis)  
- Visit: [openrouter.ai](https://openrouter.ai/settings/keys)  
- Log in with Google, create a new key  
```python
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"
```

🔐 Save these keys in your config or script file.

### Step 4: Run the App  
```bash
python Recurio.py
```
Now open your browser and visit:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---
