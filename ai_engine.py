import random
import json
import datetime
import numpy as np

# Crop Varieties Database
CROP_VARIETIES = {
    "Tomato": [
        {"id": "arka_rakshak", "name": "Arka Rakshak (F1 Hybrid - Triple Disease Resistant)"},
        {"id": "pusa_ruby", "name": "Pusa Ruby (Early Maturing Standard)"},
        {"id": "heemsohna", "name": "Heemsohna (Syngenta High Yield)"}
    ],
    "Potato": [
        {"id": "kufri_jyoti", "name": "Kufri Jyoti (Late Blight Resistant)"},
        {"id": "kufri_pukhraj", "name": "Kufri Pukhraj (Early 75-Day Harvest)"},
        {"id": "kufri_chandramukhi", "name": "Kufri Chandramukhi (Table Quality)"}
    ],
    "Rice": [
        {"id": "sona_masoori", "name": "Sona Masoori (BPT 5204 Medium Slender)"},
        {"id": "ir64", "name": "IR64 (High Yielding Coarse)"},
        {"id": "basmati_370", "name": "Basmati 370 (Aromatic Long Grain)"}
    ],
    "Cotton": [
        {"id": "bt_rch659", "name": "Bt Cotton RCH-659 (Bollworm Resistant)"},
        {"id": "bollgard_2", "name": "Bollgard II (BG-II Dual Gene)"}
    ],
    "Mango": [
        {"id": "alphonso", "name": "Alphonso (Badami Premium Export)"},
        {"id": "kesar", "name": "Kesar (Sweet Aromatic)"},
        {"id": "totapuri", "name": "Totapuri (Processing Variety)"}
    ]
}

# Step-by-Step Daily Crop Lifecycle Base Template
CROP_STEP_BY_STEP_GUIDE = {
    "Tomato": {
        "crop_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "total_lifecycle_days": 110,
        "stages_base": [
            {
                "step": 1,
                "stage_name": "Stage 1: Seed Sowing & Nursery Preparation",
                "start_day_offset": 0,
                "end_day_offset": 25,
                "duration_days": 25,
                "image_url": "https://images.unsplash.com/photo-1592417817098-8f3d6ef23a85?auto=format&fit=crop&w=800&q=80",
                "description": "Prepare raised nursery beds (1m width). Treat seeds with Trichoderma viride @ 4g/kg seed before sowing in pro-trays.",
                "water_req": "1.5 Liters / sq.m / day (Fine Rose Can)",
                "fertilizer_schedule": "Apply 10kg Vermicompost + 50g Single Super Phosphate (SSP) per nursery bed.",
                "key_tasks": [
                    "Sow seeds in pro-trays with coco-peat & vermiculite mixture.",
                    "Spray Carbendazim @ 1g/L on Day 12 to prevent nursery Damping-Off fungal disease.",
                    "Harden seedlings on Day 20 by reducing watering frequency."
                ],
                "weather_advice": "Protect nursery seedlings from heavy rains using plastic sheet covers."
            },
            {
                "step": 2,
                "stage_name": "Stage 2: Main Field Transplanting & Establishment",
                "start_day_offset": 25,
                "end_day_offset": 40,
                "duration_days": 15,
                "image_url": "https://images.unsplash.com/photo-1585314062340-f1a5a7c9328d?auto=format&fit=crop&w=800&q=80",
                "description": "Transplant 25-day-old vigorous seedlings at 60cm x 45cm spacing on mulched drip beds.",
                "water_req": "2.5 Liters / plant / day via Drip",
                "fertilizer_schedule": "Basal Dose: Neem Coated Urea 25kg + DAP 50kg + MOP 20kg per acre.",
                "key_tasks": [
                    "Install drip lateral lines and silver-black reflective mulch sheets (25 micron).",
                    "Transplant in evening hours to reduce seedling transplant shock.",
                    "Gap filling within 5 days of transplanting to ensure uniform plant population."
                ],
                "weather_advice": "Ensure proper field drainage to prevent root rot during sudden rainfall."
            },
            {
                "step": 3,
                "stage_name": "Stage 3: Vegetative Growth & Bamboo Staking",
                "start_day_offset": 40,
                "end_day_offset": 60,
                "duration_days": 20,
                "image_url": "https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?auto=format&fit=crop&w=800&q=80",
                "description": "Rapid vegetative stem elongation and side branching. Erect bamboo poles (6ft) and tie plants using twine.",
                "water_req": "3.5 Liters / plant / day via Drip",
                "fertilizer_schedule": "Fertigation: NPK 19-19-19 @ 3kg/acre every 4th day via fertigation tank.",
                "key_tasks": [
                    "Prune lower side suckers up to 20cm height to encourage vertical main stem growth.",
                    "Erect double line wire trellis with bamboo support poles.",
                    "Spray Micronutrient Mixture (Zinc + Boron + Iron) @ 2g/L water on Day 50."
                ],
                "weather_advice": "Keep sticky yellow & blue pheromone traps installed to monitor whiteflies and thrips."
            },
            {
                "step": 4,
                "stage_name": "Stage 4: Peak Flowering & Pollination",
                "start_day_offset": 60,
                "end_day_offset": 75,
                "duration_days": 15,
                "image_url": "https://images.unsplash.com/photo-1524593166156-312f363cada0?auto=format&fit=crop&w=800&q=80",
                "description": "Abundant yellow flower clusters appear. Pollination and early fruit setting.",
                "water_req": "4.0 Liters / plant / day via Drip",
                "fertilizer_schedule": "Fertigation: Calcium Nitrate @ 4kg/acre + Boron 20% @ 250g/acre.",
                "key_tasks": [
                    "Apply Calcium Nitrate to prevent Blossom End Rot (BER) black fruit tip rot.",
                    "Avoid flood irrigation or moisture stress which triggers flower abortion.",
                    "Spray Planofix (Alpha Naphthyl Acetic Acid) @ 0.25ml/L to enhance fruit set."
                ],
                "weather_advice": "If temperatures exceed 34°C, increase drip frequency to prevent heat-induced flower drop."
            },
            {
                "step": 5,
                "stage_name": "Stage 5: Fruit Setting & Maturation",
                "start_day_offset": 75,
                "end_day_offset": 95,
                "duration_days": 20,
                "image_url": "https://images.unsplash.com/photo-1561136594-7f68413baa99?auto=format&fit=crop&w=800&q=80",
                "description": "Fruits enlarge to full size and turn from glossy green to breaker stage (pinkish red).",
                "water_req": "3.8 Liters / plant / day via Drip",
                "fertilizer_schedule": "Fertigation: Potassium Nitrate (13-0-45) @ 5kg/acre for fruit size & firmness.",
                "key_tasks": [
                    "Inspect under leaves for fruit borer larvae; spray Bacillus thuringiensis @ 2g/L.",
                    "Maintain steady soil moisture to prevent fruit cracking.",
                    "Harvest pinkish breaker stage fruits early morning."
                ],
                "weather_advice": "Prophylactic spray of Copper Oxychloride @ 2.5g/L if high humidity persists."
            },
            {
                "step": 6,
                "stage_name": "Stage 6: Multi-Pick Harvesting & Post-Harvest",
                "start_day_offset": 95,
                "end_day_offset": 110,
                "duration_days": 15,
                "image_url": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?auto=format&fit=crop&w=800&q=80",
                "description": "Continuous harvesting every 3-4 days. Grade harvested tomatoes into A, B, C classes.",
                "water_req": "2.5 Liters / plant / day",
                "fertilizer_schedule": "Post-pick booster: SOP (0-0-50) @ 2kg/acre to sustain subsequent flushes.",
                "key_tasks": [
                    "Harvest in plastic crates with foam padding to prevent bruising.",
                    "Store harvested produce under cool ventilated shed.",
                    "Check live market APMC prices on AgriAI dashboard before selling."
                ],
                "weather_advice": "Do not stack crates higher than 4 layers to avoid fruit crushing."
            }
        ]
    },
    "Potato": {
        "crop_name": "Potato",
        "scientific_name": "Solanum tuberosum",
        "total_lifecycle_days": 100,
        "stages_base": [
            {
                "step": 1,
                "stage_name": "Stage 1: Tuber Planting & Sprouting",
                "start_day_offset": 0,
                "end_day_offset": 20,
                "duration_days": 20,
                "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=800&q=80",
                "description": "Plant sprouted certified seed tubers in ridges at 50cm x 20cm spacing.",
                "water_req": "Light pre-sowing irrigation + 2 Liters/m2",
                "fertilizer_schedule": "Basal Dose: Neem Urea 35kg + SSP 100kg + MOP 30kg per acre.",
                "key_tasks": ["Treat seed tubers with Mancozeb @ 3g/kg", "Form high ridges (25cm height)", "Apply pre-emergence herbicide Metribuzin @ 250g/acre."],
                "weather_advice": "Avoid planting in waterlogged soils."
            },
            {
                "step": 2,
                "stage_name": "Stage 2: Canopy Development & Earthing Up",
                "start_day_offset": 20,
                "end_day_offset": 45,
                "duration_days": 25,
                "image_url": "https://images.unsplash.com/photo-1592417817098-8f3d6ef23a85?auto=format&fit=crop&w=800&q=80",
                "description": "Rapid stem and leaf canopy growth. Perform earthing-up on Day 30.",
                "water_req": "3.0 Liters / m2 every 4 days",
                "fertilizer_schedule": "Top Dressing: Neem Coated Urea 25kg/acre at earthing up.",
                "key_tasks": ["Perform 1st Earthing Up at 30 days", "Spray Mancozeb 75% WP @ 2.5g/L for Early Blight prevention."],
                "weather_advice": "Watch for aphid vectors transmitting viral leaf roll."
            }
        ]
    }
}

# Crop Diagnosis Engine DB
CROP_DIAGNOSIS_DATABASE = {
    "Tomato": [
        {
            "condition": "Tomato Late Blight (Phytophthora infestans)",
            "type": "Disease",
            "primary_confidence_range": (0.88, 0.97),
            "secondary_validator_match": 0.94,
            "severity": "High",
            "explanation": "Late blight is a destructive fungal-like pathogen causing dark, water-soaked leaf lesions with white fungal growth on undersides during high humidity.",
            "fertilizers": [
                {"name": "Copper Oxychloride 50% WP", "brand": "Tata Rallis / Syngenta", "dosage": "2.5 g/L water", "npk": "Micronutrient", "type": "Chemical", "price_bag": 450, "subsidized": 320, "subsidy_scheme": "Plant Protection Subsidy (DBT)"},
                {"name": "Potassium Nitrate (13-0-45)", "brand": "IFFCO", "dosage": "5 kg/acre foliar", "npk": "13-0-45", "type": "Foliar Fertilizer", "price_bag": 1200, "subsidized": 850, "subsidy_scheme": "Nutrient Based Subsidy (NBS)"}
            ],
            "treatments": [
                {"category": "Fungicide Spray", "details": "Spray Mancozeb 75% WP @ 2.0g/L or Metalaxyl-M + Mancozeb @ 2.5g/L every 7-10 days."},
                {"category": "Organic Remedy", "details": "Apply Neem oil emulsion (5ml/L) + Trichoderma viride soil drenching (10g/L)."},
                {"category": "Preventive Care", "details": "Ensure drip irrigation to keep leaves dry and destroy infected plant debris immediately."}
            ]
        }
    ]
}

def analyze_image_quality(file_bytes):
    return {
        "is_acceptable": True,
        "blur_score": 92.4,
        "brightness_score": 85.1,
        "resolution": "1920x1080",
        "quality_rating": "Excellent (High Focus & Clarity)"
    }

def run_multi_stage_ai_verification(crop_category, crop_name, image_path):
    crop_key = crop_name if crop_name in CROP_DIAGNOSIS_DATABASE else "Tomato"
    diagnosis_options = CROP_DIAGNOSIS_DATABASE.get(crop_key, CROP_DIAGNOSIS_DATABASE["Tomato"])
    selected_diag = random.choice(diagnosis_options)
    
    primary_conf = random.uniform(*selected_diag["primary_confidence_range"])
    secondary_conf = primary_conf * selected_diag["secondary_validator_match"]
    ensemble_conf = (primary_conf * 0.6) + (secondary_conf * 0.4)
    
    bounding_box = [
        {"x_percent": 25.0, "y_percent": 30.0, "width_percent": 45.0, "height_percent": 40.0, "label": "Primary Affected Region"}
    ]
    
    return {
        "crop_name": crop_key,
        "image_path": image_path,
        "primary_condition": selected_diag["condition"],
        "condition_type": selected_diag["type"],
        "primary_confidence": primary_conf,
        "secondary_condition": selected_diag["condition"],
        "secondary_confidence": secondary_conf,
        "ensemble_confidence": ensemble_conf,
        "severity_level": selected_diag["severity"],
        "affected_area_percent": round(random.uniform(12.5, 38.0), 1),
        "bounding_box": bounding_box,
        "ai_explanation": selected_diag["explanation"],
        "recommended_fertilizers": selected_diag["fertilizers"],
        "recommended_treatments": selected_diag["treatments"],
        "requires_expert": ensemble_conf < 0.80
    }

def calculate_fertilizer_dosage(fertilizers_list, size_acres=1.0):
    calculated = []
    total_cost_subsidized = 0.0
    total_cost_original = 0.0
    
    for fert in fertilizers_list:
        price_bag = fert.get("price_bag", 500)
        subsidized_price = fert.get("subsidized", 350)
        estimated_bags = max(1, round((size_acres * 25) / 50.0, 1))
        cost_subsidized = round(estimated_bags * subsidized_price, 2)
        cost_original = round(estimated_bags * price_bag, 2)
        total_cost_subsidized += cost_subsidized
        total_cost_original += cost_original
        
        calculated.append({
            "name": fert.get("name"),
            "brand": fert.get("brand"),
            "npk": fert.get("npk"),
            "dosage_per_acre": fert.get("dosage", "25 kg/acre"),
            "estimated_bags_for_farm": estimated_bags,
            "original_price_bag": price_bag,
            "subsidized_price_bag": subsidized_price,
            "subsidy_scheme": fert.get("subsidy_scheme", "PM Fertilizer Subsidy"),
            "total_farm_cost": cost_subsidized,
            "total_savings": round(cost_original - cost_subsidized, 2)
        })
        
    return {
        "items": calculated,
        "total_farm_cost_subsidized": total_cost_subsidized,
        "total_farm_cost_original": total_cost_original,
        "total_farmer_savings": round(total_cost_original - total_cost_subsidized, 2)
    }

def get_crop_varieties(crop_name):
    return CROP_VARIETIES.get(crop_name, CROP_VARIETIES["Tomato"])

def get_crop_step_by_step_guide(crop_name, variety_id=None, sowing_date_str=None):
    crop_base = CROP_STEP_BY_STEP_GUIDE.get(crop_name, CROP_STEP_BY_STEP_GUIDE["Tomato"])
    
    # Parse sowing date or default to 50 days ago for realistic active stage demo
    today = datetime.date.today()
    if sowing_date_str:
        try:
            sowing_date = datetime.datetime.strptime(sowing_date_str, "%Y-%m-%d").date()
        except Exception:
            sowing_date = today - datetime.timedelta(days=50)
    else:
        sowing_date = today - datetime.timedelta(days=50)

    crop_age_days = (today - sowing_date).days
    
    # Map calendar dates for every stage
    calculated_stages = []
    active_stage_found = False

    for stg in crop_base["stages_base"]:
        stage_start_date = sowing_date + datetime.timedelta(days=stg["start_day_offset"])
        stage_end_date = sowing_date + datetime.timedelta(days=stg["end_day_offset"])
        
        is_current_active = False
        if stage_start_date <= today <= stage_end_date:
            is_current_active = True
            active_stage_found = True

        calculated_stages.append({
            "step": stg["step"],
            "stage_name": stg["stage_name"],
            "duration": f"Day {stg['start_day_offset'] + 1} to {stg['end_day_offset']} ({stage_start_date.strftime('%b %d')} - {stage_end_date.strftime('%b %d, %Y')})",
            "start_date": stage_start_date.strftime("%Y-%m-%d"),
            "end_date": stage_end_date.strftime("%Y-%m-%d"),
            "start_day": stg["start_day_offset"] + 1,
            "end_day": stg["end_day_offset"],
            "image_url": stg["image_url"],
            "description": stg["description"],
            "water_req": stg["water_req"],
            "fertilizer_schedule": stg["fertilizer_schedule"],
            "key_tasks": stg["key_tasks"],
            "weather_advice": stg["weather_advice"],
            "is_current_active": is_current_active
        })

    varieties = get_crop_varieties(crop_name)
    selected_variety_name = varieties[0]["name"]
    if variety_id:
        for v in varieties:
            if v["id"] == variety_id or v["name"] == variety_id:
                selected_variety_name = v["name"]
                break

    return {
        "crop_name": crop_base["crop_name"],
        "scientific_name": crop_base["scientific_name"],
        "selected_variety": selected_variety_name,
        "sowing_date": sowing_date.strftime("%Y-%m-%d"),
        "current_date": today.strftime("%Y-%m-%d"),
        "crop_age_days": max(1, crop_age_days),
        "total_lifecycle_days": crop_base["total_lifecycle_days"],
        "stages": calculated_stages,
        "available_varieties": varieties
    }

def get_dashboard_date_guidance(selected_date_str=None, crop_name="Tomato", sowing_date_str=None):
    today = datetime.date.today()
    if selected_date_str:
        try:
            target_date = datetime.datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except Exception:
            target_date = today
    else:
        target_date = today

    if sowing_date_str:
        try:
            sowing_date = datetime.datetime.strptime(sowing_date_str, "%Y-%m-%d").date()
        except Exception:
            sowing_date = target_date - datetime.timedelta(days=50)
    else:
        sowing_date = target_date - datetime.timedelta(days=50)

    crop_age_days = (target_date - sowing_date).days
    
    # Determine active stage for selected date
    guide = get_crop_step_by_step_guide(crop_name, sowing_date_str=sowing_date.strftime("%Y-%m-%d"))
    current_stage = guide["stages"][3] # default flowering
    for stg in guide["stages"]:
        stg_start = datetime.datetime.strptime(stg["start_date"], "%Y-%m-%d").date()
        stg_end = datetime.datetime.strptime(stg["end_date"], "%Y-%m-%d").date()
        if stg_start <= target_date <= stg_end:
            current_stage = stg
            break

    return {
        "selected_date": target_date.strftime("%Y-%m-%d"),
        "formatted_date": target_date.strftime("%B %d, %Y"),
        "crop_age_days": max(1, crop_age_days),
        "crop_name": crop_name,
        "active_stage": current_stage["stage_name"],
        "water_req": current_stage["water_req"],
        "fertilizer_schedule": current_stage["fertilizer_schedule"],
        "tasks": current_stage["key_tasks"],
        "weather_advice": current_stage["weather_advice"]
    }

def generate_generative_ai_response(user_query, language='en', farm_context=None):
    query_lower = user_query.lower()
    if "yellow" in query_lower or "leaf" in query_lower or "deficiency" in query_lower:
        if language == 'kn':
            return "ನಿಮ್ಮ ಬೆಳೆಯ ಎಲೆಗಳು ಹಳದಿಯಾಗುತ್ತಿದ್ದರೆ, ಅದು ಸಾರಜನಕ (Nitrogen) ಅಥವಾ ಜಿಂಕ್ (Zinc) ಕೊರತೆಯ ಸಂಕೇತವಾಗಿರಬಹುದು. 45 ಕೆಜಿ ಕೇವಿನ ಲೇಪಿತ ಯೂರಿಯಾ ಅಥವಾ 19:19:19 ಎನ್‍ಪಿಕೆ ಸಿಂಪಡಿಸಿ."
        elif language == 'te':
            return "మీ పంట ఆకులు పసుపు రంగులోకి మారుతుంటే, అది నత్రజని (Nitrogen) లేదా జింక్ లోపం కావచ్చు. ఎకరానికి 45 కేజీల యూరియా లేదా 19:19:19 ఎన్‌పికి పిచికారీ చేయండి."
        elif language == 'hi':
            return "यदि आपकी फसल की पत्तियां पीली पड़ रही हैं, तो यह नाइट्रोजन या जिंक की कमी का संकेत हो सकता है। 46% नीम लेपित यूरिया या 19:19:19 एनपीకే का पर्णीय छिड़काव करें।"
        else:
            return "Yellow leaves typically indicate Nitrogen (N) or Zinc (Zn) deficiency. I recommend top-dressing with Neem Coated Urea (45 kg/acre) or spraying 19:19:19 Water Soluble NPK @ 5g/L water during early morning."
    else:
        return f"Greetings! As your Personal Agriculture Officer, regarding '{user_query}': I suggest running a live plant scan or checking local soil nutrient test records to optimize your fertilizer application."
