"""
Action Plan Generator - Creates actionable steps for citizens
Based on eligibility check and available documents
"""
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ActionPlanGenerator:
    """Generates citizen action plans for scheme applications"""
    
    def __init__(self):
        # Document type translations for user-friendly names
        self.document_names = {
            "en": {
                "aadhaar": "Aadhaar Card",
                "pan": "PAN Card",
                "income_certificate": "Income Certificate",
                "caste_certificate": "Caste Certificate",
                "bank_passbook": "Bank Passbook",
                "photo": "Passport Size Photo",
                "domicile_certificate": "Domicile Certificate",
                "age_proof": "Age Proof",
                "land_records": "Land Records",
                "disability_certificate": "Disability Certificate",
                "ration_card": "Ration Card"
            },
            "hi": {
                "aadhaar": "आधार कार्ड",
                "pan": "पैन कार्ड",
                "income_certificate": "आय प्रमाण पत्र",
                "caste_certificate": "जाति प्रमाण पत्र",
                "bank_passbook": "बैंक पासबुक",
                "photo": "पासपोर्ट साइज फोटो",
                "domicile_certificate": "निवास प्रमाण पत्र",
                "age_proof": "आयु प्रमाण",
                "land_records": "भूमि रिकॉर्ड",
                "disability_certificate": "विकलांगता प्रमाण पत्र",
                "ration_card": "राशन कार्ड"
            },
            "te": {
                "aadhaar": "ఆధార్ కార్డ్",
                "pan": "పాన్ కార్డ్",
                "income_certificate": "ఆదాయ ధృవీకరణ పత్రం",
                "caste_certificate": "కుల ధృవీకరణ పత్రం",
                "bank_passbook": "బ్యాంక్ పాస్‌బుక్",
                "photo": "పాస్‌పోర్ట్ సైజ్ ఫోటో",
                "domicile_certificate": "నివాస ధృవీకరణ పత్రం",
                "age_proof": "వయస్సు రుజువు",
                "land_records": "భూమి రికార్డులు",
                "disability_certificate": "వైకల్య ధృవీకరణ పత్రం",
                "ration_card": "రేషన్ కార్డ్"
            },
            "ta": {
                "aadhaar": "ஆதார் அட்டை",
                "pan": "பான் அட்டை",
                "income_certificate": "வருமான சான்றிதழ்",
                "caste_certificate": "சாதி சான்றிதழ்",
                "bank_passbook": "வங்கி பாஸ்புக்",
                "photo": "பாஸ்போர்ட் அளவு புகைப்படம்",
                "domicile_certificate": "குடியிருப்பு சான்றிதழ்",
                "age_proof": "வயது ஆதாரம்",
                "land_records": "நில பதிவுகள்",
                "disability_certificate": "ஊனமுற்றோர் சான்றிதழ்",
                "ration_card": "ரேஷன் அட்டை"
            },
            "mr": {
                "aadhaar": "आधार कार्ड",
                "pan": "पॅन कार्ड",
                "income_certificate": "उत्पन्न प्रमाणपत्र",
                "caste_certificate": "जात प्रमाणपत्र",
                "bank_passbook": "बँक पासबुक",
                "photo": "पासपोर्ट आकाराचा फोटो",
                "domicile_certificate": "अधिवास प्रमाणपत्र",
                "age_proof": "वयाचा पुरावा",
                "land_records": "जमीन रेकॉर्ड",
                "disability_certificate": "अपंगत्व प्रमाणपत्र",
                "ration_card": "रेशन कार्ड"
            },
            "kn": {
                "aadhaar": "ಆಧಾರ್ ಕಾರ್ಡ್",
                "pan": "ಪ್ಯಾನ್ ಕಾರ್ಡ್",
                "income_certificate": "ಆದಾಯ ಪ್ರಮಾಣಪತ್ರ",
                "caste_certificate": "ಜಾತಿ ಪ್ರಮಾಣಪತ್ರ",
                "bank_passbook": "ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್",
                "photo": "ಪಾಸ್‌ಪೋರ್ಟ್ ಗಾತ್ರದ ಫೋಟೋ",
                "domicile_certificate": "ನಿವಾಸ ಪ್ರಮಾಣಪತ್ರ",
                "age_proof": "ವಯಸ್ಸಿನ ಪುರಾವೆ",
                "land_records": "ಭೂಮಿ ದಾಖಲೆಗಳು",
                "disability_certificate": "ಅಂಗವೈಕಲ್ಯ ಪ್ರಮಾಣಪತ್ರ",
                "ration_card": "ರೇಷನ್ ಕಾರ್ಡ್"
            }
        }
    
    def generate_action_plan(
        self,
        scheme: Dict[str, Any],
        eligibility: Dict[str, Any],
        available_documents: List[str],
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generate complete action plan for a scheme
        
        Args:
            scheme: Scheme dictionary
            eligibility: Eligibility check result
            available_documents: List of documents user has
            language: Language for multilingual content
        
        Returns:
            Action plan dictionary
        """
        scheme_id = scheme.get("scheme_id", "")
        scheme_name = scheme.get("name", {})
        required_docs = scheme.get("required_documents", [])
        
        # Determine eligibility status from score
        score = eligibility.get("score", 0)
        if score >= 80:
            status = "ELIGIBLE"
        elif score >= 60:
            status = "LIKELY_ELIGIBLE"
        elif score >= 40:
            status = "NEEDS_VERIFICATION"
        else:
            status = "NOT_ELIGIBLE"
        
        # Calculate missing documents
        missing_docs = [doc for doc in required_docs if doc not in available_documents]
        
        # Generate action steps
        steps = self._generate_steps(
            status=status,
            required_docs=required_docs,
            available_docs=available_documents,
            missing_docs=missing_docs,
            eligibility=eligibility,
            language=language
        )
        
        # Get application method
        application_method = self._get_application_method(scheme, language)
        
        # Generate notes
        notes = self._generate_notes(status, eligibility, language)
        
        return {
            "scheme_id": scheme_id,
            "scheme_name": scheme_name,
            "eligibility_status": status,
            "required_documents": required_docs,
            "available_documents": available_documents,
            "missing_documents": missing_docs,
            "next_steps": steps,
            "application_method": application_method,
            "portal_url": scheme.get("portal_url"),
            "estimated_time": self._estimate_time(missing_docs),
            "notes": notes
        }
    
    def _generate_steps(
        self,
        status: str,
        required_docs: List[str],
        available_docs: List[str],
        missing_docs: List[str],
        eligibility: Dict[str, Any],
        language: str
    ) -> List[Dict[str, Any]]:
        """Generate action steps based on eligibility status"""
        steps = []
        step_num = 1
        
        # Step templates by language
        templates = {
            "en": {
                "check_eligibility": "Review your eligibility status",
                "gather_info": "Provide missing information",
                "obtain_doc": "Obtain {doc}",
                "upload_doc": "Upload {doc}",
                "verify_info": "Verify your information",
                "submit": "Submit your application",
                "track": "Track your application status"
            },
            "hi": {
                "check_eligibility": "अपनी पात्रता की स्थिति की समीक्षा करें",
                "gather_info": "लापता जानकारी प्रदान करें",
                "obtain_doc": "{doc} प्राप्त करें",
                "upload_doc": "{doc} अपलोड करें",
                "verify_info": "अपनी जानकारी सत्यापित करें",
                "submit": "अपना आवेदन जमा करें",
                "track": "अपने आवेदन की स्थिति ट्रैक करें"
            },
            "te": {
                "check_eligibility": "మీ అర్హత స్థితిని సమీక్షించండి",
                "gather_info": "తప్పిపోయిన సమాచారాన్ని అందించండి",
                "obtain_doc": "{doc} పొందండి",
                "upload_doc": "{doc} అప్‌లోడ్ చేయండి",
                "verify_info": "మీ సమాచారాన్ని ధృవీకరించండి",
                "submit": "మీ దరఖాస్తును సమర్పించండి",
                "track": "మీ దరఖాస్తు స్థితిని ట్రాక్ చేయండి"
            },
            "ta": {
                "check_eligibility": "உங்கள் தகுதி நிலையை மதிப்பாய்வு செய்யவும்",
                "gather_info": "காணாமல் போன தகவலை வழங்கவும்",
                "obtain_doc": "{doc} பெறவும்",
                "upload_doc": "{doc} பதிவேற்றவும்",
                "verify_info": "உங்கள் தகவலை சரிபார்க்கவும்",
                "submit": "உங்கள் விண்ணப்பத்தை சமர்ப்பிக்கவும்",
                "track": "உங்கள் விண்ணப்ப நிலையை கண்காணிக்கவும்"
            },
            "mr": {
                "check_eligibility": "आपल्या पात्रतेच्या स्थितीचे पुनरावलोकन करा",
                "gather_info": "गहाळ माहिती प्रदान करा",
                "obtain_doc": "{doc} मिळवा",
                "upload_doc": "{doc} अपलोड करा",
                "verify_info": "आपली माहिती सत्यापित करा",
                "submit": "आपला अर्ज सबमिट करा",
                "track": "आपल्या अर्जाची स्थिती ट्रॅक करा"
            },
            "kn": {
                "check_eligibility": "ನಿಮ್ಮ ಅರ್ಹತೆಯ ಸ್ಥಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ",
                "gather_info": "ಕಾಣೆಯಾದ ಮಾಹಿತಿಯನ್ನು ಒದಗಿಸಿ",
                "obtain_doc": "{doc} ಪಡೆಯಿರಿ",
                "upload_doc": "{doc} ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
                "verify_info": "ನಿಮ್ಮ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ",
                "submit": "ನಿಮ್ಮ ಅರ್ಜಿಯನ್ನು ಸಲ್ಲಿಸಿ",
                "track": "ನಿಮ್ಮ ಅರ್ಜಿ ಸ್ಥಿತಿಯನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಿ"
            }
        }
        
        lang_templates = templates.get(language, templates["en"])
        
        # Step 1: Check eligibility (if needed)
        if status in ["NEEDS_VERIFICATION", "NOT_ELIGIBLE"]:
            missing_info = eligibility.get("missing_info", [])
            if missing_info:
                steps.append({
                    "step_number": step_num,
                    "action": lang_templates["gather_info"],
                    "description": ", ".join(missing_info[:3]),  # Limit to 3 items
                    "status": "REQUIRED",
                    "documents_needed": []
                })
                step_num += 1
        
        # Steps for missing documents
        doc_names = self.document_names.get(language, self.document_names["en"])
        
        for doc in missing_docs[:5]:  # Limit to 5 most important
            doc_name = doc_names.get(doc, doc)
            steps.append({
                "step_number": step_num,
                "action": lang_templates["obtain_doc"].format(doc=doc_name),
                "description": f"Required document: {doc_name}",
                "status": "REQUIRED",
                "documents_needed": [doc]
            })
            step_num += 1
        
        # Step: Upload available documents
        if available_docs:
            steps.append({
                "step_number": step_num,
                "action": lang_templates["upload_doc"].format(doc="documents"),
                "description": f"{len(available_docs)} document(s) ready to upload",
                "status": "REQUIRED",
                "documents_needed": available_docs
            })
            step_num += 1
        
        # Step: Verify information
        if status in ["ELIGIBLE", "LIKELY_ELIGIBLE"]:
            steps.append({
                "step_number": step_num,
                "action": lang_templates["verify_info"],
                "description": "Review all information before submission",
                "status": "REQUIRED",
                "documents_needed": []
            })
            step_num += 1
            
            # Step: Submit
            steps.append({
                "step_number": step_num,
                "action": lang_templates["submit"],
                "description": "Submit through government portal",
                "status": "REQUIRED",
                "documents_needed": []
            })
            step_num += 1
            
            # Step: Track
            steps.append({
                "step_number": step_num,
                "action": lang_templates["track"],
                "description": "Monitor application progress",
                "status": "OPTIONAL",
                "documents_needed": []
            })
        
        return steps
    
    def _get_application_method(
        self,
        scheme: Dict[str, Any],
        language: str
    ) -> str:
        """Get application method description"""
        methods = {
            "en": "Apply online through government portal",
            "hi": "सरकारी पोर्टल के माध्यम से ऑनलाइन आवेदन करें",
            "te": "ప్రభుత్వ పోర్టల్ ద్వారా ఆన్‌లైన్‌లో దరఖాస్తు చేసుకోండి",
            "ta": "அரசாங்க போர்ட்டல் மூலம் ஆன்லைனில் விண்ணப்பிக்கவும்",
            "mr": "सरकारी पोर्टलद्वारे ऑनलाइन अर्ज करा",
            "kn": "ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್ ಮೂಲಕ ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಅನ್ವಯಿಸಿ"
        }
        
        return methods.get(language, methods["en"])
    
    def _estimate_time(
        self,
        missing_docs: List[str]
    ) -> str:
        """Estimate time to complete application"""
        if not missing_docs:
            return "1-2 days"
        elif len(missing_docs) <= 2:
            return "1-2 weeks"
        else:
            return "2-4 weeks"
    
    def _generate_notes(
        self,
        status: str,
        eligibility: Dict[str, Any],
        language: str
    ) -> List[str]:
        """Generate helpful notes"""
        notes = []
        
        note_templates = {
            "en": {
                "eligible": "You meet the eligibility criteria for this scheme.",
                "likely": "You likely meet the criteria, but some verification is needed.",
                "verification": "Please provide missing information to check your eligibility.",
                "not_eligible": "Based on current information, you may not be eligible for this scheme."
            },
            "hi": {
                "eligible": "आप इस योजना के लिए पात्रता मानदंडों को पूरा करते हैं।",
                "likely": "आप संभवतः मानदंडों को पूरा करते हैं, लेकिन कुछ सत्यापन की आवश्यकता है।",
                "verification": "अपनी पात्रता जांचने के लिए कृपया लापता जानकारी प्रदान करें।",
                "not_eligible": "वर्तमान जानकारी के आधार पर, आप इस योजना के लिए पात्र नहीं हो सकते हैं।"
            },
            "te": {
                "eligible": "మీరు ఈ పథకానికి అర్హత ప్రమాణాలను తీర్చారు.",
                "likely": "మీరు ప్రమాణాలను తీర్చే అవకాశం ఉంది, కానీ కొంత ధృవీకరణ అవసరం.",
                "verification": "మీ అర్హతను తనిఖీ చేయడానికి దయచేసి తప్పిపోయిన సమాచారాన్ని అందించండి.",
                "not_eligible": "ప్రస్తుత సమాచారం ఆధారంగా, మీరు ఈ పథకానికి అర్హులు కాకపోవచ్చు."
            },
            "ta": {
                "eligible": "இந்த திட்டத்திற்கான தகுதி நிபந்தனைகளை நீங்கள் பூர்த்தி செய்கிறீர்கள்.",
                "likely": "நீங்கள் நிபந்தனைகளை பூர்த்தி செய்ய வாய்ப்புள்ளது, ஆனால் சில சரிபார்ப்பு தேவை.",
                "verification": "உங்கள் தகுதியை சரிபார்க்க காணாமல் போன தகவலை வழங்கவும்.",
                "not_eligible": "தற்போதைய தகவலின் அடிப்படையில், இந்த திட்டத்திற்கு நீங்கள் தகுதியற்றவராக இருக்கலாம்."
            },
            "mr": {
                "eligible": "तुम्ही या योजनेसाठी पात्रता निकष पूर्ण करता.",
                "likely": "तुम्ही निकष पूर्ण करण्याची शक्यता आहे, परंतु काही पडताळणी आवश्यक आहे.",
                "verification": "तुमची पात्रता तपासण्यासाठी कृपया गहाळ माहिती प्रदान करा.",
                "not_eligible": "सध्याच्या माहितीच्या आधारे, तुम्ही या योजनेसाठी पात्र नसू शकता."
            },
            "kn": {
                "eligible": "ಈ ಯೋಜನೆಗೆ ಅರ್ಹತಾ ಮಾನದಂಡಗಳನ್ನು ನೀವು ಪೂರೈಸುತ್ತೀರಿ.",
                "likely": "ನೀವು ಮಾನದಂಡಗಳನ್ನು ಪೂರೈಸುವ ಸಾಧ್ಯತೆಯಿದೆ, ಆದರೆ ಕೆಲವು ಪರಿಶೀಲನೆ ಅಗತ್ಯವಿದೆ.",
                "verification": "ನಿಮ್ಮ ಅರ್ಹತೆಯನ್ನು ಪರಿಶೀಲಿಸಲು ದಯವಿಟ್ಟು ಕಾಣೆಯಾದ ಮಾಹಿತಿಯನ್ನು ಒದಗಿಸಿ.",
                "not_eligible": "ಪ್ರಸ್ತುತ ಮಾಹಿತಿಯ ಆಧಾರದ ಮೇಲೆ, ನೀವು ಈ ಯೋಜನೆಗೆ ಅರ್ಹರಾಗಿರದಿರಬಹುದು."
            }
        }
        
        lang_notes = note_templates.get(language, note_templates["en"])
        
        if status == "ELIGIBLE":
            notes.append(lang_notes["eligible"])
        elif status == "LIKELY_ELIGIBLE":
            notes.append(lang_notes["likely"])
        elif status == "NEEDS_VERIFICATION":
            notes.append(lang_notes["verification"])
        else:
            notes.append(lang_notes["not_eligible"])
        
        return notes
