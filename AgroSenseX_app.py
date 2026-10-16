import os
import tempfile
import sqlite3
import hashlib
import hmac
import secrets
from pathlib import Path

import streamlit as st
from PIL import Image

# AgroSense-X app. Keep predictor.py, chatbot.py, result_explainer.py,
# knowledge/diseases.json and Models/ in the same project folder.

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="AgroSense-X | Plant Disease Intelligence",
    page_icon="🌱",
    layout="wide",
)


# Fresh green visual theme for AgroSense-X
st.markdown(
    """
    <style>
    :root { --green:#16a34a; --deep:#14532d; --navy:#172333; --mint:#eaf8ef; }
    .stApp, [data-testid="stAppViewContainer"] {
      background: linear-gradient(135deg,#e9f8ef 0%,#f7fcf8 52%,#e1f4e7 100%) !important;
      color:#172333;
    }
    [data-testid="stHeader"] { background:rgba(234,248,239,.92) !important; }
    [data-testid="stSidebar"] {
      background:linear-gradient(180deg,#172333 0%,#203447 100%) !important;
      border-right:3px solid #22a05a;
    }
    [data-testid="stSidebar"] * { color:#edf8f0 !important; }
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] div[data-baseweb="select"] * {
      color:#172333 !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] {
      background:#26384a !important; border:1px solid #3c5865 !important; border-radius:12px !important;
    }
    .main .block-container { padding-top:1.8rem; max-width:1450px; }
    h1,h2,h3 { color:#14743a !important; }
    [data-testid="stCaptionContainer"] { color:#5e806a !important; }
    .agro-hero {
      background:linear-gradient(120deg,#0f8f48,#17a765 58%,#1478bd);
      color:white; padding:28px 30px; border-radius:22px; margin:8px 0 22px;
      box-shadow:0 12px 28px rgba(16,100,55,.18);
    }
    .agro-hero h1 {color:white !important; margin:0; font-size:2.55rem;}
    .agro-hero p {color:#e8fff0; font-size:1.08rem; margin:.45rem 0 0;}
    .agro-card {
      background:rgba(255,255,255,.88); border:1px solid #c5e8d0; border-radius:18px;
      padding:18px 20px; box-shadow:0 6px 20px rgba(26,95,55,.07); margin-bottom:14px;
    }
    [data-testid="stMetric"] {background:#e0f5e6;border:1px solid #b5e2c1;border-radius:14px;padding:14px;}
    [data-testid="stMetricValue"] {color:#13803d !important;}
    .stButton > button, .stFormSubmitButton > button {
      border-radius:12px !important; border:1px solid #159447 !important;
      background:linear-gradient(100deg,#16a34a,#079669) !important; color:white !important;
      font-weight:700; min-height:2.65rem; transition:all .15s ease;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
      background:linear-gradient(100deg,#117437,#087c5b) !important;
      box-shadow:0 5px 14px rgba(22,163,74,.2); transform:translateY(-1px);
    }
    [data-testid="stFileUploader"] {background:#e4f7ea;border:2px dashed #50ae70;border-radius:16px;padding:12px;}
    [data-testid="stAlert"] {border-radius:12px;}
    [data-testid="stProgressBar"] > div > div {background:linear-gradient(90deg,#16a34a,#62cf86) !important;}
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {border-color:#b6dfc2 !important;border-radius:10px;}
    [data-testid="stVerticalBlockBorderWrapper"] {background:rgba(231,247,235,.72);border-color:#c7e6ce !important;border-radius:16px;}
    hr {border-color:#cde6d2 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

LANGUAGES = {
    "English": "en",
    "ಕನ್ನಡ (Kannada)": "kn",
    "हिन्दी (Hindi)": "hi",
    "తెలుగు (Telugu)": "te",
    "தமிழ் (Tamil)": "ta",
    "मराठी (Marathi)": "mr",
}

TEXT = {
    "English": {
        "tagline": "Smarter decisions for healthier crops",
        "welcome": "Welcome to your crop health dashboard",
        "dashboard": "Dashboard",
        "detect": "Disease Detection",
        "assistant": "Crop Health Assistant",
        "about": "About AgroSense-X",
        "choose_crop": "Choose crop",
        "upload": "Upload a clear, well-lit leaf photograph",
        "analyze": "Analyze image",
        "analyzing": "Analyzing leaf image...",
        "result": "Prediction Result",
        "crop": "Crop",
        "disease": "Predicted disease/class",
        "confidence": "Model confidence",
        "understand": "Understand Your Result",
        "feedback": "Was this prediction correct?",
        "correct": "Correct",
        "incorrect": "Incorrect",
        "unsure": "Unsure",
        "submit_feedback": "Submit feedback",
        "feedback_saved": "Thank you. Your feedback has been recorded for this session.",
        "chat_title": "Ask the Crop Health Assistant",
        "question": "Type your question in your selected language",
        "send": "Send",
        "no_image": "Upload a leaf image to continue.",
        "warning": "AI predictions are experimental and can be wrong. Confirm important results with a qualified agricultural expert before treatment.",
        "about_text": "AgroSense-X helps farmers review crop-leaf images and access general educational guidance. It is not a substitute for a confirmed diagnosis.",
        "symptoms": "Common symptoms",
        "prevention": "Prevention",
        "treatment": "Management guidance",
        "actions": "What you can do now",
        "alternatives": "Alternative predictions",
        "not_found": "No matching entry was found in the local knowledge base. Verify the diagnosis before deciding on treatment.",
        "chat_error": "The assistant could not answer right now. Please try again.",
    },
    "ಕನ್ನಡ (Kannada)": {
        "tagline": "ಆರೋಗ್ಯಕರ ಬೆಳೆಗಳಿಗೆ ಉತ್ತಮ ನಿರ್ಧಾರಗಳು",
        "welcome": "ನಿಮ್ಮ ಬೆಳೆ ಆರೋಗ್ಯ ಫಲಕಕ್ಕೆ ಸ್ವಾಗತ",
        "dashboard": "ಮುಖ್ಯ ಫಲಕ",
        "detect": "ರೋಗ ಪತ್ತೆ",
        "assistant": "ಬೆಳೆ ಆರೋಗ್ಯ ಸಹಾಯಕ",
        "about": "AgroSense-X ಬಗ್ಗೆ",
        "choose_crop": "ಬೆಳೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "upload": "ಎಲೆಯ ಸ್ಪಷ್ಟವಾದ, ಉತ್ತಮ ಬೆಳಕಿನ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "analyze": "ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        "analyzing": "ಎಲೆಯ ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...",
        "result": "ಭವಿಷ್ಯವಾಣಿ ಫಲಿತಾಂಶ",
        "crop": "ಬೆಳೆ",
        "disease": "ಊಹಿಸಿದ ರೋಗ/ವರ್ಗ",
        "confidence": "ಮಾದರಿಯ ವಿಶ್ವಾಸ ಮಟ್ಟ",
        "understand": "ಫಲಿತಾಂಶವನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಿ",
        "feedback": "ಈ ಫಲಿತಾಂಶ ಸರಿಯೇ?",
        "correct": "ಸರಿ",
        "incorrect": "ತಪ್ಪು",
        "unsure": "ಖಚಿತವಿಲ್ಲ",
        "submit_feedback": "ಪ್ರತಿಕ್ರಿಯೆ ಸಲ್ಲಿಸಿ",
        "feedback_saved": "ಧನ್ಯವಾದಗಳು. ನಿಮ್ಮ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ಈ ಸೆಷನ್‌ನಲ್ಲಿ ದಾಖಲಿಸಲಾಗಿದೆ.",
        "chat_title": "ಬೆಳೆ ಆರೋಗ್ಯ ಸಹಾಯಕರನ್ನು ಕೇಳಿ",
        "question": "ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಪ್ರಶ್ನೆ ಟೈಪ್ ಮಾಡಿ",
        "send": "ಕಳುಹಿಸಿ",
        "no_image": "ಮುಂದುವರಿಯಲು ಎಲೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
        "warning": "AI ಫಲಿತಾಂಶ ತಪ್ಪಾಗಿರಬಹುದು. ಚಿಕಿತ್ಸೆಗೂ ಮೊದಲು ಕೃಷಿ ತಜ್ಞರಿಂದ ದೃಢೀಕರಿಸಿ.",
        "about_text": "AgroSense-X ಬೆಳೆ ಎಲೆಗಳ ಚಿತ್ರಗಳನ್ನು ಪರಿಶೀಲಿಸಲು ಮತ್ತು ಸಾಮಾನ್ಯ ಮಾರ್ಗದರ್ಶನ ಪಡೆಯಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ.",
        "symptoms": "ಸಾಮಾನ್ಯ ಲಕ್ಷಣಗಳು",
        "prevention": "ತಡೆಗಟ್ಟುವಿಕೆ",
        "treatment": "ನಿರ್ವಹಣಾ ಮಾರ್ಗದರ್ಶನ",
        "actions": "ಈಗ ನೀವು ಮಾಡಬಹುದಾದದ್ದು",
        "alternatives": "ಇತರೆ ಸಾಧ್ಯತೆಗಳು",
        "not_found": "ಸ್ಥಳೀಯ ಜ್ಞಾನಕೋಶದಲ್ಲಿ ಹೊಂದಾಣಿಕೆಯ ಮಾಹಿತಿ ಸಿಗಲಿಲ್ಲ. ಚಿಕಿತ್ಸೆಗೆ ಮೊದಲು ರೋಗವನ್ನು ದೃಢೀಕರಿಸಿ.",
        "chat_error": "ಸಹಾಯಕ ಈಗ ಉತ್ತರಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
    },
    "हिन्दी (Hindi)": {
        "tagline": "स्वस्थ फसलों के लिए बेहतर निर्णय",
        "welcome": "आपके फसल स्वास्थ्य डैशबोर्ड में स्वागत है",
        "dashboard": "डैशबोर्ड",
        "detect": "रोग पहचान",
        "assistant": "फसल स्वास्थ्य सहायक",
        "about": "AgroSense-X के बारे में",
        "choose_crop": "फसल चुनें",
        "upload": "पत्ती की साफ़ और अच्छी रोशनी वाली तस्वीर अपलोड करें",
        "analyze": "तस्वीर का विश्लेषण करें",
        "analyzing": "पत्ती की तस्वीर का विश्लेषण हो रहा है...",
        "result": "अनुमान का परिणाम",
        "crop": "फसल",
        "disease": "अनुमानित रोग/वर्ग",
        "confidence": "मॉडल का विश्वास स्तर",
        "understand": "अपने परिणाम को समझें",
        "feedback": "क्या यह अनुमान सही था?",
        "correct": "सही",
        "incorrect": "गलत",
        "unsure": "निश्चित नहीं",
        "submit_feedback": "प्रतिक्रिया भेजें",
        "feedback_saved": "धन्यवाद। आपकी प्रतिक्रिया इस सत्र के लिए दर्ज की गई है।",
        "chat_title": "फसल स्वास्थ्य सहायक से पूछें",
        "question": "अपनी चुनी हुई भाषा में प्रश्न लिखें",
        "send": "भेजें",
        "no_image": "आगे बढ़ने के लिए पत्ती की तस्वीर अपलोड करें।",
        "warning": "AI अनुमान गलत हो सकता है। उपचार से पहले कृषि विशेषज्ञ से पुष्टि करें।",
        "about_text": "AgroSense-X पत्ती की तस्वीरों की समीक्षा और सामान्य शैक्षिक मार्गदर्शन में मदद करता है।",
        "symptoms": "सामान्य लक्षण",
        "prevention": "बचाव",
        "treatment": "प्रबंधन संबंधी सलाह",
        "actions": "अभी आप क्या कर सकते हैं",
        "alternatives": "अन्य संभावित अनुमान",
        "not_found": "स्थानीय ज्ञान आधार में मेल खाती जानकारी नहीं मिली। उपचार से पहले रोग की पुष्टि करें।",
        "chat_error": "सहायक अभी उत्तर नहीं दे सका। कृपया फिर कोशिश करें।",
    },
    "తెలుగు (Telugu)": {
        "tagline": "ఆరోగ్యకరమైన పంటల కోసం మెరుగైన నిర్ణయాలు",
        "welcome": "మీ పంట ఆరోగ్య డ్యాష్‌బోర్డ్‌కు స్వాగతం",
        "dashboard": "డ్యాష్‌బోర్డ్",
        "detect": "వ్యాధి గుర్తింపు",
        "assistant": "పంట ఆరోగ్య సహాయకుడు",
        "about": "AgroSense-X గురించి",
        "choose_crop": "పంటను ఎంచుకోండి",
        "upload": "ఆకుకు సంబంధించిన స్పష్టమైన, మంచి వెలుతురు ఉన్న ఫోటోను అప్‌లోడ్ చేయండి",
        "analyze": "చిత్రాన్ని విశ్లేషించండి",
        "analyzing": "ఆకు చిత్రాన్ని విశ్లేషిస్తోంది...",
        "result": "అంచనా ఫలితం",
        "crop": "పంట",
        "disease": "అంచనా వేసిన వ్యాధి/వర్గం",
        "confidence": "మోడల్ విశ్వాస స్థాయి",
        "understand": "ఫలితాన్ని అర్థం చేసుకోండి",
        "feedback": "ఈ అంచనా సరైనదా?",
        "correct": "సరైనది",
        "incorrect": "తప్పు",
        "unsure": "నిశ్చయం లేదు",
        "submit_feedback": "అభిప్రాయాన్ని పంపండి",
        "feedback_saved": "ధన్యవాదాలు. ఈ సెషన్‌లో మీ అభిప్రాయం నమోదు చేయబడింది.",
        "chat_title": "పంట ఆరోగ్య సహాయకుడిని అడగండి",
        "question": "మీ భాషలో ప్రశ్న టైప్ చేయండి",
        "send": "పంపండి",
        "no_image": "కొనసాగించడానికి ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి.",
        "warning": "AI అంచనా తప్పు కావచ్చు. చికిత్సకు ముందు వ్యవసాయ నిపుణుడితో నిర్ధారించండి.",
        "about_text": "AgroSense-X పంట ఆకు చిత్రాలను పరిశీలించడానికి, సాధారణ విద్యా మార్గదర్శకాన్ని అందించడానికి సహాయపడుతుంది.",
        "symptoms": "సాధారణ లక్షణాలు",
        "prevention": "నివారణ",
        "treatment": "నిర్వహణ సూచనలు",
        "actions": "ఇప్పుడు మీరు చేయగలిగేవి",
        "alternatives": "ఇతర అంచనాలు",
        "not_found": "స్థానిక జ్ఞాన ఆధారంలో సరిపోలే సమాచారం లేదు. చికిత్సకు ముందు నిర్ధారించండి.",
        "chat_error": "సహాయకుడు ప్రస్తుతం సమాధానం ఇవ్వలేకపోయాడు. మళ్లీ ప్రయత్నించండి.",
    },
    "தமிழ் (Tamil)": {
        "tagline": "ஆரோக்கியமான பயிர்களுக்கு சிறந்த முடிவுகள்",
        "welcome": "உங்கள் பயிர் நல முகப்புப் பலகைக்கு வரவேற்கிறோம்",
        "dashboard": "முகப்புப் பலகை",
        "detect": "நோய் கண்டறிதல்",
        "assistant": "பயிர் நல உதவியாளர்",
        "about": "AgroSense-X பற்றி",
        "choose_crop": "பயிரைத் தேர்ந்தெடுக்கவும்",
        "upload": "தெளிவான, நல்ல வெளிச்சமுள்ள இலைப் படத்தைப் பதிவேற்றவும்",
        "analyze": "படத்தை ஆய்வு செய்க",
        "analyzing": "இலைப் படம் ஆய்வு செய்யப்படுகிறது...",
        "result": "கணிப்பு முடிவு",
        "crop": "பயிர்",
        "disease": "கணிக்கப்பட்ட நோய்/வகை",
        "confidence": "மாதிரியின் நம்பிக்கை அளவு",
        "understand": "முடிவைப் புரிந்துகொள்ளுங்கள்",
        "feedback": "இந்தக் கணிப்பு சரியானதா?",
        "correct": "சரி",
        "incorrect": "தவறு",
        "unsure": "தெரியவில்லை",
        "submit_feedback": "கருத்தைச் சமர்ப்பிக்கவும்",
        "feedback_saved": "நன்றி. இந்த அமர்வில் உங்கள் கருத்து பதிவு செய்யப்பட்டது.",
        "chat_title": "பயிர் நல உதவியாளரிடம் கேளுங்கள்",
        "question": "உங்கள் மொழியில் கேள்வியைத் தட்டச்சு செய்யவும்",
        "send": "அனுப்பு",
        "no_image": "தொடர இலைப் படத்தைப் பதிவேற்றவும்.",
        "warning": "AI கணிப்பு தவறாக இருக்கலாம். சிகிச்சைக்கு முன் வேளாண் நிபுணரிடம் உறுதிப்படுத்தவும்.",
        "about_text": "AgroSense-X இலைப் படங்களை மதிப்பாய்வு செய்து பொதுவான கல்வி வழிகாட்டுதலை வழங்க உதவுகிறது.",
        "symptoms": "பொதுவான அறிகுறிகள்",
        "prevention": "தடுப்பு",
        "treatment": "மேலாண்மை வழிகாட்டுதல்",
        "actions": "இப்போது நீங்கள் செய்யக்கூடியவை",
        "alternatives": "மாற்றுக் கணிப்புகள்",
        "not_found": "உள்ளூர் அறிவுத் தரவுத்தளத்தில் பொருத்தமான தகவல் இல்லை. சிகிச்சைக்கு முன் உறுதிப்படுத்தவும்.",
        "chat_error": "உதவியாளர் இப்போது பதிலளிக்க முடியவில்லை. மீண்டும் முயற்சிக்கவும்.",
    },
    "मराठी (Marathi)": {
        "tagline": "निरोगी पिकांसाठी अधिक चांगले निर्णय",
        "welcome": "आपल्या पीक आरोग्य मुख्य पटलावर स्वागत आहे",
        "dashboard": "मुख्य पटल",
        "detect": "रोग ओळख",
        "assistant": "पीक आरोग्य सहाय्यक",
        "about": "AgroSense-X बद्दल",
        "choose_crop": "पीक निवडा",
        "upload": "पानाचा स्पष्ट आणि चांगल्या प्रकाशातील फोटो अपलोड करा",
        "analyze": "प्रतिमेचे विश्लेषण करा",
        "analyzing": "पानाच्या प्रतिमेचे विश्लेषण सुरू आहे...",
        "result": "अंदाजाचा निकाल",
        "crop": "पीक",
        "disease": "अंदाजित रोग/वर्ग",
        "confidence": "मॉडेलचा विश्वास स्तर",
        "understand": "निकाल समजून घ्या",
        "feedback": "हा अंदाज बरोबर होता का?",
        "correct": "बरोबर",
        "incorrect": "चुकीचा",
        "unsure": "खात्री नाही",
        "submit_feedback": "अभिप्राय पाठवा",
        "feedback_saved": "धन्यवाद. या सत्रासाठी तुमचा अभिप्राय नोंदवला आहे.",
        "chat_title": "पीक आरोग्य सहाय्यकाला विचारा",
        "question": "तुमच्या निवडलेल्या भाषेत प्रश्न लिहा",
        "send": "पाठवा",
        "no_image": "पुढे जाण्यासाठी पानाचा फोटो अपलोड करा.",
        "warning": "AI चा अंदाज चुकीचा असू शकतो. उपचारापूर्वी कृषी तज्ज्ञांकडून खात्री करा.",
        "about_text": "AgroSense-X पानांच्या प्रतिमांचे परीक्षण आणि सामान्य शैक्षणिक मार्गदर्शन करण्यात मदत करते.",
        "symptoms": "सामान्य लक्षणे",
        "prevention": "प्रतिबंध",
        "treatment": "व्यवस्थापन मार्गदर्शन",
        "actions": "आता तुम्ही काय करू शकता",
        "alternatives": "पर्यायी अंदाज",
        "not_found": "स्थानिक ज्ञानसंग्रहात जुळणारी माहिती मिळाली नाही. उपचारापूर्वी निदानाची खात्री करा.",
        "chat_error": "सहाय्यक सध्या उत्तर देऊ शकत नाही. कृपया पुन्हा प्रयत्न करा.",
    },
}

# Local account storage. Passwords are salted PBKDF2 hashes, never stored in plain text.
AUTH_DB = BASE_DIR / "agrosense_users.db"

def init_auth_db():
    with sqlite3.connect(AUTH_DB) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY COLLATE NOCASE, full_name TEXT NOT NULL, salt BLOB NOT NULL, password_hash BLOB NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")

def password_digest(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 310000)

def create_user(username: str, full_name: str, password: str):
    username = username.strip()
    full_name = full_name.strip()
    if len(username) < 3 or not username.replace("_", "").replace(".", "").isalnum():
        return False, "Username must be at least 3 characters and use letters, numbers, dots or underscores."
    if not full_name:
        return False, "Please enter your name."
    if len(password) < 8:
        return False, "Use a password with at least 8 characters."
    salt = secrets.token_bytes(16)
    digest = password_digest(password, salt)
    try:
        with sqlite3.connect(AUTH_DB) as conn:
            conn.execute("INSERT INTO users (username, full_name, salt, password_hash) VALUES (?, ?, ?, ?)", (username, full_name, salt, digest))
        return True, "Account created. You can now sign in."
    except sqlite3.IntegrityError:
        return False, "That username already exists. Please choose another."

def verify_user(username: str, password: str):
    with sqlite3.connect(AUTH_DB) as conn:
        row = conn.execute("SELECT full_name, salt, password_hash FROM users WHERE username = ?", (username.strip(),)).fetchone()
    if not row:
        return None
    full_name, salt, expected = row
    if hmac.compare_digest(password_digest(password, salt), expected):
        return {"username": username.strip(), "full_name": full_name}
    return None

init_auth_db()
if "user" not in st.session_state:
    st.session_state.user = None

# Selected language is retained by Streamlit between reruns.
with st.sidebar:
    st.markdown("## 🌱 AgroSense-X")
    st.caption("Smart Agriculture Companion")
    if st.session_state.user:
        st.success(f"Signed in as **{st.session_state.user['full_name']}**")
        if st.button("Sign out", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        with st.expander("🔐 Sign In", expanded=False):
            with st.form("signin_form"):
                login_username = st.text_input("Username", key="login_username")
                login_password = st.text_input("Password", type="password", key="login_password")
                signin_submit = st.form_submit_button("Sign In", use_container_width=True)
            if signin_submit:
                user = verify_user(login_username, login_password)
                if user:
                    st.session_state.user = user
                    st.success("Signed in successfully.")
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
        with st.expander("✨ Sign Up", expanded=False):
            with st.form("signup_form"):
                signup_name = st.text_input("Full name", key="signup_name")
                signup_username = st.text_input("Choose username", key="signup_username")
                signup_password = st.text_input("Create password (8+ characters)", type="password", key="signup_password")
                signup_confirm = st.text_input("Confirm password", type="password", key="signup_confirm")
                signup_submit = st.form_submit_button("Create Account", use_container_width=True)
            if signup_submit:
                if signup_password != signup_confirm:
                    st.error("Passwords do not match.")
                else:
                    ok, message = create_user(signup_username, signup_name, signup_password)
                    (st.success if ok else st.error)(message)
    language = st.selectbox("🌐 Language / ಭಾಷೆ", list(LANGUAGES.keys()), key="language")
    nav_options = [
        TEXT[language]["dashboard"],
        TEXT[language]["detect"],
        TEXT[language]["assistant"],
        "Personalized Advice",
        TEXT[language]["about"],
    ]
    # Apply dashboard navigation BEFORE instantiating the radio widget.
    # Streamlit forbids changing a widget's own session-state key after creation.
    pending_page = st.session_state.pop("pending_navigation", None)
    if pending_page in nav_options:
        st.session_state["nav_selection"] = pending_page
    if "nav_selection" not in st.session_state or st.session_state.nav_selection not in nav_options:
        st.session_state["nav_selection"] = TEXT[language]["dashboard"]
    page = st.radio(
        "Navigation",
        nav_options,
        key="nav_selection",
        label_visibility="collapsed",
    )

t = TEXT[language]
display_name = st.session_state.user["full_name"] if st.session_state.user else "Farmer"
st.markdown(
    f"""<div class="agro-hero">
      <h1>🌱 AgroSense-X</h1>
      <p>{t["tagline"]} &nbsp; • &nbsp; AI-powered crop health companion</p>
    </div>""",
    unsafe_allow_html=True,
)
if st.session_state.user:
    st.markdown(f'<div class="agro-card"><h3>👋 Welcome back, {display_name}!</h3><p>Your farm health workspace is ready.</p></div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="agro-card"><h3>👋 {t["welcome"]}</h3><p>Sign in or create an account in the sidebar to personalize your workspace.</p></div>', unsafe_allow_html=True)



from functools import lru_cache


@lru_cache(maxsize=1)
def load_leaf_model():
    """Load the Leaf / Non-Leaf model once per server process."""
    import torch
    from torch import nn
    from torchvision import models

    checkpoint_path = (
        BASE_DIR / "Results" / "Leaf_Validator"
        / "checkpoints" / "leaf_validator_best.pth"
    )

    if not checkpoint_path.is_file():
        raise RuntimeError(
            "Leaf validator checkpoint missing. Disease prediction blocked."
        )

    # Only load checkpoints created by our own training process.
    checkpoint = torch.load(
        checkpoint_path,
        map_location="cpu",
        weights_only=True
    )

    if checkpoint.get("labels") != ["Non-Leaf", "Leaf"]:
        raise RuntimeError("Unexpected Leaf Validator classes.")

    model = models.mobilenet_v3_small(weights=None)
    model.classifier[3] = nn.Linear(
        model.classifier[3].in_features, 2
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    return model


def validate_leaf_image(image_path):
    """Reject non-leaf uploads before crop and disease prediction."""
    import torch
    from PIL import Image, ImageOps
    from torchvision import transforms

    model = load_leaf_model()

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225]
        ),
    ])

    with Image.open(image_path) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        tensor = transform(image).unsqueeze(0)

    with torch.inference_mode():
        probabilities = torch.softmax(model(tensor), dim=1)[0]

    predicted = ["Non-Leaf", "Leaf"][int(probabilities.argmax())]

    if predicted != "Leaf":
        raise ValueError(
            "Non-leaf image detected. Please upload a clear plant leaf photograph."
        )

    return predicted


def validate_selected_crop(image_path, crop_key):
    """Validate crop selection without a Windows-specific subprocess."""
    from crop_validator_inference import predict

    try:
        response = predict(image_path)
    except Exception as exc:
        raise RuntimeError(
            "Crop validation unavailable. Disease prediction blocked."
        ) from exc

    predicted = response.get("predicted_crop")

    if predicted not in {"Paddy", "Potato", "Tomato", "Grape", "Other"}:
        raise RuntimeError(
            "Invalid crop validator response. Disease prediction blocked."
        )

    if predicted.lower() != crop_key:
        raise ValueError(
            f"Crop mismatch: selected {crop_key.title()}, "
            f"validator identified {predicted}. "
            "Disease prediction blocked. "
            "Check the selected crop and upload a clear leaf photo."
        )

    return response


def call_predictor(uploaded_file, crop_label):
    """Bridge Streamlit's UploadedFile to predictor.predict_image(path, crop_key)."""
    import predictor

    crop_aliases = {
        "paddy": "paddy", "rice": "paddy",
        "potato": "potato", "tomato": "tomato", "grape": "grape",
    }
    crop_key = crop_aliases.get(crop_label.strip().lower())
    if not crop_key:
        raise ValueError(f"Unsupported crop selection: {crop_label}")

    function = getattr(predictor, "predict_image", None)
    if not callable(function):
        raise RuntimeError("predict_image(image_path, crop_key) is missing from predictor.py")

    suffix = Path(getattr(uploaded_file, "name", "leaf.jpg")).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
        suffix = ".jpg"

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp.write(uploaded_file.getvalue())
            temp_path = temp.name

        # The existing predictor uses positional parameters image_path, crop_key.
        validate_leaf_image(temp_path)
        validate_selected_crop(temp_path, crop_key)
        result = function(temp_path, crop_key)
        if not isinstance(result, dict):
            raise ValueError("predict_image() did not return a dictionary.")
        return result
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass

def normalize_prediction(result, crop_label):
    disease = result.get("disease") or result.get("class_name") or result.get("predicted_class")
    confidence = result.get("confidence", result.get("confidence_score"))
    if disease is None:
        raise ValueError("Prediction result does not contain a 'disease' field.")
    try:
        confidence = float(confidence) if confidence is not None else None
        if confidence is not None and confidence > 1:
            confidence /= 100.0
    except (TypeError, ValueError):
        confidence = None
    return {
        **result,
        "crop": result.get("crop", crop_label),
        "disease": str(disease),
        "confidence": confidence,
        "top_predictions": result.get("top_predictions", []),
    }

def show_bullets(title, items):
    if items:
        st.markdown(f"**{title}**")
        for item in items:
            st.markdown(f"- {item}")

def show_explanation(prediction):
    st.subheader(t["understand"])
    try:
        from result_explainer import explain_prediction
        explanation = explain_prediction({
            "crop": prediction["crop"],
            "disease": prediction["disease"],
            "confidence": prediction.get("confidence") or 0,
        })
    except Exception:
        explanation = None

    if not isinstance(explanation, dict) or not explanation:
        st.info(t["not_found"])
        st.markdown(t["warning"])
        return

    st.markdown(f"### {explanation.get('title', t['understand'])}")
    if explanation.get("summary"):
        st.write(explanation["summary"])
    show_bullets(t["symptoms"], explanation.get("symptoms", []))
    show_bullets(t["prevention"], explanation.get("prevention", []))
    show_bullets(t["treatment"], explanation.get("treatment", []))
    show_bullets(t["actions"], explanation.get("actions", []))
    st.caption(t["warning"])

if page == t["about"]:
    st.subheader(t["about"])
    st.write(t["about_text"])
    st.info(t["warning"])

elif page == "Personalized Advice":
    st.subheader("🌿 Personalized Crop Advice")
    st.write("Choose your crop and the main concern to see general educational guidance.")
    advice_crop = st.selectbox("Choose your crop", ["Paddy", "Potato", "Tomato", "Grape"], key="advice_crop")
    concern = st.selectbox(
        "What would you like help with?",
        ["General crop care", "Leaf spots or discoloration", "Yellowing leaves", "Pest prevention", "Watering and soil care"],
        key="advice_concern",
    )
    advice = {
        "General crop care": [
            "Inspect plants regularly and compare symptoms across several leaves.",
            "Use clean tools, suitable spacing, and balanced fertilizer based on local soil guidance.",
            "Keep a record of planting dates, irrigation, weather, and any treatments used.",
        ],
        "Leaf spots or discoloration": [
            "Photograph affected leaves in good light and check whether symptoms are spreading.",
            "Avoid handling healthy plants immediately after affected plants; clean tools between plants.",
            "Confirm the cause with a local agricultural expert before applying pesticides or fungicides.",
        ],
        "Yellowing leaves": [
            "Check soil moisture and drainage; both overwatering and underwatering can stress plants.",
            "Look at whether older leaves or new leaves are affected and check for pests on leaf undersides.",
            "Avoid adding fertilizer without checking crop stage and local soil recommendations.",
        ],
        "Pest prevention": [
            "Inspect leaf undersides and new growth regularly for insects or eggs.",
            "Remove heavily affected plant material where appropriate and keep the field free of crop debris.",
            "Use locally approved integrated pest-management practices and follow product labels exactly.",
        ],
        "Watering and soil care": [
            "Water near the root zone when appropriate and avoid keeping foliage wet for long periods.",
            "Check drainage and soil moisture before irrigating; needs vary by crop, growth stage, and weather.",
            "Use soil-test-based nutrient recommendations from a trusted local agricultural service.",
        ],
    }
    st.markdown(f"### {advice_crop} · {concern}")
    for tip in advice[concern]:
        st.markdown(f"- {tip}")
    st.info("These are general suggestions, not a confirmed diagnosis. Consult a local agricultural expert for severe or spreading symptoms.")

elif page == t["assistant"]:
    st.subheader(t["chat_title"])
    st.caption("Type your question or use the microphone to speak. Voice transcription requires internet access and the optional speech package.")
    voice_text = None
    try:
        from streamlit_mic_recorder import speech_to_text
        voice_text = speech_to_text(
            language=LANGUAGES[language],
            start_prompt="🎙️ Start speaking",
            stop_prompt="⏹️ Stop recording",
            just_once=True,
            use_container_width=True,
            key="agrosense_voice_input",
        )
    except ImportError:
        # Keep text chat usable if the voice component is unavailable.
        st.caption(
            "Voice input is temporarily unavailable in this deployment. "
            "You can still type your question below."
        )
    except Exception:
        # Browser/device microphone issues should not break the assistant page.
        st.caption(
            "Voice input is not available on this browser or device right now. "
            "Please check microphone permission, or type your question below."
        )
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for item in st.session_state.chat_history:
        with st.chat_message(item["role"]):
            st.write(item["content"])

    question = st.chat_input(t["question"])
    if voice_text and str(voice_text).strip():
        question = str(voice_text).strip()
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        answer = None
        try:
            from chatbot import get_response
            answer = get_response(question, language=LANGUAGES[language])
        except Exception as exc:
            st.error(f"{t['chat_error']} ({exc})")
        if answer:
            answer = str(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.write(answer)

elif page == t["detect"]:
    st.subheader(f"🔬 {t['detect']}")
    st.write(t["upload"])
    crop = st.selectbox(t["choose_crop"], ["Paddy", "Potato", "Tomato", "Grape"])
    uploaded = st.file_uploader(
        t["upload"],
        type=["jpg", "jpeg", "png", "webp", "bmp"],
        key="leaf_upload",
    )

    if uploaded:
        col_image, col_details = st.columns([1, 1])
        with col_image:
            st.image(uploaded, caption="Uploaded leaf", use_container_width=True)
        with col_details:
            st.write(f"**{t['crop']}:** {crop}")
            st.caption("For best results, use a single leaf in focus with natural lighting.")

    if st.button(f"🔬 {t['analyze']}", type="primary", disabled=uploaded is None):
        st.session_state.pop("latest_prediction", None)
        with st.spinner(t["analyzing"]):
            try:
                raw = call_predictor(uploaded, crop)
                prediction = normalize_prediction(raw, crop)
                st.session_state.latest_prediction = prediction
                st.session_state.feedback_choice = None
            except Exception as exc:
                st.error(f"Prediction failed: {exc}")
                st.info("For a crop mismatch, select the correct crop or upload a different leaf image. If validation is unavailable, check .venv_gpu and the crop validator checkpoint.")

    prediction = st.session_state.get("latest_prediction")
    if prediction:
        st.divider()
        st.subheader(f"📋 {t['result']}")
        left, right = st.columns([1, 2])
        with left:
            if uploaded:
                st.image(uploaded, caption="Analyzed leaf", use_container_width=True)
        with right:
            st.write(f"**{t['crop']}:** {prediction['crop']}")
            st.write(f"**{t['disease']}:** {prediction['disease']}")
            confidence = prediction.get("confidence")
            if confidence is not None:
                st.metric(t["confidence"], f"{confidence * 100:.1f}%")
                st.progress(max(0.0, min(1.0, confidence)))
            if prediction.get("warning"):
                st.warning(prediction["warning"])
            if prediction.get("confidence_status") == "LOW":
                st.warning("Low model confidence. Please verify this result.")
            if prediction.get("confidence") is not None:
                st.caption("Model confidence is not the same as the probability that the diagnosis is correct.")

        alternatives = prediction.get("top_predictions", [])
        if len(alternatives) > 1:
            with st.expander(t["alternatives"]):
                for alt in alternatives:
                    score = alt.get("confidence")
                    score_text = f" — {float(score)*100:.1f}%" if score is not None else ""
                    st.write(f"- {alt.get('disease', 'Unknown')}{score_text}")

        show_explanation(prediction)

        st.divider()
        st.subheader(f"📝 {t['feedback']}")
        choice = st.radio(
            t["feedback"],
            [t["correct"], t["incorrect"], t["unsure"]],
            horizontal=True,
            label_visibility="collapsed",
            key="feedback_choice",
        )
        if st.button(t["submit_feedback"]):
            feedback_file = BASE_DIR / "feedback.csv"
            import csv
            new_file = not feedback_file.exists()
            with open(feedback_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if new_file:
                    writer.writerow(["crop", "disease", "confidence", "feedback", "language"])
                writer.writerow([
                    prediction.get("crop", ""),
                    prediction.get("disease", ""),
                    prediction.get("confidence", ""),
                    choice,
                    language,
                ])
            st.success(t["feedback_saved"])

else:
    st.subheader("🌾 Your Crop Health Dashboard")
    a,b,c = st.columns(3)
    with a:
        st.markdown('<div class="agro-card"><h3>📷 Disease Detection</h3><p>Upload a leaf image and run your trained model.</p></div>', unsafe_allow_html=True)
        if st.button("Open Disease Detection", use_container_width=True, key="dashboard_open_disease"):
            st.session_state["pending_navigation"] = t["detect"]
            st.rerun()
    with b:
        st.markdown('<div class="agro-card"><h3>🎙️ Voice Assistant</h3><p>Ask crop-care questions by typing or speaking.</p></div>', unsafe_allow_html=True)
        if st.button("Open Crop Assistant", use_container_width=True, key="dashboard_open_assistant"):
            st.session_state["pending_navigation"] = t["assistant"]
            st.rerun()
    with c:
        st.markdown('<div class="agro-card"><h3>🌿 Personalized Advice</h3><p>Get general educational guidance for crop health.</p></div>', unsafe_allow_html=True)
        if st.button("Open Personalized Advice", use_container_width=True, key="dashboard_open_advice"):
            st.session_state["pending_navigation"] = "Personalized Advice"
            st.rerun()
    st.warning(t["warning"])
