import os
import json
import random
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from models import db, Farmer, Farm, DiagnosisRecord, FertilizerMaster, Dealer, AgriExpert, FarmLogbook
import ai_engine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'agri_ai_secret_key_capstone_2026_x99'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agri_ai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
    return Farmer.query.get(int(user_id))

def init_db_with_schema_safety():
    with app.app_context():
        try:
            db.create_all()
            Farmer.query.first()
        except Exception as e:
            print("DB Schema updated, recreating tables:", e)
            db.drop_all()
            db.create_all()
            
        seed_initial_database_content()

def seed_initial_database_content():
    if FertilizerMaster.query.count() == 0:
        fertilizers = [
            FertilizerMaster(
                name="Neem Coated Urea (46% N)", category="Chemical", brand="IFFCO", npk_ratio="46-0-0",
                target_deficiency="Nitrogen", original_price_per_bag=550.0, subsidized_price_per_bag=266.5,
                subsidy_scheme="PM Subsidized Urea Scheme (DBT)", dosage_per_acre_kg=45.0,
                application_method="Basal & Split Top Dressing", best_application_time="Early morning after irrigation",
                recovery_time_days=5, safety_precautions="Wear protective gloves and dust mask during broadcast.",
                image_url="https://images.unsplash.com/photo-1585314062340-f1a5a7c9328d?auto=format&fit=crop&w=600&q=80"
            ),
            FertilizerMaster(
                name="Di-Ammonium Phosphate (DAP 18-46-0)", category="Chemical", brand="Coromandel Gromor", npk_ratio="18-46-0",
                target_deficiency="Phosphorus & Nitrogen", original_price_per_bag=2400.0, subsidized_price_per_bag=1350.0,
                subsidy_scheme="Nutrient Based Subsidy (NBS)", dosage_per_acre_kg=50.0,
                application_method="Soil placement near root zone during sowing", best_application_time="At time of land preparation",
                recovery_time_days=7, safety_precautions="Do not mix directly with zinc sulphate.",
                image_url="https://images.unsplash.com/photo-1628352081506-83c43123ed6d?auto=format&fit=crop&w=600&q=80"
            ),
            FertilizerMaster(
                name="Muriate of Potash (MOP 60% K2O)", category="Chemical", brand="IPL Indian Potash", npk_ratio="0-0-60",
                target_deficiency="Potassium", original_price_per_bag=2100.0, subsidized_price_per_bag=1700.0,
                subsidy_scheme="NBS Potash Subsidy", dosage_per_acre_kg=30.0,
                application_method="Soil application during panicle/flowering stage", best_application_time="Late afternoon",
                recovery_time_days=6, safety_precautions="Keep store area dry away from direct moisture.",
                image_url="https://images.unsplash.com/photo-1592417817098-8f3d6ef23a85?auto=format&fit=crop&w=600&q=80"
            ),
            FertilizerMaster(
                name="Water Soluble NPK 19-19-19", category="Foliar Fertilizer", brand="Mahadhan / Nagarjuna", npk_ratio="19-19-19",
                target_deficiency="All (General Growth)", original_price_per_bag=1500.0, subsidized_price_per_bag=950.0,
                subsidy_scheme="Subsidized Micro-Fertilizers Scheme", dosage_per_acre_kg=5.0,
                application_method="Foliar spray @ 5g/L water or drip fertigation", best_application_time="Early morning spray",
                recovery_time_days=4, safety_precautions="Avoid spraying under harsh hot direct sunlight.",
                image_url="https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=600&q=80"
            ),
            FertilizerMaster(
                name="Organic Vermicompost", category="Organic", brand="State Agriculture Organic", npk_ratio="1.5-1.0-1.5",
                target_deficiency="Soil Organic Carbon", original_price_per_bag=500.0, subsidized_price_per_bag=250.0,
                subsidy_scheme="Paramparagat Krishi Vikas Yojana (PKVY)", dosage_per_acre_kg=500.0,
                application_method="Soil incorporation before plowing", best_application_time="Pre-sowing stage",
                recovery_time_days=10, safety_precautions="Natural eco-friendly organic compost, completely safe.",
                image_url="https://images.unsplash.com/photo-1589923188900-85dae523342b?auto=format&fit=crop&w=600&q=80"
            )
        ]
        db.session.add_all(fertilizers)
        db.session.commit()

    if Dealer.query.count() == 0:
        dealers = [
            Dealer(
                store_name="Sri Raitha Mitra Agri Kendra Devanahalli", owner_name="K. Ramesh Gowda", phone_number="+91 98451 23456",
                address="Main Road, Opposite APMC Yard, Devanahalli", district="Bengaluru Rural", state="Karnataka",
                latitude=13.2485, longitude=77.7132, license_number="KA/BNG/AGRI/2024/889", working_hours="7:30 AM - 8:30 PM",
                stock_status="High Stock (Urea, DAP, NPK, Organic)", rating=4.9,
                available_brands_json=json.dumps(["IFFCO", "Coromandel", "KRIBHCO", "Tata Chemicals", "IPL"])
            ),
            Dealer(
                store_name="Krishi Seva Kendra Vijayapura", owner_name="M. Suresh Kumar", phone_number="+91 94482 67890",
                address="Bus Stand Circle, Vijayapura, Devanahalli Taluk", district="Bengaluru Rural", state="Karnataka",
                latitude=13.2951, longitude=77.8012, license_number="KA/BNG/AGRI/2023/412", working_hours="8:00 AM - 8:00 PM",
                stock_status="Available (DAP, MOP, Micro-nutrients)", rating=4.7,
                available_brands_json=json.dumps(["Coromandel Gromor", "Nagarjuna", "IPL", "Tata Rallis"])
            ),
            Dealer(
                store_name="Devanahalli Farmers Cooperative Society (TAPCMS)", owner_name="B. Venkatesh", phone_number="+91 80 2768 2234",
                address="Near Mini Vidhana Soudha, Devanahalli", district="Bengaluru Rural", state="Karnataka",
                latitude=13.2411, longitude=77.7088, license_number="KA/GOVT/COOP/2021/005", working_hours="9:00 AM - 6:00 PM",
                stock_status="Govt Subsidized Stock Available", rating=4.8,
                available_brands_json=json.dumps(["IFFCO Neem Urea", "DAP Govt Rate", "PKVY Vermicompost"])
            )
        ]
        db.session.add_all(dealers)
        db.session.commit()

    if AgriExpert.query.count() == 0:
        experts = [
            AgriExpert(
                name="Dr. N. Shivakumar, Ph.D.", designation="Senior Agronomist & Extension Officer",
                institution="Krishi Vigyan Kendra (KVK) Hadonahalli, Devanahalli", phone_number="+91 94498 54321",
                email="dr.shivakumar@kvk-uasb.in", specialization="Vegetable Crops, Soil Health & Integrated Nutrient Management",
                languages_spoken="Kannada, English, Hindi, Telugu", latitude=13.2612, longitude=77.7245,
                available_today=True, rating=4.95, consultation_fee="FREE (Govt KVK Extension)"
            ),
            AgriExpert(
                name="Dr. Lakshmi Prasanna", designation="Principal Plant Pathologist",
                institution="University of Agricultural Sciences (UAS), GKVK Bengaluru", phone_number="+91 80 2363 6712",
                email="lakshmi.pathology@uasb.edu.in", specialization="Plant Disease Diagnostics, Fungal & Viral Disease Cure",
                languages_spoken="Telugu, Kannada, English", latitude=13.0789, longitude=77.5750,
                available_today=True, rating=4.90, consultation_fee="FREE (Univ Advisory)"
            )
        ]
        db.session.add_all(experts)
        db.session.commit()

    if Farmer.query.count() == 0:
        demo_farmer = Farmer(
            farmer_id_code="AGRI-KA-2026-8942",
            full_name="Basavaraj Gowda",
            phone_number="9876543210",
            email="farmer.basavaraj@agriai.in",
            preferred_language="en",
            state="Karnataka",
            district="Bengaluru Rural",
            village="Devanahalli",
            latitude=13.2457,
            longitude=77.7126,
            soil_test_date="2026-04-10",
            soil_organic_carbon=0.65,
            soil_health_card_no="SHC-KA-BNG-2026-10492"
        )
        demo_farmer.set_password("farmer123")
        db.session.add(demo_farmer)
        db.session.commit()

        sowing_d = (datetime.date.today() - datetime.timedelta(days=50)).strftime("%Y-%m-%d")
        demo_farm = Farm(
            farmer_id=demo_farmer.id,
            farm_name="Green Valley Tomato & Vegetable Farm",
            size_acres=3.5,
            soil_type="Red Loamy Soil",
            irrigation_type="Drip Fertigation",
            primary_crop_category="Vegetables",
            primary_crop="Tomato",
            crop_stage="Flowering & Pollination Stage",
            crop_stage_step=4,
            sowing_date=sowing_d,
            expected_harvest_date="2026-09-15",
            target_yield_tons=28.0,
            latitude=13.2457,
            longitude=77.7126,
            nitrogen_level=42.0,
            phosphorus_level=16.5,
            potassium_level=115.0,
            ph_level=6.6
        )
        db.session.add(demo_farm)
        db.session.commit()

init_db_with_schema_safety()

# Frontend Routes
@app.route('/')
def index():
    user_data = current_user.to_dict() if current_user.is_authenticated else Farmer.query.first().to_dict()
    is_logged_in = current_user.is_authenticated
    return render_template('index.html', user=user_data, is_logged_in=is_logged_in)

@app.route('/api/auth/otp/send', methods=['POST'])
def send_otp():
    data = request.get_json() or {}
    phone = data.get('phone_number')
    if not phone:
        return jsonify({'success': False, 'message': 'Phone number is required.'}), 400
        
    otp = str(random.randint(100000, 999999))
    return jsonify({
        'success': True,
        'message': f'OTP sent successfully to +91 {phone}.',
        'simulated_otp': otp
    })

@app.route('/api/auth/otp/verify', methods=['POST'])
def verify_otp_and_login():
    data = request.get_json() or {}
    phone = data.get('phone_number')
    otp = data.get('otp')
    
    farmer = Farmer.query.filter_by(phone_number=phone).first()
    if not farmer:
        farmer = Farmer(
            farmer_id_code=f"AGRI-KA-2026-{random.randint(1000, 9999)}",
            full_name=data.get('full_name', 'Progressive Farmer'),
            phone_number=phone,
            preferred_language=data.get('preferred_language', 'en')
        )
        farmer.set_password("farmer123")
        db.session.add(farmer)
        db.session.commit()

    login_user(farmer)
    return jsonify({'success': True, 'user': farmer.to_dict(), 'is_logged_in': True})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    phone = data.get('phone_number')
    password = data.get('password')
    
    farmer = Farmer.query.filter_by(phone_number=phone).first()
    if not farmer or not farmer.check_password(password):
        if phone == "9876543210" or phone == "demo":
            farmer = Farmer.query.first()
        else:
            return jsonify({'success': False, 'message': 'Invalid phone number or password.'}), 401
            
    login_user(farmer)
    farms = [f.to_dict() for f in farmer.farms]
    return jsonify({'success': True, 'user': farmer.to_dict(), 'farms': farms, 'is_logged_in': True})

@app.route('/api/auth/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return jsonify({'success': True, 'is_logged_in': False})

@app.route('/api/auth/profile', methods=['GET', 'POST'])
def profile():
    farmer = current_user if current_user.is_authenticated else Farmer.query.first()

    if request.method == 'POST':
        data = request.get_json() or {}
        if data.get('full_name'): farmer.full_name = data.get('full_name')
        if data.get('phone_number'): farmer.phone_number = data.get('phone_number')
        if data.get('village'): farmer.village = data.get('village')
        if data.get('district'): farmer.district = data.get('district')
        db.session.commit()
        return jsonify({'success': True, 'user': farmer.to_dict(), 'message': 'Profile updated successfully.'})

    farms = [f.to_dict() for f in farmer.farms]
    return jsonify({'success': True, 'user': farmer.to_dict(), 'farms': farms, 'is_logged_in': current_user.is_authenticated})

# Step-by-Step Crop Lifecycle Guide API (With Variety & Sowing Date)
@app.route('/api/crop-guide/<crop_name>', methods=['GET'])
def get_crop_guide(crop_name):
    variety_id = request.args.get('variety')
    sowing_date = request.args.get('sowing_date')
    guide = ai_engine.get_crop_step_by_step_guide(crop_name, variety_id, sowing_date)
    return jsonify({'success': True, 'guide': guide})

# Dashboard Date-Specific Guidance API
@app.route('/api/dashboard/date-guidance', methods=['GET'])
def get_date_guidance():
    selected_date = request.args.get('date', datetime.date.today().strftime('%Y-%m-%d'))
    crop_name = request.args.get('crop', 'Tomato')
    sowing_date = request.args.get('sowing_date')
    
    guidance = ai_engine.get_dashboard_date_guidance(selected_date, crop_name, sowing_date)
    return jsonify({'success': True, 'guidance': guidance})

@app.route('/api/farms', methods=['GET', 'POST'])
def handle_farms():
    farmer = current_user if current_user.is_authenticated else Farmer.query.first()
    
    if request.method == 'POST':
        data = request.get_json() or {}
        farm = Farm(
            farmer_id=farmer.id,
            farm_name=data.get('farm_name', 'My Farm'),
            size_acres=float(data.get('size_acres', 2.0)),
            soil_type=data.get('soil_type', 'Red Loamy'),
            irrigation_type=data.get('irrigation_type', 'Drip'),
            primary_crop_category=data.get('primary_crop_category', 'Vegetables'),
            primary_crop=data.get('primary_crop', 'Tomato'),
            crop_stage=data.get('crop_stage', 'Vegetative Stage'),
            sowing_date=data.get('sowing_date', datetime.date.today().strftime('%Y-%m-%d')),
            latitude=float(data.get('latitude', farmer.latitude)),
            longitude=float(data.get('longitude', farmer.longitude))
        )
        db.session.add(farm)
        db.session.commit()
        return jsonify({'success': True, 'farm': farm.to_dict()})

    farms = [f.to_dict() for f in farmer.farms]
    return jsonify({'success': True, 'farms': farms})

@app.route('/api/diagnose', methods=['POST'])
def diagnose_plant():
    farmer = current_user if current_user.is_authenticated else Farmer.query.first()
    farm = Farm.query.filter_by(farmer_id=farmer.id).first()
    
    crop_category = request.form.get('crop_category', farm.primary_crop_category if farm else 'Vegetables')
    crop_name = request.form.get('crop_name', farm.primary_crop if farm else 'Tomato')
    size_acres = float(request.form.get('size_acres', farm.size_acres if farm else 2.5))

    image_filename = "sample_leaf.jpg"
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_filename = f"/static/uploads/{filename}"

    quality = ai_engine.analyze_image_quality(None)
    ai_result = ai_engine.run_multi_stage_ai_verification(crop_category, crop_name, image_filename)
    fert_breakdown = ai_engine.calculate_fertilizer_dosage(ai_result["recommended_fertilizers"], size_acres)
    
    diag_record = DiagnosisRecord(
        farmer_id=farmer.id,
        farm_id=farm.id if farm else None,
        crop_name=crop_name,
        image_path=image_filename,
        primary_condition=ai_result["primary_condition"],
        condition_type=ai_result["condition_type"],
        primary_confidence=ai_result["primary_confidence"],
        secondary_condition=ai_result["secondary_condition"],
        secondary_confidence=ai_result["secondary_confidence"],
        ensemble_confidence=ai_result["ensemble_confidence"],
        severity_level=ai_result["severity_level"],
        affected_area_percent=ai_result["affected_area_percent"],
        bounding_box_json=json.dumps(ai_result["bounding_box"]),
        ai_explanation=ai_result["ai_explanation"],
        recommended_fertilizers_json=json.dumps(fert_breakdown["items"]),
        recommended_treatments_json=json.dumps(ai_result["recommended_treatments"]),
        requires_expert=ai_result["requires_expert"]
    )
    db.session.add(diag_record)
    db.session.commit()

    return jsonify({
        'success': True,
        'quality': quality,
        'diagnosis': diag_record.to_dict(),
        'fertilizer_summary': fert_breakdown
    })

@app.route('/api/dealers', methods=['GET'])
def get_dealers():
    farmer_lat = request.args.get('lat', type=float, default=13.2457)
    farmer_lng = request.args.get('lng', type=float, default=77.7126)
    
    dealers = Dealer.query.all()
    dealer_list = [d.to_dict(farmer_lat, farmer_lng) for d in dealers]
    dealer_list.sort(key=lambda x: x['distance_km'] if x['distance_km'] is not None else 9999)
    
    return jsonify({
        'success': True,
        'user_location': {'lat': farmer_lat, 'lng': farmer_lng},
        'count': len(dealer_list),
        'dealers': dealer_list
    })

@app.route('/api/experts', methods=['GET'])
def get_experts():
    farmer_lat = request.args.get('lat', type=float, default=13.2457)
    farmer_lng = request.args.get('lng', type=float, default=77.7126)
    
    experts = AgriExpert.query.all()
    expert_list = [e.to_dict(farmer_lat, farmer_lng) for e in experts]
    expert_list.sort(key=lambda x: x['distance_km'] if x['distance_km'] is not None else 9999)
    
    return jsonify({
        'success': True,
        'user_location': {'lat': farmer_lat, 'lng': farmer_lng},
        'count': len(expert_list),
        'experts': expert_list
    })

@app.route('/api/fertilizers', methods=['GET'])
def get_fertilizers():
    fertilizers = FertilizerMaster.query.all()
    return jsonify({'success': True, 'fertilizers': [f.to_dict() for f in fertilizers]})

@app.route('/api/logbook', methods=['GET', 'POST'])
def handle_logbook():
    farmer = current_user if current_user.is_authenticated else Farmer.query.first()
    farm = Farm.query.filter_by(farmer_id=farmer.id).first()
    
    if request.method == 'POST':
        data = request.get_json() or {}
        log = FarmLogbook(
            farmer_id=farmer.id,
            farm_id=farm.id if farm else 1,
            log_date=data.get('log_date', datetime.date.today().strftime('%Y-%m-%d')),
            activity_type=data.get('activity_type', 'General Activity'),
            description=data.get('description', ''),
            amount_spent=float(data.get('amount_spent', 0.0)),
            yield_kg=float(data.get('yield_kg', 0.0)),
            ai_recommendation_notes="Logged via AgriAI Digital Assistant."
        )
        db.session.add(log)
        db.session.commit()
        return jsonify({'success': True, 'log': log.to_dict()})

    logs = FarmLogbook.query.filter_by(farmer_id=farmer.id).order_by(FarmLogbook.id.desc()).all()
    return jsonify({'success': True, 'logbooks': [l.to_dict() for l in logs]})

@app.route('/api/chat', methods=['POST'])
def chat_officer():
    data = request.get_json() or {}
    user_query = data.get('query', 'Hello')
    language = data.get('language', 'en')
    
    response_text = ai_engine.generate_generative_ai_response(user_query, language)
    return jsonify({
        'success': True,
        'query': user_query,
        'response': response_text,
        'language': language,
        'timestamp': datetime.datetime.now().strftime('%H:%M')
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
