
"""
AgroSense-X multilingual language resources.
Version 1.0: English, Kannada, Hindi, Telugu, Tamil, Marathi.
"""

LANGUAGES = {
    "English": "en",
    "ಕನ್ನಡ (Kannada)": "kn",
    "हिन्दी (Hindi)": "hi",
    "తెలుగు (Telugu)": "te",
    "தமிழ் (Tamil)": "ta",
    "मराठी (Marathi)": "mr",
}

TRANSLATIONS = {
    "en": {
        "app_title": "AgroSense-X",
        "tagline": "Plant Disease Detection & Intelligence",
        "language": "Choose language",
        "dashboard": "Dashboard",
        "detection": "Disease Detection",
        "assistant": "Crop Health Assistant",
        "about": "About",
        "welcome": "Welcome to your crop health dashboard",
        "welcome_text": (
            "Upload a leaf image for a model prediction, or ask "
            "the agricultural assistant about crop diseases."
        ),
        "supported_crops": "Supported crops",
        "knowledge_entries": "Knowledge entries",
        "prediction_models": "Prediction models",
        "select_crop": "Select crop",
        "upload_image": "Upload a leaf image",
        "analyze": "Analyze Leaf",
        "prediction_result": "Prediction result",
        "predicted_class": "Predicted disease",
        "confidence": "Model confidence",
        "symptoms": "Symptoms",
        "prevention": "Prevention",
        "treatment": "Treatment guidance",
        "ask_placeholder": "Ask a question about crop health...",
        "clear_chat": "Clear conversation",
        "greeting": (
            "Hello! I'm the AgroSense-X agricultural assistant. "
            "Ask me about disease symptoms, prevention, or management."
        ),
        "unknown_disease": (
            "I couldn't find that disease in the current knowledge base. "
            "Try the disease name shown by the model."
        ),
        "uncertain": (
            "The prediction is uncertain. Try a clearer image and "
            "confirm the result with an agricultural expert."
        ),
        "disclaimer": (
            "This is educational decision support, not a confirmed diagnosis. "
            "Follow local agricultural recommendations and product labels."
        ),
        "about_text": (
            "AgroSense-X combines crop image prediction with agricultural "
            "knowledge to support plant health decisions."
        ),
        "ask_about_result": "Ask the assistant about this result",
        "open_detection": "Open Disease Detection",
        "open_assistant": "Open Crop Health Assistant",
        "goodbye": "Goodbye! Take care of your crops.",
        "general_prevention": (
            "Inspect crops regularly, use healthy planting material, "
            "maintain balanced nutrition, and manage infected plant debris."
        ),
    },

    "kn": {
        "app_title": "ಅಗ್ರೋಸೆನ್ಸ್-X",
        "tagline": "ಸಸ್ಯ ರೋಗ ಪತ್ತೆ ಮತ್ತು ಮಾಹಿತಿ",
        "language": "ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "dashboard": "ಮುಖ್ಯ ಫಲಕ",
        "detection": "ರೋಗ ಪತ್ತೆ",
        "assistant": "ಬೆಳೆ ಆರೋಗ್ಯ ಸಹಾಯಕ",
        "about": "ನಮ್ಮ ಬಗ್ಗೆ",
        "welcome": "ನಿಮ್ಮ ಬೆಳೆ ಆರೋಗ್ಯ ಫಲಕಕ್ಕೆ ಸ್ವಾಗತ",
        "welcome_text": (
            "ಎಲೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ರೋಗದ ಮುನ್ಸೂಚನೆ ಪಡೆಯಿರಿ "
            "ಅಥವಾ ಬೆಳೆ ರೋಗಗಳ ಬಗ್ಗೆ ಸಹಾಯಕರನ್ನು ಕೇಳಿ."
        ),
        "supported_crops": "ಬೆಂಬಲಿತ ಬೆಳೆಗಳು",
        "knowledge_entries": "ಜ್ಞಾನ ಮಾಹಿತಿಗಳು",
        "prediction_models": "ಮುನ್ಸೂಚನೆ ಮಾದರಿಗಳು",
        "select_crop": "ಬೆಳೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "upload_image": "ಎಲೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "analyze": "ಎಲೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        "prediction_result": "ಮುನ್ಸೂಚನೆಯ ಫಲಿತಾಂಶ",
        "predicted_class": "ಅಂದಾಜಿಸಿದ ರೋಗ",
        "confidence": "ಮಾದರಿಯ ವಿಶ್ವಾಸ ಮಟ್ಟ",
        "symptoms": "ಲಕ್ಷಣಗಳು",
        "prevention": "ತಡೆಗಟ್ಟುವಿಕೆ",
        "treatment": "ನಿರ್ವಹಣಾ ಸಲಹೆ",
        "ask_placeholder": "ಬೆಳೆ ಆರೋಗ್ಯದ ಬಗ್ಗೆ ಪ್ರಶ್ನಿಸಿ...",
        "clear_chat": "ಸಂಭಾಷಣೆಯನ್ನು ತೆರವುಗೊಳಿಸಿ",
        "greeting": (
            "ನಮಸ್ಕಾರ! ನಾನು ಅಗ್ರೋಸೆನ್ಸ್-X ಬೆಳೆ ಆರೋಗ್ಯ ಸಹಾಯಕ. "
            "ರೋಗದ ಲಕ್ಷಣಗಳು, ತಡೆಗಟ್ಟುವಿಕೆ ಅಥವಾ ನಿರ್ವಹಣೆಯ ಬಗ್ಗೆ ಕೇಳಿ."
        ),
        "unknown_disease": (
            "ಈ ರೋಗದ ಮಾಹಿತಿ ಪ್ರಸ್ತುತ ಜ್ಞಾನ ಸಂಗ್ರಹದಲ್ಲಿ ಲಭ್ಯವಿಲ್ಲ. "
            "ಮಾದರಿಯಲ್ಲಿ ತೋರಿಸಿರುವ ರೋಗದ ಹೆಸರನ್ನು ಬಳಸಿ."
        ),
        "uncertain": (
            "ರೋಗದ ಮುನ್ಸೂಚನೆ ಖಚಿತವಾಗಿಲ್ಲ. ಸ್ಪಷ್ಟವಾದ ಚಿತ್ರವನ್ನು ಬಳಸಿ "
            "ಮತ್ತು ಕೃಷಿ ತಜ್ಞರಿಂದ ದೃಢೀಕರಿಸಿ."
        ),
        "disclaimer": (
            "ಇದು ಮಾಹಿತಿ ಆಧಾರಿತ ಸಹಾಯ ಮಾತ್ರ; ಖಚಿತ ರೋಗನಿರ್ಣಯವಲ್ಲ. "
            "ಸ್ಥಳೀಯ ಕೃಷಿ ಸಲಹೆ ಮತ್ತು ಉತ್ಪನ್ನದ ಸೂಚನೆಗಳನ್ನು ಪಾಲಿಸಿ."
        ),
        "about_text": (
            "ಅಗ್ರೋಸೆನ್ಸ್-X ಸಸ್ಯದ ಚಿತ್ರ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಕೃಷಿ ಮಾಹಿತಿಯನ್ನು "
            "ಒಟ್ಟುಗೂಡಿಸಿ ಬೆಳೆ ಆರೋಗ್ಯ ನಿರ್ಧಾರಗಳಿಗೆ ಸಹಾಯ ಮಾಡುತ್ತದೆ."
        ),
        "ask_about_result": "ಈ ಫಲಿತಾಂಶದ ಬಗ್ಗೆ ಸಹಾಯಕರನ್ನು ಕೇಳಿ",
        "open_detection": "ರೋಗ ಪತ್ತೆ ತೆರೆಯಿರಿ",
        "open_assistant": "ಬೆಳೆ ಆರೋಗ್ಯ ಸಹಾಯಕ ತೆರೆಯಿರಿ",
        "goodbye": "ವಿದಾಯ! ನಿಮ್ಮ ಬೆಳೆಗಳನ್ನು ಚೆನ್ನಾಗಿ ನೋಡಿಕೊಳ್ಳಿ.",
        "general_prevention": (
            "ಬೆಳೆಗಳನ್ನು ನಿಯಮಿತವಾಗಿ ಪರಿಶೀಲಿಸಿ, ಆರೋಗ್ಯಕರ ಬೀಜ ಬಳಸಿ, "
            "ಸಮತೋಲಿತ ಪೋಷಕಾಂಶ ನೀಡಿ ಮತ್ತು ಸೋಂಕಿತ ಅವಶೇಷಗಳನ್ನು ನಿರ್ವಹಿಸಿ."
        ),
    },

    "hi": {
        "app_title": "एग्रोसेंस-X",
        "tagline": "पौधों के रोग की पहचान और जानकारी",
        "language": "भाषा चुनें",
        "dashboard": "डैशबोर्ड",
        "detection": "रोग पहचान",
        "assistant": "फसल स्वास्थ्य सहायक",
        "about": "हमारे बारे में",
        "welcome": "आपके फसल स्वास्थ्य डैशबोर्ड में स्वागत है",
        "welcome_text": (
            "रोग का अनुमान पाने के लिए पत्ती की तस्वीर अपलोड करें "
            "या फसल रोगों के बारे में सहायक से पूछें।"
        ),
        "supported_crops": "समर्थित फसलें",
        "knowledge_entries": "ज्ञान प्रविष्टियाँ",
        "prediction_models": "पूर्वानुमान मॉडल",
        "select_crop": "फसल चुनें",
        "upload_image": "पत्ती की तस्वीर अपलोड करें",
        "analyze": "पत्ती का विश्लेषण करें",
        "prediction_result": "पूर्वानुमान परिणाम",
        "predicted_class": "अनुमानित रोग",
        "confidence": "मॉडल का विश्वास स्तर",
        "symptoms": "लक्षण",
        "prevention": "रोकथाम",
        "treatment": "प्रबंधन संबंधी सलाह",
        "ask_placeholder": "फसल स्वास्थ्य के बारे में पूछें...",
        "clear_chat": "बातचीत साफ़ करें",
        "greeting": (
            "नमस्ते! मैं एग्रोसेंस-X कृषि सहायक हूँ। "
            "रोग के लक्षण, रोकथाम या प्रबंधन के बारे में पूछें।"
        ),
        "unknown_disease": (
            "इस रोग की जानकारी वर्तमान ज्ञान संग्रह में नहीं मिली। "
            "मॉडल में दिखाए गए रोग का नाम लिखकर देखें।"
        ),
        "uncertain": (
            "पूर्वानुमान निश्चित नहीं है। अधिक स्पष्ट तस्वीर लें "
            "और कृषि विशेषज्ञ से पुष्टि करें।"
        ),
        "disclaimer": (
            "यह शैक्षिक सहायता है, निश्चित रोग निदान नहीं। "
            "स्थानीय कृषि सलाह और उत्पाद के निर्देशों का पालन करें।"
        ),
        "about_text": (
            "एग्रोसेंस-X पौधों की तस्वीरों के विश्लेषण और कृषि जानकारी "
            "को जोड़कर फसल स्वास्थ्य संबंधी निर्णयों में सहायता करता है।"
        ),
        "ask_about_result": "इस परिणाम के बारे में सहायक से पूछें",
        "open_detection": "रोग पहचान खोलें",
        "open_assistant": "फसल स्वास्थ्य सहायक खोलें",
        "goodbye": "अलविदा! अपनी फसलों का ध्यान रखें।",
        "general_prevention": (
            "फसलों की नियमित जाँच करें, स्वस्थ बीज या रोपण सामग्री का "
            "उपयोग करें, संतुलित पोषण दें और संक्रमित अवशेषों का प्रबंधन करें।"
        ),
    },

    "te": {
        "app_title": "అగ్రోసెన్స్-X",
        "tagline": "మొక్కల వ్యాధుల గుర్తింపు మరియు సమాచారం",
        "language": "భాషను ఎంచుకోండి",
        "dashboard": "డ్యాష్‌బోర్డ్",
        "detection": "వ్యాధి గుర్తింపు",
        "assistant": "పంట ఆరోగ్య సహాయకుడు",
        "about": "మా గురించి",
        "welcome": "మీ పంట ఆరోగ్య డ్యాష్‌బోర్డ్‌కు స్వాగతం",
        "welcome_text": (
            "వ్యాధి అంచనా కోసం ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి "
            "లేదా పంట వ్యాధుల గురించి సహాయకుడిని అడగండి."
        ),
        "supported_crops": "మద్దతు ఉన్న పంటలు",
        "knowledge_entries": "జ్ఞాన అంశాలు",
        "prediction_models": "అంచనా నమూనాలు",
        "select_crop": "పంటను ఎంచుకోండి",
        "upload_image": "ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి",
        "analyze": "ఆకును విశ్లేషించండి",
        "prediction_result": "అంచనా ఫలితం",
        "predicted_class": "అంచనా వేసిన వ్యాధి",
        "confidence": "మోడల్ విశ్వాస స్థాయి",
        "symptoms": "లక్షణాలు",
        "prevention": "నివారణ",
        "treatment": "నిర్వహణ సూచనలు",
        "ask_placeholder": "పంట ఆరోగ్యం గురించి అడగండి...",
        "clear_chat": "సంభాషణను తొలగించండి",
        "greeting": (
            "నమస్కారం! నేను అగ్రోసెన్స్-X పంట ఆరోగ్య సహాయకుడిని. "
            "వ్యాధి లక్షణాలు, నివారణ లేదా నిర్వహణ గురించి అడగండి."
        ),
        "unknown_disease": (
            "ఈ వ్యాధి సమాచారం ప్రస్తుత జ్ఞాన సేకరణలో లేదు. "
            "మోడల్ చూపించిన వ్యాధి పేరుతో ప్రయత్నించండి."
        ),
        "uncertain": (
            "వ్యాధి అంచనా నిర్ధారితంగా లేదు. స్పష్టమైన చిత్రాన్ని "
            "ఉపయోగించి వ్యవసాయ నిపుణుడితో నిర్ధారించండి."
        ),
        "disclaimer": (
            "ఇది విద్యాపరమైన సహాయం మాత్రమే; నిర్ధారిత వ్యాధి నిర్ధారణ కాదు. "
            "స్థానిక వ్యవసాయ సలహాలు, ఉత్పత్తి సూచనలు పాటించండి."
        ),
        "about_text": (
            "అగ్రోసెన్స్-X మొక్కల చిత్ర విశ్లేషణను వ్యవసాయ సమాచారంతో "
            "కలిపి పంట ఆరోగ్య నిర్ణయాలకు సహాయపడుతుంది."
        ),
        "ask_about_result": "ఈ ఫలితం గురించి సహాయకుడిని అడగండి",
        "open_detection": "వ్యాధి గుర్తింపును తెరవండి",
        "open_assistant": "పంట ఆరోగ్య సహాయకుడిని తెరవండి",
        "goodbye": "వీడ్కోలు! మీ పంటలను జాగ్రత్తగా చూసుకోండి.",
        "general_prevention": (
            "పంటలను క్రమం తప్పకుండా పరిశీలించండి, ఆరోగ్యకరమైన విత్తనాలు "
            "వాడండి, సమతుల్య పోషణ అందించండి, సోకిన అవశేషాలను నిర్వహించండి."
        ),
    },

    "ta": {
        "app_title": "அக்ரோசென்ஸ்-X",
        "tagline": "தாவர நோய் கண்டறிதல் மற்றும் தகவல்",
        "language": "மொழியைத் தேர்ந்தெடுக்கவும்",
        "dashboard": "முகப்புப் பலகை",
        "detection": "நோய் கண்டறிதல்",
        "assistant": "பயிர் நல உதவியாளர்",
        "about": "எங்களைப் பற்றி",
        "welcome": "உங்கள் பயிர் நல முகப்புப் பலகைக்கு வரவேற்கிறோம்",
        "welcome_text": (
            "நோய் கணிப்பிற்காக இலைப் படத்தைப் பதிவேற்றவும் அல்லது "
            "பயிர் நோய்கள் குறித்து உதவியாளரிடம் கேட்கவும்."
        ),
        "supported_crops": "ஆதரிக்கப்படும் பயிர்கள்",
        "knowledge_entries": "அறிவுத் தகவல்கள்",
        "prediction_models": "கணிப்பு மாதிரிகள்",
        "select_crop": "பயிரைத் தேர்ந்தெடுக்கவும்",
        "upload_image": "இலைப் படத்தைப் பதிவேற்றவும்",
        "analyze": "இலையைப் பகுப்பாய்வு செய்யவும்",
        "prediction_result": "கணிப்பு முடிவு",
        "predicted_class": "கணிக்கப்பட்ட நோய்",
        "confidence": "மாதிரியின் நம்பிக்கை அளவு",
        "symptoms": "அறிகுறிகள்",
        "prevention": "தடுப்பு",
        "treatment": "மேலாண்மை வழிகாட்டுதல்",
        "ask_placeholder": "பயிர் நலம் குறித்து கேளுங்கள்...",
        "clear_chat": "உரையாடலை அழிக்கவும்",
        "greeting": (
            "வணக்கம்! நான் அக்ரோசென்ஸ்-X பயிர் நல உதவியாளர். "
            "நோய் அறிகுறிகள், தடுப்பு அல்லது மேலாண்மை குறித்து கேளுங்கள்."
        ),
        "unknown_disease": (
            "இந்த நோய் பற்றிய தகவல் தற்போதைய அறிவுத் தொகுப்பில் இல்லை. "
            "மாதிரியில் காட்டப்பட்ட நோயின் பெயரை முயற்சிக்கவும்."
        ),
        "uncertain": (
            "கணிப்பு உறுதியானதல்ல. தெளிவான படத்தைப் பயன்படுத்தி "
            "வேளாண் நிபுணரிடம் உறுதிப்படுத்தவும்."
        ),
        "disclaimer": (
            "இது கல்வி நோக்கத்திற்கான உதவி மட்டுமே; உறுதியான நோய் கண்டறிதல் அல்ல. "
            "உள்ளூர் வேளாண் ஆலோசனைகளையும் தயாரிப்பு வழிமுறைகளையும் பின்பற்றவும்."
        ),
        "about_text": (
            "அக்ரோசென்ஸ்-X தாவரப் படப் பகுப்பாய்வையும் வேளாண் தகவல்களையும் "
            "இணைத்து பயிர் நல முடிவுகளுக்கு உதவுகிறது."
        ),
        "ask_about_result": "இந்த முடிவைப் பற்றி உதவியாளரிடம் கேளுங்கள்",
        "open_detection": "நோய் கண்டறிதலைத் திறக்கவும்",
        "open_assistant": "பயிர் நல உதவியாளரைத் திறக்கவும்",
        "goodbye": "விடைபெறுகிறேன்! உங்கள் பயிர்களைப் பராமரிக்கவும்.",
        "general_prevention": (
            "பயிர்களைத் தொடர்ந்து ஆய்வு செய்யவும், ஆரோக்கியமான விதைகளைப் "
            "பயன்படுத்தவும், சமநிலையான ஊட்டச்சத்து வழங்கவும், பாதிக்கப்பட்ட "
            "தாவரக் கழிவுகளை முறையாக நிர்வகிக்கவும்."
        ),
    },

    "mr": {
        "app_title": "अ‍ॅग्रोसेन्स-X",
        "tagline": "वनस्पती रोग ओळख आणि माहिती",
        "language": "भाषा निवडा",
        "dashboard": "मुख्य पटल",
        "detection": "रोग ओळख",
        "assistant": "पीक आरोग्य सहाय्यक",
        "about": "आमच्याबद्दल",
        "welcome": "आपल्या पीक आरोग्य मुख्य पटलावर स्वागत आहे",
        "welcome_text": (
            "रोगाचा अंदाज मिळवण्यासाठी पानाचा फोटो अपलोड करा "
            "किंवा पीक रोगांबद्दल सहाय्यकाला विचारा."
        ),
        "supported_crops": "समर्थित पिके",
        "knowledge_entries": "ज्ञान नोंदी",
        "prediction_models": "अंदाज मॉडेल",
        "select_crop": "पीक निवडा",
        "upload_image": "पानाचा फोटो अपलोड करा",
        "analyze": "पानाचे विश्लेषण करा",
        "prediction_result": "अंदाजाचा निकाल",
        "predicted_class": "अंदाजित रोग",
        "confidence": "मॉडेलचा विश्वास स्तर",
        "symptoms": "लक्षणे",
        "prevention": "प्रतिबंध",
        "treatment": "व्यवस्थापन मार्गदर्शन",
        "ask_placeholder": "पीक आरोग्याबद्दल प्रश्न विचारा...",
        "clear_chat": "संभाषण साफ करा",
        "greeting": (
            "नमस्कार! मी अ‍ॅग्रोसेन्स-X पीक आरोग्य सहाय्यक आहे. "
            "रोगाची लक्षणे, प्रतिबंध किंवा व्यवस्थापनाबद्दल विचारा."
        ),
        "unknown_disease": (
            "या रोगाची माहिती सध्याच्या ज्ञानसंग्रहात नाही. "
            "मॉडेलमध्ये दाखवलेले रोगाचे नाव वापरून पाहा."
        ),
        "uncertain": (
            "रोगाचा अंदाज निश्चित नाही. अधिक स्पष्ट फोटो वापरा "
            "आणि कृषी तज्ज्ञांकडून खात्री करून घ्या."
        ),
        "disclaimer": (
            "ही शैक्षणिक मदत आहे; निश्चित रोगनिदान नाही. "
            "स्थानिक कृषी सल्ला आणि उत्पादनाच्या सूचनांचे पालन करा."
        ),
        "about_text": (
            "अ‍ॅग्रोसेन्स-X वनस्पतींच्या प्रतिमांचे विश्लेषण आणि कृषी माहिती "
            "एकत्र करून पीक आरोग्यविषयक निर्णयांना मदत करते."
        ),
        "ask_about_result": "या निकालाबद्दल सहाय्यकाला विचारा",
        "open_detection": "रोग ओळख उघडा",
        "open_assistant": "पीक आरोग्य सहाय्यक उघडा",
        "goodbye": "निरोप! आपल्या पिकांची काळजी घ्या.",
        "general_prevention": (
            "पिकांची नियमित तपासणी करा, निरोगी बियाणे वापरा, संतुलित "
            "पोषण द्या आणि संक्रमित अवशेषांचे योग्य व्यवस्थापन करा."
        ),
    },
}


def translate(key, language="en"):
    """Return a translated string, falling back safely to English."""
    language = language if language in TRANSLATIONS else "en"
    return TRANSLATIONS[language].get(
        key,
        TRANSLATIONS["en"].get(key, key),
    )


def get_language_code(language_name):
    """Get a language code from its display name."""
    return LANGUAGES.get(language_name, "en")