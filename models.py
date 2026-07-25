import datetime
import json
import random
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Farmer(UserMixin, db.Model):
    __tablename__ = 'farmers'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id_code = db.Column(db.String(50), unique=True, nullable=False, default='AGRI-KA-2026-8942')
    full_name = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    preferred_language = db.Column(db.String(20), default='en') # en, kn, te, hi
    state = db.Column(db.String(80), default='Karnataka')
    district = db.Column(db.String(80), default='Bengaluru Rural')
    village = db.Column(db.String(100), default='Devanahalli')
    latitude = db.Column(db.Float, default=13.2457)
    longitude = db.Column(db.Float, default=77.7126)
    
    # Soil Health Card & Profile Metadata
    soil_test_date = db.Column(db.String(30), default='2026-04-10')
    soil_organic_carbon = db.Column(db.Float, default=0.65)
    soil_health_card_no = db.Column(db.String(80), default='SHC-KA-BNG-2026-10492')
    notification_sms = db.Column(db.Boolean, default=True)
    notification_whatsapp = db.Column(db.Boolean, default=True)
    notification_voice_calls = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    farms = db.relationship('Farm', backref='owner', lazy=True, cascade="all, delete-orphan")
    logbooks = db.relationship('FarmLogbook', backref='farmer', lazy=True, cascade="all, delete-orphan")
    diagnoses = db.relationship('DiagnosisRecord', backref='farmer', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id_code': self.farmer_id_code,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'preferred_language': self.preferred_language,
            'state': self.state,
            'district': self.district,
            'village': self.village,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'soil_test_date': self.soil_test_date,
            'soil_organic_carbon': self.soil_organic_carbon,
            'soil_health_card_no': self.soil_health_card_no,
            'notification_sms': self.notification_sms,
            'notification_whatsapp': self.notification_whatsapp,
            'notification_voice_calls': self.notification_voice_calls,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class Farm(db.Model):
    __tablename__ = 'farms'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    farm_name = db.Column(db.String(120), nullable=False)
    size_acres = db.Column(db.Float, nullable=False, default=2.5)
    soil_type = db.Column(db.String(80), default='Red Loamy')
    irrigation_type = db.Column(db.String(80), default='Drip')
    primary_crop_category = db.Column(db.String(80), default='Vegetables')
    primary_crop = db.Column(db.String(80), default='Tomato')
    crop_stage = db.Column(db.String(80), default='Flowering Stage')
    crop_stage_step = db.Column(db.Integer, default=4)
    sowing_date = db.Column(db.String(30), default='2026-06-01')
    expected_harvest_date = db.Column(db.String(30), default='2026-09-15')
    target_yield_tons = db.Column(db.Float, default=25.0)
    latitude = db.Column(db.Float, default=13.2457)
    longitude = db.Column(db.Float, default=77.7126)
    
    nitrogen_level = db.Column(db.Float, default=45.0)
    phosphorus_level = db.Column(db.Float, default=18.0)
    potassium_level = db.Column(db.Float, default=120.0)
    ph_level = db.Column(db.Float, default=6.5)

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farm_name': self.farm_name,
            'size_acres': self.size_acres,
            'soil_type': self.soil_type,
            'irrigation_type': self.irrigation_type,
            'primary_crop_category': self.primary_crop_category,
            'primary_crop': self.primary_crop,
            'crop_stage': self.crop_stage,
            'crop_stage_step': self.crop_stage_step,
            'sowing_date': self.sowing_date,
            'expected_harvest_date': self.expected_harvest_date,
            'target_yield_tons': self.target_yield_tons,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'nitrogen_level': self.nitrogen_level,
            'phosphorus_level': self.phosphorus_level,
            'potassium_level': self.potassium_level,
            'ph_level': self.ph_level
        }

class DiagnosisRecord(db.Model):
    __tablename__ = 'diagnosis_records'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=True)
    crop_name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    primary_condition = db.Column(db.String(150), nullable=False)
    condition_type = db.Column(db.String(50), nullable=False)
    primary_confidence = db.Column(db.Float, nullable=False)
    secondary_condition = db.Column(db.String(150), nullable=True)
    secondary_confidence = db.Column(db.Float, nullable=True)
    ensemble_confidence = db.Column(db.Float, nullable=False)
    severity_level = db.Column(db.String(30), nullable=False)
    affected_area_percent = db.Column(db.Float, default=15.0)
    bounding_box_json = db.Column(db.Text, nullable=True)
    ai_explanation = db.Column(db.Text, nullable=False)
    recommended_fertilizers_json = db.Column(db.Text, nullable=True)
    recommended_treatments_json = db.Column(db.Text, nullable=True)
    requires_expert = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farm_id': self.farm_id,
            'crop_name': self.crop_name,
            'image_path': self.image_path,
            'primary_condition': self.primary_condition,
            'condition_type': self.condition_type,
            'primary_confidence': round(self.primary_confidence * 100, 1),
            'secondary_condition': self.secondary_condition,
            'secondary_confidence': round(self.secondary_confidence * 100, 1) if self.secondary_confidence else None,
            'ensemble_confidence': round(self.ensemble_confidence * 100, 1),
            'severity_level': self.severity_level,
            'affected_area_percent': self.affected_area_percent,
            'bounding_box': json.loads(self.bounding_box_json) if self.bounding_box_json else [],
            'ai_explanation': self.ai_explanation,
            'recommended_fertilizers': json.loads(self.recommended_fertilizers_json) if self.recommended_fertilizers_json else [],
            'recommended_treatments': json.loads(self.recommended_treatments_json) if self.recommended_treatments_json else [],
            'requires_expert': self.requires_expert,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class FertilizerMaster(db.Model):
    __tablename__ = 'fertilizer_master'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    npk_ratio = db.Column(db.String(50), default='19:19:19')
    target_deficiency = db.Column(db.String(100), nullable=True)
    original_price_per_bag = db.Column(db.Float, nullable=False)
    subsidized_price_per_bag = db.Column(db.Float, nullable=False)
    subsidy_scheme = db.Column(db.String(150), default='PM Fertilizer Subsidy (DBT)')
    dosage_per_acre_kg = db.Column(db.Float, default=25.0)
    application_method = db.Column(db.String(150), default='Foliar spray / Soil application')
    best_application_time = db.Column(db.String(120), default='Early morning or late evening')
    recovery_time_days = db.Column(db.Integer, default=7)
    safety_precautions = db.Column(db.Text, default='Wear protective mask and gloves during application.')
    image_url = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'brand': self.brand,
            'npk_ratio': self.npk_ratio,
            'target_deficiency': self.target_deficiency,
            'original_price_per_bag': self.original_price_per_bag,
            'subsidized_price_per_bag': self.subsidized_price_per_bag,
            'subsidy_savings': round(self.original_price_per_bag - self.subsidized_price_per_bag, 2),
            'subsidy_scheme': self.subsidy_scheme,
            'dosage_per_acre_kg': self.dosage_per_acre_kg,
            'application_method': self.application_method,
            'best_application_time': self.best_application_time,
            'recovery_time_days': self.recovery_time_days,
            'safety_precautions': self.safety_precautions,
            'image_url': self.image_url
        }

class Dealer(db.Model):
    __tablename__ = 'dealers'
    
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(150), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    license_number = db.Column(db.String(80), nullable=False)
    working_hours = db.Column(db.String(80), default='8:00 AM - 8:00 PM')
    stock_status = db.Column(db.String(50), default='Available (High Stock)')
    rating = db.Column(db.Float, default=4.8)
    available_brands_json = db.Column(db.Text, nullable=True)

    def to_dict(self, farmer_lat=None, farmer_lng=None):
        distance = None
        if farmer_lat and farmer_lng:
            import math
            R = 6371
            dlat = math.radians(self.latitude - farmer_lat)
            dlng = math.radians(self.longitude - farmer_lng)
            a = math.sin(dlat/2)**2 + math.cos(math.radians(farmer_lat)) * math.cos(math.radians(self.latitude)) * math.sin(dlng/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = round(R * c, 2)
            
        return {
            'id': self.id,
            'store_name': self.store_name,
            'owner_name': self.owner_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'district': self.district,
            'state': self.state,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'license_number': self.license_number,
            'working_hours': self.working_hours,
            'stock_status': self.stock_status,
            'rating': self.rating,
            'available_brands': json.loads(self.available_brands_json) if self.available_brands_json else [],
            'distance_km': distance
        }

class AgriExpert(db.Model):
    __tablename__ = 'agri_experts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    designation = db.Column(db.String(120), nullable=False)
    institution = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(150), nullable=False)
    languages_spoken = db.Column(db.String(100), default='Kannada, English, Hindi, Telugu')
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    available_today = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=4.9)
    consultation_fee = db.Column(db.String(50), default='FREE (Govt Extension Support)')

    def to_dict(self, farmer_lat=None, farmer_lng=None):
        distance = None
        if farmer_lat and farmer_lng:
            import math
            R = 6371
            dlat = math.radians(self.latitude - farmer_lat)
            dlng = math.radians(self.longitude - farmer_lng)
            a = math.sin(dlat/2)**2 + math.cos(math.radians(farmer_lat)) * math.cos(math.radians(self.latitude)) * math.sin(dlng/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = round(R * c, 2)

        return {
            'id': self.id,
            'name': self.name,
            'designation': self.designation,
            'institution': self.institution,
            'phone_number': self.phone_number,
            'email': self.email,
            'specialization': self.specialization,
            'languages_spoken': self.languages_spoken,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'available_today': self.available_today,
            'rating': self.rating,
            'consultation_fee': self.consultation_fee,
            'distance_km': distance
        }

class FarmLogbook(db.Model):
    __tablename__ = 'farm_logbooks'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    log_date = db.Column(db.String(30), nullable=False)
    activity_type = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount_spent = db.Column(db.Float, default=0.0)
    yield_kg = db.Column(db.Float, default=0.0)
    ai_recommendation_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farm_id': self.farm_id,
            'log_date': self.log_date,
            'activity_type': self.activity_type,
            'description': self.description,
            'amount_spent': self.amount_spent,
            'yield_kg': self.yield_kg,
            'ai_recommendation_notes': self.ai_recommendation_notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
