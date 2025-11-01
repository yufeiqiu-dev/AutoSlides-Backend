# 🪄 AutoSlides Backend

AutoSlides is a **Flask-based API** that converts PDF documents into structured PowerPoint presentations using an **LLM (Google Gemini)**.  
It extracts text and images from the input PDF, generates slide content using the Gemini API, and returns a downloadable `.pptx` file.

---

## 🚀 Features

- 📄 **Upload PDF → Generate PowerPoint (.pptx)**
- 🧠 **Gemini-powered slide generation** (LLM creates structured JSON slide content)
- 🖼️ **Automatic parsing of text and images** using `PyMuPDF` (`fitz`) and `pdfplumber`
- 🧱 **Flask REST API** ready for frontend or client integration
- 🧪 **Comprehensive pytest coverage**
- 🧰 **Environment-based config (.env)** for API keys
- 🧾 **Structured logging** for all stages of the pipeline

---

## 🧩 Project Structure
```
AutoSlides-backend/
├── app/
│ ├── init.py
│ ├── app.py # Flask entrypoint (create_app)
│ ├── routes.py # Defines /pdf2slides endpoint
│ ├── tools/
│ │ ├── init.py
│ │ ├── pdf_parser.py # PDF → text & images
│ │ ├── pdf_to_slides.py # Orchestrates the full pipeline
│ │ ├── TextToSlideContent.py # LLM interaction (Gemini)
│ │ └── json_to_ppt.py # JSON → PowerPoint
│ └── utils/
| │ ├── init.py
| │ └── logger.py # Centralized logging
├── test/
│ ├── init.py
│ ├── pdf_parser_test.py
│ ├── pdf_to_slides_test.py
│ ├── api_tests/
│ │ ├── pdf2slides_api_test.py
│ └── files/
│ └── test_simple_pdf.pdf
├── .env # Holds GOOGLE_API_KEY
├── requirements.txt
├── pytest.ini
└── README.md
```
## 🧠 How It Works

1. **Upload PDF**  
   The client sends a `multipart/form-data` POST request to `/pdf2slides` with key named file and value as the pdf file.

2. **Receive PPTX**
    The client then receives the pptx powerpoint


## Installation
1. Clone the repo
2. Create a virtua environment
 - python3 -m venv .venv
 - source .venv/bin/activate
3. install the requirements via pip
 - pip install -r requirements.txt
4. save your gemini api key to the environment
 - GOOGLE_API_KEY=your_google_gemini_api_key_here
5. run the server
 - python -m app.app
6. upload via Postman or curl
