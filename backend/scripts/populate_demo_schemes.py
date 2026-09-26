"""
Populate Demo Scheme Data for PS6 Hackathon
Telugu Farmer Scenario + General Demo Schemes
"""
import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import boto3
from shared.utils import get_dynamodb_resource, get_table_name


def populate_demo_schemes():
    """Populate demo scheme data in DynamoDB"""
    
    dynamodb = get_dynamodb_resource()
    schemes_table = dynamodb.Table(get_table_name("schemes"))
    
    demo_schemes = [
        # Telugu Farmer Scheme - Primary demo scenario
        {
            "scheme_id": "DEMO-TS-RYTHU-BANDHU-001",
            "name": {
                "en": "Rythu Bandhu - Farmer Investment Support",
                "hi": "रायथु बंधु - किसान निवेश सहायता",
                "te": "రైతు బంధు - రైతు పెట్టుబడి మద్దతు",
                "ta": "ரைத்து பந்து - விவசாயி முதலீட்டு ஆதரவு",
                "mr": "रायथु बंधू - शेतकरी गुंतवणूक समर्थन",
                "kn": "ರೈತು ಬಂಧು - ರೈತ ಹೂಡಿಕೆ ಬೆಂಬಲ"
            },
            "description": {
                "en": "Financial assistance to farmers for agricultural investment support (DEMO DATA - For Hackathon Testing Only)",
                "hi": "कृषि निवेश सहायता के लिए किसानों को वित्तीय सहायता (डेमो डेटा - केवल हैकथॉन परीक्षण के लिए)",
                "te": "వ్యవసాయ పెట్టుబడి మద్దతు కోసం రైతులకు ఆర్థిక సహాయం (డెమో డేటా - హ్యాకథాన్ పరీక్ష కోసం మాత్రమే)",
                "ta": "விவசாய முதலீட்டு ஆதரவுக்கான விவசாயிகளுக்கு நிதி உதவி (டெமோ தரவு - ஹேக்கத்தான் சோதனைக்கு மட்டும்)",
                "mr": "शेती गुंतवणूक समर्थनासाठी शेतकऱ्यांना आर्थिक सहाय्य (डेमो डेटा - केवळ हॅकथॉन चाचणीसाठी)",
                "kn": "ಕೃಷಿ ಹೂಡಿಕೆ ಬೆಂಬಲಕ್ಕಾಗಿ ರೈತರಿಗೆ ಹಣಕಾಸಿನ ಸಹಾಯ (ಡೆಮೋ ಡೇಟಾ - ಹ್ಯಾಕಥಾನ್ ಪರೀಕ್ಷೆಗೆ ಮಾತ್ರ)"
            },
            "state": "TS",
            "category": "agriculture",
            "eligibility_criteria": {
                "min_age": 18,
                "max_age": 70,
                "gender": ["ALL"],
                "income_limit": 500000,
                "categories": ["ALL"],
                "states": ["TS"],
                "custom_rules": [
                    {
                        "field": "is_farmer",
                        "operator": "eq",
                        "value": True
                    },
                    {
                        "field": "has_land",
                        "operator": "eq",
                        "value": True
                    }
                ]
            },
            "benefits": {
                "en": "₹10,000 per acre per season for investment support. Direct benefit transfer to bank account.",
                "hi": "निवेश सहायता के लिए प्रति एकड़ प्रति सीजन ₹10,000। बैंक खाते में सीधा लाभ हस्तांतरण।",
                "te": "పెట్టుబడి మద్దతు కోసం ఎకరాకు సీజన్‌కు ₹10,000. బ్యాంకు ఖాతాకు ప్రత్యక్ష ప్రయోజన బదిలీ.",
                "ta": "முதலீட்டு ஆதரவுக்காக ஏக்கருக்கு பருவத்திற்கு ₹10,000. வங்கி கணக்கிற்கு நேரடி நன்மை பரிமாற்றம்.",
                "mr": "गुंतवणूक समर्थनासाठी प्रति एकर प्रति हंगाम ₹10,000. बँक खात्यात थेट लाभ हस्तांतरण.",
                "kn": "ಹೂಡಿಕೆ ಬೆಂಬಲಕ್ಕಾಗಿ ಎಕರೆಗೆ ಋತುವಿಗೆ ₹10,000. ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ನೇರ ಲಾಭ ವರ್ಗಾವಣೆ."
            },
            "application_process": {
                "en": [
                    "Visit official government portal",
                    "Register with Aadhaar",
                    "Upload land records",
                    "Submit bank account details",
                    "Receive confirmation SMS"
                ],
                "hi": [
                    "आधिकारिक सरकारी पोर्टल पर जाएं",
                    "आधार से पंजीकरण करें",
                    "भूमि रिकॉर्ड अपलोड करें",
                    "बैंक खाता विवरण जमा करें",
                    "पुष्टिकरण SMS प्राप्त करें"
                ],
                "te": [
                    "అధికారిక ప్రభుత్వ పోర్టల్‌ను సందర్శించండి",
                    "ఆధార్‌తో నమోదు చేసుకోండి",
                    "భూమి రికార్డులను అప్‌లోడ్ చేయండి",
                    "బ్యాంకు ఖాతా వివరాలను సమర్పించండి",
                    "నిర్ధారణ SMS స్వీకరించండి"
                ],
                "ta": [
                    "அதிகாரப்பூர்வ அரசாங்க போர்ட்டலைப் பார்வையிடவும்",
                    "ஆதாருடன் பதிவு செய்யவும்",
                    "நில பதிவுகளைப் பதிவேற்றவும்",
                    "வங்கி கணக்கு விவரங்களைச் சமர்ப்பிக்கவும்",
                    "உறுதிப்படுத்தல் SMS பெறவும்"
                ],
                "mr": [
                    "अधिकृत सरकारी पोर्टलला भेट द्या",
                    "आधारसह नोंदणी करा",
                    "जमीन रेकॉर्ड अपलोड करा",
                    "बँक खाते तपशील सबमिट करा",
                    "पुष्टीकरण SMS प्राप्त करा"
                ],
                "kn": [
                    "ಅಧಿಕೃತ ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್ ಅನ್ನು ಭೇಟಿ ಮಾಡಿ",
                    "ಆಧಾರ್‌ನೊಂದಿಗೆ ನೋಂದಾಯಿಸಿ",
                    "ಭೂಮಿ ದಾಖಲೆಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
                    "ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳನ್ನು ಸಲ್ಲಿಸಿ",
                    "ದೃಢೀಕರಣ SMS ಸ್ವೀಕರಿಸಿ"
                ]
            },
            "required_documents": [
                "aadhaar",
                "land_records",
                "bank_passbook"
            ],
            "portal_url": "https://demo-rythu-bandhu.telangana.gov.in",
            "portal_status": "ACTIVE",
            "last_synced_at": datetime.utcnow().isoformat(),
            "is_active": True,
            "view_count": 0,
            "demo_data": True
        },
        
        # PM-KISAN - All India Farmer Scheme
        {
            "scheme_id": "DEMO-ALL-PM-KISAN-001",
            "name": {
                "en": "PM-KISAN - Pradhan Mantri Kisan Samman Nidhi",
                "hi": "पीएम-किसान - प्रधानमंत्री किसान सम्मान निधि",
                "te": "పీఎం-కిసాన్ - ప్రధాన మంత్రి కిసాన్ సమ్మాన్ నిధి",
                "ta": "பிஎம்-கிசான் - பிரதமர் கிசான் சம்மான் நிதி",
                "mr": "पीएम-किसान - प्रधानमंत्री किसान सम्मान निधी",
                "kn": "ಪಿಎಂ-ಕಿಸಾನ್ - ಪ್ರಧಾನ ಮಂತ್ರಿ ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿ"
            },
            "description": {
                "en": "Central government income support for small and marginal farmers (DEMO DATA)",
                "hi": "छोटे और सीमांत किसानों के लिए केंद्र सरकार की आय सहायता (डेमो डेटा)",
                "te": "చిన్న మరియు సీమాంత రైతులకు కేంద్ర ప్రభుత్వ ఆదాయ మద్దతు (డెమో డేటా)",
                "ta": "சிறு மற்றும் விளிம்புநிலை விவசாயிகளுக்கான மத்திய அரசு வருமான ஆதரவு (டெமோ தரவு)",
                "mr": "लहान आणि सीमांत शेतकऱ्यांसाठी केंद्र सरकारची उत्पन्न समर्थन (डेमो डेटा)",
                "kn": "ಸಣ್ಣ ಮತ್ತು ಮರ್ಜಿನಲ್ ರೈತರಿಗೆ ಕೇಂದ್ರ ಸರ್ಕಾರದ ಆದಾಯ ಬೆಂಬಲ (ಡೆಮೋ ಡೇಟಾ)"
            },
            "state": "ALL_INDIA",
            "category": "agriculture",
            "eligibility_criteria": {
                "min_age": 18,
                "max_age": None,
                "gender": ["ALL"],
                "income_limit": None,
                "categories": ["ALL"],
                "states": ["ALL_INDIA"],
                "custom_rules": []
            },
            "benefits": {
                "en": "₹6,000 per year in three equal installments directly to bank account",
                "hi": "बैंक खाते में सीधे तीन समान किस्तों में प्रति वर्ष ₹6,000",
                "te": "బ్యాంకు ఖాతాకు నేరుగా మూడు సమాన వాయిదాలలో సంవత్సరానికి ₹6,000",
                "ta": "வங்கி கணக்கில் நேரடியாக மூன்று சம தவணைகளில் ஆண்டுக்கு ₹6,000",
                "mr": "बँक खात्यात थेट तीन समान हप्त्यांमध्ये दरवर्षी ₹6,000",
                "kn": "ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ನೇರವಾಗಿ ಮೂರು ಸಮಾನ ಕಂತುಗಳಲ್ಲಿ ವರ್ಷಕ್ಕೆ ₹6,000"
            },
            "application_process": {
                "en": ["Register on PM-KISAN portal", "Link Aadhaar", "Submit land records", "Verify bank account"],
                "hi": ["पीएम-किसान पोर्टल पर पंजीकरण करें", "आधार लिंक करें", "भूमि रिकॉर्ड जमा करें", "बैंक खाता सत्यापित करें"],
                "te": ["పీఎం-కిసాన్ పోర్టల్‌లో నమోదు చేసుకోండి", "ఆధార్ లింక్ చేయండి", "భూమి రికార్డులను సమర్పించండి", "బ్యాంకు ఖాతాను ధృవీకరించండి"],
                "ta": ["பிஎம்-கிசான் போர்ட்டலில் பதிவு செய்யவும்", "ஆதாரை இணைக்கவும்", "நில பதிவுகளைச் சமர்ப்பிக்கவும்", "வங்கி கணக்கைச் சரிபார்க்கவும்"],
                "mr": ["पीएम-किसान पोर्टलवर नोंदणी करा", "आधार लिंक करा", "जमीन रेकॉर्ड सबमिट करा", "बँक खाते सत्यापित करा"],
                "kn": ["ಪಿಎಂ-ಕಿಸಾನ್ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನೋಂದಾಯಿಸಿ", "ಆಧಾರ್ ಲಿಂಕ್ ಮಾಡಿ", "ಭೂಮಿ ದಾಖಲೆಗಳನ್ನು ಸಲ್ಲಿಸಿ", "ಬ್ಯಾಂಕ್ ಖಾತೆಯನ್ನು ಪರಿಶೀಲಿಸಿ"]
            },
            "required_documents": ["aadhaar", "land_records", "bank_passbook"],
            "portal_url": "https://pmkisan.gov.in",
            "portal_status": "ACTIVE",
            "last_synced_at": datetime.utcnow().isoformat(),
            "is_active": True,
            "view_count": 0,
            "demo_data": True
        },
        
        # Education Scholarship - For students
        {
            "scheme_id": "DEMO-ALL-NSP-SCHOLARSHIP-001",
            "name": {
                "en": "National Scholarship Portal - Merit Scholarship",
                "hi": "राष्ट्रीय छात्रवृत्ति पोर्टल - मेरिट छात्रवृत्ति",
                "te": "నేషనల్ స్కాలర్‌షిప్ పోర్టల్ - మెరిట్ స్కాలర్‌షిప్",
                "ta": "தேசிய புலமைப்பரிசில் போர்ட்டல் - மெரிட் புலமைப்பரிசில்",
                "mr": "राष्ट्रीय शिष्यवृत्ती पोर्टल - मेरिट शिष्यवृत्ती",
                "kn": "ರಾಷ್ಟ್ರೀಯ ವಿದ್ಯಾರ್ಥಿವೇತನ ಪೋರ್ಟಲ್ - ಮೆರಿಟ್ ವಿದ್ಯಾರ್ಥಿವೇತನ"
            },
            "description": {
                "en": "Merit-based scholarship for higher education students (DEMO DATA)",
                "hi": "उच्च शिक्षा छात्रों के लिए मेरिट-आधारित छात्रवृत्ति (डेमो डेटा)",
                "te": "ఉన్నత విద్యా విద్యార్థులకు మెరిట్ ఆధారిత స్కాలర్‌షిప్ (డెమో డేటా)",
                "ta": "உயர் கல்வி மாணவர்களுக்கான தகுதி அடிப்படையிலான புலமைப்பரிசில் (டெமோ தரவு)",
                "mr": "उच्च शिक्षण विद्यार्थ्यांसाठी मेरिट-आधारित शिष्यवृत्ती (डेमो डेटा)",
                "kn": "ಉನ್ನತ ಶಿಕ್ಷಣ ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಮೆರಿಟ್-ಆಧಾರಿತ ವಿದ್ಯಾರ್ಥಿವೇತನ (ಡೆಮೋ ಡೇಟಾ)"
            },
            "state": "ALL_INDIA",
            "category": "education",
            "eligibility_criteria": {
                "min_age": 17,
                "max_age": 30,
                "gender": ["ALL"],
                "income_limit": 800000,
                "categories": ["ALL"],
                "states": ["ALL_INDIA"],
                "custom_rules": []
            },
            "benefits": {
                "en": "₹12,000 to ₹50,000 per year based on course and merit",
                "hi": "पाठ्यक्रम और योग्यता के आधार पर प्रति वर्ष ₹12,000 से ₹50,000",
                "te": "కోర్సు మరియు మెరిట్ ఆధారంగా సంవత్సరానికి ₹12,000 నుండి ₹50,000",
                "ta": "பாடநெறி மற்றும் தகுதியின் அடிப்படையில் ஆண்டுக்கு ₹12,000 முதல் ₹50,000",
                "mr": "अभ्यासक्रम आणि मेरिटच्या आधारावर दरवर्षी ₹12,000 ते ₹50,000",
                "kn": "ಕೋರ್ಸ್ ಮತ್ತು ಮೆರಿಟ್ ಆಧಾರದ ಮೇಲೆ ವರ್ಷಕ್ಕೆ ₹12,000 ರಿಂದ ₹50,000"
            },
            "application_process": {
                "en": ["Register on NSP portal", "Upload academic certificates", "Submit income certificate", "Wait for approval"],
                "hi": ["एनएसपी पोर्टल पर पंजीकरण करें", "शैक्षणिक प्रमाणपत्र अपलोड करें", "आय प्रमाणपत्र जमा करें", "अनुमोदन की प्रतीक्षा करें"],
                "te": ["ఎన్‌ఎస్‌పి పోర్టల్‌లో నమోదు చేసుకోండి", "విద్యా ప్రమాణపత్రాలను అప్‌లోడ్ చేయండి", "ఆదాయ ధృవీకరణ పత్రం సమర్పించండి", "ఆమోదం కోసం వేచి ఉండండి"],
                "ta": ["என்எஸ்பி போர்ட்டலில் பதிவு செய்யவும்", "கல்வி சான்றிதழ்களை பதிவேற்றவும்", "வருமான சான்றிதழை சமர்ப்பிக்கவும்", "அங்கீகாரத்திற்காக காத்திருக்கவும்"],
                "mr": ["एनएसपी पोर्टलवर नोंदणी करा", "शैक्षणिक प्रमाणपत्रे अपलोड करा", "उत्पन्न प्रमाणपत्र सबमिट करा", "मंजुरीची प्रतीक्षा करा"],
                "kn": ["ಎನ್‌ಎಸ್‌ಪಿ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನೋಂದಾಯಿಸಿ", "ಶೈಕ್ಷಣಿಕ ಪ್ರಮಾಣಪತ್ರಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ", "ಆದಾಯ ಪ್ರಮಾಣಪತ್ರವನ್ನು ಸಲ್ಲಿಸಿ", "ಅನುಮೋದನೆಗಾಗಿ ಕಾಯಿರಿ"]
            },
            "required_documents": ["aadhaar", "income_certificate", "photo", "age_proof"],
            "portal_url": "https://scholarships.gov.in",
            "portal_status": "ACTIVE",
            "last_synced_at": datetime.utcnow().isoformat(),
            "is_active": True,
            "view_count": 0,
            "demo_data": True
        }
    ]
    
    # Insert demo schemes
    for scheme in demo_schemes:
        try:
            schemes_table.put_item(Item=scheme)
            print(f"✓ Inserted demo scheme: {scheme['scheme_id']} - {scheme['name']['en']}")
        except Exception as e:
            print(f"✗ Error inserting scheme {scheme['scheme_id']}: {e}")
    
    print(f"\n✓ Demo scheme population complete! Added {len(demo_schemes)} schemes.")
    print("\nNote: All schemes are clearly marked with 'DEMO DATA' disclaimer.")


if __name__ == "__main__":
    print("Voice for Bharat - Demo Scheme Data Population")
    print("=" * 60)
    print("\nThis script populates DEMO/TEST scheme data for hackathon demonstration.")
    print("All data is clearly labeled as demo data and not official government information.\n")
    
    try:
        populate_demo_schemes()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
