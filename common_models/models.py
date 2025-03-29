from datetime import datetime
from common_models.db import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import JSONB  # Import JSONB
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime, String, Float, Date, ForeignKey, Boolean, Text, Table
import csv
import random
import string
import json
import pandas as pd
import io
from sqlalchemy.orm import relationship

dog_vet_association = db.Table('dog_vet',
    db.Column('dog_id', db.Integer, db.ForeignKey('dog.dog_id'), primary_key=True),
    db.Column('vet_id', db.Integer, db.ForeignKey('vet.vet_id'), primary_key=True),
    extend_existing=True
)

prevention_condition = db.Table(
    'prevention_condition',
    db.Column('prevention_id', db.Integer, ForeignKey('prevention.prevention_id'), primary_key=True),
    db.Column('condition_id', db.Integer, ForeignKey('conditions.condition_id'), primary_key=True),
    extend_existing=True
)

prevention_symptom = db.Table(
    'prevention_symptom',
    db.Column('prevention_id', db.Integer, ForeignKey('prevention.prevention_id'), primary_key=True),
    db.Column('symptom_id', db.Integer, ForeignKey('symptoms.symptom_id'), primary_key=True),
    extend_existing=True
)

drug_condition = db.Table(
    'drug_condition',
    db.Column('drug_id', db.Integer, ForeignKey('drugs.drug_id'), primary_key=True),
    db.Column('condition_id', db.Integer, ForeignKey('conditions.condition_id'), primary_key=True),
    extend_existing=True
)

panel_components = db.Table('panel_components',
    db.Column('panel_id', db.Integer, db.ForeignKey('panel.id', ondelete="CASCADE"), primary_key=True),
    db.Column('component_id', db.Integer, db.ForeignKey('component.id'), primary_key=True),
    extend_existing=True
)

drug_ingredients = db.Table(
    'drug_ingredients',
    db.Column('drug_id', db.Integer, ForeignKey('drugs.drug_id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, ForeignKey('active_ingredients.ingredient_id'), primary_key=True),
    extend_existing=True
)

drug_dosage_forms = db.Table(
    'drug_dosage_forms',
    db.Column('drug_id', db.Integer, db.ForeignKey('drugs.drug_id'), primary_key=True),
    db.Column('dosage_form_id', db.Integer, db.ForeignKey('dosage_forms.dosage_form_id'), primary_key=True),
    extend_existing=True
)


class Role(db.Model):
    __table_args__ = {'extend_existing': True}
    """
    Role model representing user roles (e.g., Vet, Patient).

    Attributes:
        id (int): Primary key.
        name (str): Name of the role.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
class User(db.Model, UserMixin):
    """
    User model representing users of the system.

    Attributes:
        id (int): Primary key.
        email (str): User's email address.
        password (str): Hashed password.
        name (str): User's first name.
        last_name (str): User's last name.
        phone (str): User's phone number.
        next_page (str): Next page to navigate to.
        last_dog (int): ID of the last dog added by the user.
        dogs (relationship): List of dogs owned by the user.
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'user'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=True, default='Pending')
    password = db.Column(db.String(60))
    name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    dogs = db.relationship('Dog', backref='owner', lazy=True)
    def __repr__(self):
            return f"User('{self.email}')"
    def get_id(self):
        return f"user-{self.id}"

class Dog(db.Model):
    """
    Dog model representing dogs in the system.

    Attributes:
        dog_id (int): Primary key.
        owner_id (int): Foreign key linking to the owner (User).
        vets (relationship): List of vets associated with the dog.
        image_status (int): Status of the dog's image.
        dd_microchip (str): Dog's microchip number.
        dd_dog_name (str): Dog's name.
        dd_weight_lbs (int): Dog's weight in pounds.
        dd_sex (str): Dog's sex.
        dd_age_years (int): Dog's age in years.
        cv_population_density (float): Population density of the area where the dog lives.
        cv_gini_index (float): Gini index of the area where the dog lives.
        cv_median_income (float): Median income of the area where the dog lives.
        cv_population_estimate (float): Population estimate of the area where the dog lives.
        cv_pct_female (float): Percentage of females in the area where the dog lives.
        cv_pct_owner_occupied (float): Percentage of owner-occupied households in the area where the dog lives.
        cv_pct_nothispanic_white (float): Percentage of non-Hispanic white population in the area where the dog lives.
        cv_pct_nothispanic_black (float): Percentage of non-Hispanic black population in the area where the dog lives.
        cv_pct_nothispanic_ian (float): Percentage of non-Hispanic American Indian and Alaska Native population in the area where the dog lives.
        cv_pct_nothispanic_asian (float): Percentage of non-Hispanic Asian population in the area where the dog lives.
        cv_pct_nothispanic_hpi (float): Percentage of non-Hispanic Native Hawaiian and Other Pacific Islander population in the area where the dog lives.
        cv_pct_hispanic (float): Percentage of Hispanic population in the area where the dog lives.
        cv_pct_below_125povline (float): Percentage of population below 125% of the poverty line in the area where the dog lives.
        cv_pct_famsownchild_female_led (float): Percentage of families with own children under 18 years led by a female householder with no husband present in the area where the dog lives.
        cv_pct_less_than_100k (float): Percentage of households with income less than $100,000 in the area where the dog lives.
        cv_pct_same_house_1yrago (float): Percentage of people living in the same house 1 year ago in the area where the dog lives.
        tp_tmpc_norm_07 (float): Normalized temperature in July in the area where the dog lives.
        tp_tmpc_norm_12 (float): Normalized temperature in December in the area where the dog lives.
        pv_no2 (float): NO2 pollution value in the area where the dog lives.
        pv_o3 (float): O3 pollution value in the area where the dog lives.
        pv_pm10 (float): PM10 pollution value in the area where the dog lives.
        pv_pm25 (float): PM2.5 pollution value in the area where the dog lives.
        pv_so2 (float): SO2 pollution value in the area where the dog lives.
        time_together (int): Time spent together with the owner.
        breed (str): Dog's breed.
        dd_breed_mixed (int): Indicator of whether the dog is mixed breed.
        dd_breed_pure (int): Indicator of whether the dog is purebred.
        dd_breed_mixed_primary (int): Primary breed in mixed breed dogs.
        dd_breed_mixed_secondary (int): Secondary breed in mixed breed dogs.
        address (str): Address where the dog lives.
        de_home_square_footage (int): Square footage of the home.
        de_home_years_lived_in (int): Years lived in the home.
        de_property_area (int): Area of the property.
        de_home_construction_decade (int): Decade of home construction.
        de_traffic_noise_in_home_frequency (int): Frequency of traffic noise in the home.
        de_routine_hours_per_day_roaming_house (int): Routine hours per day spent roaming the house.
        de_routine_hours_per_day_in_yard (int): Routine hours per day spent in the yard.
        de_daytime_sleep_avg_hours (int): Average hours of daytime sleep.
        de_nighttime_sleep_avg_hours (int): Average hours of nighttime sleep.
        pa_activity_level (int): Physical activity level.
        pa_other_aerobic_activity_frequency (int): Frequency of other aerobic activities.
        pa_physical_games_frequency (int): Frequency of physical games.
        db_playful_frequency (int): Frequency of playfulness.
        mp_dental_examination_frequency (int): Frequency of dental examinations.
        mp_dental_treat_frequency (int): Frequency of dental treats.
        mp_dental_procedure_undergone (int): Dental procedures undergone.
        mp_flea_and_tick_treatment (int): Flea and tick treatment status.
        mp_flea_and_tick_treatment_frequency (int): Frequency of flea and tick treatment.
        mp_heartworm_preventative (int): Heartworm preventative status.
        mp_heartworm_preventative_frequency (int): Frequency of heartworm preventative.
        mp_vaccination_status (int): Vaccination status.
        hs_general_health (int): General health status.
        hs_new_condition_diagnosed_recently (int): Recently diagnosed conditions.
        hs_chronic_condition_present (int): Presence of chronic conditions.
        hs_condition_is_congenital (int): Congenital condition status.
        health_conditions (JSON): JSON field storing health conditions.
        dd_status (str): Dog's status.
        next_due (Date): Date of the next due event.
        date_enrolled (Date): Date the dog was enrolled in the system.
        processed (int): Processed status.
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'dog'
    dog_id = db.Column(db.Integer, unique=True, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vets = db.relationship('Vet', secondary=dog_vet_association, backref=db.backref('dogs', lazy=True), cascade="all, delete")
    image_status = db.Column(db.Integer, default=0)
    screen_status = db.Column(db.String(100))
    last_screen = db.Column(DateTime(timezone=False), server_default=func.now())
    ss_household_dog_count = db.Column(db.Integer)
    
    dd_dob = db.Column(Date, nullable=True)
    dd_microchip = db.Column(db.String(100))
    dd_dog_name = db.Column(db.String(30))
    dd_weight_lbs = db.Column(db.Float)
    dd_expected_weight_range = db.Column(db.String(30))
    dd_weight_range = db.Column(db.Integer)
    dd_weight_range_expected_adult = db.Column(db.String(30))
    
    is_overweight = db.Column(db.Boolean)
    is_underweight = db.Column(db.Boolean)
    off_weight_by = db.Column(db.Float)
    
    df_ever_underweight = db.Column(db.Integer)
    df_ever_overweight = db.Column(db.Integer)
    df_weight_change_last_year = db.Column(db.Integer)

    dd_sex = db.Column(db.String(180))
    dd_spayed_or_neutered = db.Column(db.Integer)
    dd_spay_or_neuter_age = db.Column(db.Integer)

    dd_age_years = db.Column(db.Float)
    dd_expected_lifespan = db.Column(db.String(30))
    dd_lifestage = db.Column(db.String(30))

    cv_population_density = db.Column(db.Float)
    cv_gini_index = db.Column(db.Float)
    cv_median_income = db.Column(db.Float)
    cv_population_estimate = db.Column(db.Float)
    cv_pct_female = db.Column(db.Float)
    cv_pct_owner_occupied = db.Column(db.Float)
    cv_pct_nothispanic_white = db.Column(db.Float)
    cv_pct_nothispanic_black = db.Column(db.Float)
    # cv_pct_nothispanic_ian = db.Column(db.Float) #### Remove
    cv_pct_nothispanic_asian = db.Column(db.Float)
    # cv_pct_nothispanic_hpi = db.Column(db.Float) #### Remove
    cv_pct_hispanic = db.Column(db.Float)
    cv_pct_below_125povline = db.Column(db.Float)
    # cv_pct_famsownchild_female_led = db.Column(db.Float) #### Remove
    cv_pct_less_than_100k = db.Column(db.Float)
    cv_pct_same_house_1yrago = db.Column(db.Float)
    
    tp_tmpc_norm_07 = db.Column(db.Float)
    tp_tmpc_norm_12 = db.Column(db.Float)
    
    pv_no2 = db.Column(db.Float)
    pv_o3 = db.Column(db.Float)
    pv_pm10 = db.Column(db.Float)
    pv_pm25 = db.Column(db.Float)
    pv_so2 = db.Column(db.Float)

    # time_together = db.Column(db.Integer, nullable=True) #### Remove
    
    breed = db.Column(db.String(100), nullable=True)
    dd_breed_pure_or_mixed = db.Column(db.Integer, nullable=True)
    dd_breed_pure = db.Column(db.Integer, nullable=True)
    dd_breed_mixed_primary = db.Column(db.Integer, nullable=True)
    dd_breed_mixed_secondary = db.Column(db.Integer, nullable=True)

    address = db.Column(db.String(180))
    
    de_home_square_footage = db.Column(db.Integer)
    # de_home_years_lived_in = db.Column(db.Integer) #### Remove
    de_property_area = db.Column(db.Integer) 
    # de_home_construction_decade = db.Column(db.Integer) #### Remove
    # de_traffic_noise_in_home_frequency = db.Column(db.Integer) #### Remove
    de_routine_hours_per_day_roaming_house = db.Column(db.Integer)
    de_routine_hours_per_day_roaming_outside = db.Column(db.Integer)
    de_routine_hours_per_day_in_yard = db.Column(db.Integer)
    de_daytime_sleep_avg_hours = db.Column(db.Integer)
    de_nighttime_sleep_avg_hours = db.Column(db.Integer)
    
    de_recreational_spaces = db.Column(db.Integer)
    de_recreational_spaces_days_per_month = db.Column(db.Integer)
    de_stairs_avg_flights_per_day = db.Column(db.Integer)
    de_routine_toys = db.Column(db.Integer)
    de_routine_toys_hours_per_day = db.Column(db.Integer)
    de_routine_hours_per_day_away_from_home = db.Column(db.Integer)
    de_dogpark = db.Column(db.Integer)
    de_dogpark_days_per_month = db.Column(db.Integer)
    
    pa_on_leash_off_leash_walk = db.Column(db.Integer)
    pa_activity_level = db.Column(db.Integer)
    pa_avg_activity_intensity = db.Column(db.Integer)
    # pa_other_aerobic_activity_frequency = db.Column(db.Integer) # Remove
    pa_physical_games_frequency = db.Column(db.Integer)
    pa_swim_moderate_weather_frequency = db.Column(db.Integer)
    pa_on_leash_walk_frequency = db.Column(db.Integer)
    # db_playful_frequency = db.Column(db.Integer) # Remove

    de_eats_feces = db.Column(db.Integer)
    de_eats_grass_frequency = db.Column(db.Integer)
    de_drinks_outdoor_water = db.Column(db.Integer)
    de_drinking_water_source = db.Column(db.Integer)
    
    de_recent_toxins_or_hazards_ingested_frequency = db.Column(db.Integer)
    de_recent_toxins_or_hazards_ingested_required_vet = db.Column(db.Integer)
    de_recent_toxins_or_hazards_ingested_chocolate = db.Column(db.Integer)
    de_recent_toxins_or_hazards_ingested_poison = db.Column(db.Integer)
    de_recent_toxins_or_hazards_ingested_human_medication = db.Column(db.Integer)
    de_recent_toxins_or_hazards_ingested_garbage_or_food = db.Column(db.Integer)
    
    df_primary_diet_component = db.Column(db.Integer)
    df_secondary_diet_component = db.Column(db.Integer)
    df_primary_diet_component_change_recent = db.Column(db.Integer)
    df_primary_diet_component_change_months_ago = db.Column(db.Integer)
    df_primary_diet_component_change_allergy_related = db.Column(db.Integer)
    df_primary_diet_component_change_health_condition_specific = db.Column(db.Integer)
    df_treats_table_carbs = db.Column(db.Integer)
    df_feedings_per_day = db.Column(db.Integer)
    df_appetite = db.Column(db.Integer)
    df_primary_diet_component_grain_free = db.Column(db.Integer)
    df_appetite_change_last_year = db.Column(db.Integer)
    
    
    df_daily_supplements = db.Column(db.Integer)
    df_daily_supplements_fiber = db.Column(db.Integer)
    df_daily_supplements_alkalinize = db.Column(db.Integer)
    df_daily_supplements_acidify = db.Column(db.Integer)
    df_daily_supplements_probiotics = db.Column(db.Integer)
    df_daily_supplements_chondroitin = db.Column(db.Integer)
    
    de_routine_consistency = db.Column(db.Integer)

    mp_dental_examination_frequency = db.Column(db.Integer)
    mp_dental_brushing_frequency = db.Column(db.Integer)

    mp_dental_treat_frequency = db.Column(db.Integer)
    mp_dental_procedure_undergone = db.Column(db.Integer)
    mp_dental_cleaning = db.Column(db.Integer)
    mp_dental_cleaning_months_ago = db.Column(db.Integer)
    mp_dental_extraction = db.Column(db.Integer)
    mp_dental_extraction_months_ago = db.Column(db.Integer)
    
    mp_home_grooming_frequency = db.Column(db.Integer)

    mp_flea_and_tick_treatment = db.Column(db.Integer)
    # mp_flea_and_tick_treatment_frequency = db.Column(db.Integer) # Rremove
    mp_heartworm_preventative = db.Column(db.Integer)
    # mp_heartworm_preventative_frequency = db.Column(db.Integer) # Rremove
    mp_vaccination_status = db.Column(db.Integer)
    
    mp_recent_non_prescription_meds_ear_cleaner = db.Column(db.Integer)

    hs_general_health = db.Column(db.Integer)
    hs_new_condition_diagnosed_recently = db.Column(db.Integer)
    hs_chronic_condition_present = db.Column(db.Integer)
    hs_congenital_condition_present = db.Column(db.Integer)

    hs_health_conditions_cancer = db.Column(db.Integer, default=0)
    hs_health_conditions_cardiac = db.Column(db.Integer, default=0)
    hs_health_conditions_ear = db.Column(db.Integer, default=0)
    hs_health_conditions_endocrine = db.Column(db.Integer, default=0)
    hs_health_conditions_eye = db.Column(db.Integer, default=0)
    hs_health_conditions_gastrointestinal = db.Column(db.Integer, default=0)
    hs_health_conditions_hematologic = db.Column(db.Integer, default=0)
    hs_health_conditions_immune = db.Column(db.Integer, default=0)
    hs_health_conditions_infectious_disease = db.Column(db.Integer, default=0)
    hs_health_conditions_kidney = db.Column(db.Integer, default=0)
    hs_health_conditions_liver = db.Column(db.Integer, default=0)
    hs_health_conditions_neurological = db.Column(db.Integer, default=0)
    hs_health_conditions_oral = db.Column(db.Integer, default=0)
    hs_health_conditions_orthopedic = db.Column(db.Integer, default=0)
    hs_health_conditions_other = db.Column(db.Integer, default=0)
    hs_health_conditions_reproductive = db.Column(db.Integer, default=0)
    hs_health_conditions_respiratory = db.Column(db.Integer, default=0)
    hs_health_conditions_skin = db.Column(db.Integer, default=0)
    hs_health_conditions_toxin_consumption = db.Column(db.Integer, default=0)
    hs_health_conditions_trauma = db.Column(db.Integer, default=0)

    health_conditions = db.Column(db.JSON)
    imminent_conditions = db.Column(db.JSON)

    status = db.Column(db.String(30), nullable=True)
    next_due = db.Column(Date, nullable=True)
    date_enrolled = db.Column(Date, server_default=func.now(), nullable=True)

    source_id = db.Column(db.String(100), nullable=True)
    origin = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f"Dog('{self.dog_id}')"

class Vet(db.Model, UserMixin):
    """
    Vet model representing veterinarians in the system.

    Attributes:
        vet_id (int): Primary key.
        vet_email (str): Vet's email address.
        vet_password (str): Hashed password.
        vet_name (str): Vet's first name.
        vet_last_name (str): Vet's last name.
        vet_register_id (str): Vet's registration ID.
        clinic (str): Name of the vet's clinic.
        clinic_address (str): Address of the vet's clinic.
        specialty_area (str): Vet's specialty area.
        vet_date_enrolled (DateTime): Date the vet was enrolled in the system.
        no_patients (int): Number of patients the vet has.
        contact_no (str): Vet's contact number.
        experience (int): Vet's years of experience.
        software (str): Software used by the vet.
        completed_questions (int): Number of questions completed by the vet.
        onboarding (int): Onboarding status of the vet.
        role_id (int): Foreign key linking to the vet's role.
        role (relationship): Role of the vet.
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'vet'
    vet_id = db.Column(db.Integer, primary_key=True)
    vet_email = db.Column(db.String(120), nullable=False)
    vet_password = db.Column(db.String(60), nullable=False)
    vet_profile = db.Column(db.String(200), default='/static/img/inci-icon.svg')
    clinic = db.Column(db.String(200), nullable=True)
    clinic_address = db.Column(db.String(200), nullable=True)
    booking_link = db.Column(Text)
    status = db.Column(db.String(200), nullable=True)
    
    pims = db.Column(db.String(200), nullable=True)
    integrated = db.Column(db.Boolean, default=False)
    threshold_preference = db.Column(db.Integer, default=55)

    integration_practice_id = db.Column(db.String(800), nullable=True)
    
    vet_date_enrolled = db.Column(DateTime(timezone=True), server_default=func.now())
    
    contact_no = db.Column(db.String(200), nullable=True)
    last_login = db.Column(DateTime(timezone=True), server_default=func.now())

    onboarding = db.Column(db.Integer, nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='vets')
    
    def get_id(self):
        return str(self.vet_id)

    def __repr__(self):
            return f"Vet('{self.vet_email}')"

class Appointments(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'appointments'
    
    appointment_id = db.Column(db.Integer, primary_key=True)
    appointment_pims_id = db.Column(Text, nullable=True)
    vet_id = db.Column(db.Integer, db.ForeignKey('vet.vet_id'), nullable=False)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id'), nullable=False)
    dog = db.relationship('Dog', backref=db.backref('appointments', lazy=True))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    created = db.Column(Date, server_default=func.now(), nullable=False)
    updated = db.Column(Date, server_default=func.now(), nullable=False)
    status = db.Column(db.String(60), nullable=False)
    trackingStatus = db.Column(db.String(60), nullable=False)
    startTime = db.Column(Date, server_default=func.now(), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    notes = db.Column(Text, nullable=True)
    
    def __repr__(self):
            return f"Appointments('{self.appointment_id}')"

class EHRJson(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'ehr_jsons'

    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id'), nullable=False)
    dog = db.relationship('Dog', backref=db.backref('ehr_jsons', lazy=True))  # Optional relationship to access EHRs from Dog

    json_data = db.Column(db.JSON, nullable=True)  # Stores the JSON content, optional
    json_file_path = db.Column(db.String, nullable=False)  # Path to JSON file on disk or cloud
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())  # Date the JSON was created/added
    last_updated = db.Column(db.DateTime(timezone=True), server_default=func.now())  # Last update timestamp

    # Additional optional fields for metadata
    source_pdf = db.Column(db.String, nullable=True)  # Original PDF filename, if applicable
    extraction_status = db.Column(db.String(50), nullable=True)  # Status of extraction (e.g., 'completed', 'in_progress')
    accuracy = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return f"<EHRJson id={self.id} dog_id={self.dog_id} file_path={self.json_file_path}>"


class Handouts(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'handouts'
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id', ondelete="CASCADE"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('vet.vet_id', ondelete="CASCADE"), nullable=False)
    creation_date = db.Column(Date, server_default=func.now(), nullable=False)
    handout_data = db.Column(db.JSON, nullable=True)
    target_conditions = db.Column(Text, nullable=True)
    interventions = db.relationship('PatientInterventions', back_populates='handout', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Handouts('{self.id}', '{self.dog_id}', '{self.created_by}')"
    
class InterventionEffects(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'intervention_effects'
    id = db.Column(db.Integer, primary_key=True)
    patient_intervention_id = db.Column(db.Integer, db.ForeignKey('patient_interventions.id', ondelete="CASCADE"), nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=False)
    extected_effect = db.Column(db.Float, nullable=True)
    actual_effect = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), nullable=True)

    # Establish relationship back to PatientInterventions
    patient_intervention = db.relationship('PatientInterventions', back_populates='condition_effects')
    
    def __repr__(self):
        return f"InterventionEffects('{self.id}', 'Patient Intervention: {self.patient_intervention_id}', 'Condition: {self.condition_id}')"
    
class StorySlides(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'story_slides'
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('patient_stories.id', ondelete="CASCADE"), nullable=False)
    type = db.Column(Text)
    image = db.Column(Text)
    title = db.Column(Text)
    url = db.Column(Text)
    content = db.Column(db.JSON, nullable=True)
    status = db.Column(Text, nullable=False, default='created')
    seen = db.Column(db.Boolean, default=False)
    seen_date = db.Column(db.DateTime, nullable=True)
    views = db.Column(db.Integer, default=0)
    story = db.relationship('PatientStories', back_populates='story_slides')
    
    def __repr__(self):
        return f"StorySlides('{self.id}', '{self.handout_id}')"


class Condition(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'conditions'
    condition_id = db.Column(db.Integer, primary_key=True)
    
    condition_name = db.Column(db.Text, unique=True, nullable=False)
    condition_secondary_name = db.Column(db.Text, nullable=True)
    condition_umls_term = db.Column(db.Text, nullable=True)
    condition_umls_cui = db.Column(db.Text, nullable=True)
    condition_umls_def = db.Column(db.Text, nullable=True)
    condition_code = db.Column(db.Integer, nullable=True)
    condition_area = db.Column(db.Integer, nullable=True)
    
    is_chronic = db.Column(db.Boolean, nullable=True, default=None)
    can_be_cured = db.Column(db.Boolean, nullable=True)
    clinical_priority_score = db.Column(db.Float, nullable=True)

    condition_confidence = db.Column(db.Float, nullable=True)
    condition_precision = db.Column(db.Float, nullable=True)
    condition_recall = db.Column(db.Float, nullable=True)
    condition_sample = db.Column(db.Float, nullable=True)
    
    lena_nodes = db.Column(db.Boolean, nullable=True, default=False)
    supp_nodes = db.Column(db.Boolean, nullable=True, default=False)

    keywords = db.Column(db.Text, nullable=True)

    signalment = db.relationship('Signalment', secondary='condition_signalment', back_populates='condition')
    symptoms = db.relationship('Symptom', secondary='condition_symptom', back_populates='conditions')
    signs = db.relationship('Sign', secondary='condition_sign', back_populates='conditions')
    labs = db.relationship('LabTests', secondary='condition_lab', back_populates='conditions')
    
    affiliated_conditions = db.relationship(
        'Condition',
        secondary='condition_affiliated',
        primaryjoin='Condition.condition_id == ConditionAffiliated.condition_id',
        secondaryjoin='Condition.condition_id == ConditionAffiliated.affiliated_condition_id',
        back_populates='affiliated_conditions'
    )
    
    preventions = db.relationship('Prevention', secondary=prevention_condition, back_populates='conditions')
    drugs = db.relationship('Drugs', secondary=drug_condition, back_populates='conditions')
    condition_imaging = db.relationship('ConditionImaging', back_populates='condition')
    prevalence = db.Column(db.Text, nullable=True)
    status = db.Column(db.Text, nullable=True, default='Pending')
    causal_edges = db.relationship('CausalEdge', backref='condition', lazy=True, primaryjoin="Condition.condition_id == foreign(CausalEdge.target_variable)")
    
    def __repr__(self):
        return f"Condition('{self.condition_id}', '{self.condition_name}')"

class Symptom(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'symptoms'
    symptom_id = db.Column(db.Integer, primary_key=True)
    symptom_name = db.Column(db.Text, unique=True, nullable=False)
    conditions = db.relationship('Condition', secondary='condition_symptom', back_populates='symptoms')

    preventions = db.relationship('Prevention', secondary=prevention_symptom, back_populates='symptoms')

    def __repr__(self):
        return f"Symptom('{self.symptom_id}', '{self.symptom_name}')"

class Step(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=False)
    step_id = db.Column(db.String(80), nullable=False)
    attribute_type = db.Column(db.String(80), nullable=False)

class Entry(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.Integer, db.ForeignKey('step.id'), nullable=False)
    entry_id = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=True)

class Link(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=False)
    start_step_id = db.Column(db.String(80), nullable=False)
    end_step_id = db.Column(db.String(80), nullable=False)

class Signalment(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'signalments'
    signalment_id = db.Column(db.Integer, primary_key=True)
    signalment_name = db.Column(db.Text, unique=True, nullable=False)

    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'))
    condition = db.relationship('Condition', back_populates='signalment')

    def __repr__(self):
        return f"Signalment('{self.signalment_id}')"

class Sign(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'signs'
    sign_id = db.Column(db.Integer, primary_key=True)
    sign_name = db.Column(db.Text, unique=True, nullable=False)
    conditions = db.relationship('Condition', secondary='condition_sign', back_populates='signs')

    def __repr__(self):
        return f"Sign('{self.sign_id}', '{self.sign_name}')"

class LabTests(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'lab_tests'
    lab_test_id = db.Column(db.Integer, primary_key=True)
    lab_test_name = db.Column(db.Text, unique=True, nullable=False)
    lab_test_units = db.Column(db.Text, nullable=True)
    conditions = db.relationship('Condition', secondary='condition_lab', back_populates='labs')

    component_id = db.Column(db.Integer, db.ForeignKey('component.id'), nullable=True)
    
    def __repr__(self):
        return f"LabTests('{self.lab_test_id}', '{self.lab_test_name}')"

class Imaging(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'imaging'
    imaging_id = db.Column(db.Integer, primary_key=True)
    modality = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f"Imaging('{self.imaging_id}', '{self.modality}')"

class Exception(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'exceptions'
    exception_id = db.Column(db.Integer, primary_key=True)

    exception_category = db.Column(db.String(50), nullable=True)
    exception_value = db.Column(db.Text, nullable=True)
    exception_type = db.Column(db.String(50), nullable=True)

    condition_signalment_id = db.Column(db.Integer, db.ForeignKey('condition_signalment.condition_signalment_id'), nullable=True)
    condition_symptom_id = db.Column(db.Integer, db.ForeignKey('condition_symptom.condition_symptom_id'), nullable=True)
    condition_sign_id = db.Column(db.Integer, db.ForeignKey('condition_sign.condition_sign_id'), nullable=True)
    condition_lab_id = db.Column(db.Integer, db.ForeignKey('condition_lab.condition_lab_id'), nullable=True)
    condition_imaging_id = db.Column(db.Integer, db.ForeignKey('condition_imaging.condition_imaging_id'), nullable=True)
    condition_affiliated_id = db.Column(db.Integer, db.ForeignKey('condition_affiliated.id'), nullable=True)

    condition_signalment = db.relationship('ConditionSignalment', back_populates='exceptions')
    condition_symptom = db.relationship('ConditionSymptom', back_populates='exceptions')
    condition_sign = db.relationship('ConditionSign', back_populates='exceptions')
    condition_lab = db.relationship('ConditionLab', back_populates='exceptions')
    condition_imaging = db.relationship('ConditionImaging', back_populates='exceptions')
    condition_affiliated = db.relationship('ConditionAffiliated', back_populates='exceptions')

    def __repr__(self):
        return f"Exception('{self.exception_id}')"


class ConditionSignalment(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'condition_signalment'
    condition_signalment_id = db.Column(db.Integer, primary_key=True)
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=False)
    signalment_id = db.Column(db.Integer, db.ForeignKey('signalments.signalment_id'), nullable=False)

    category = db.Column(db.String(50), nullable=True)
    value = db.Column(db.Text, nullable=True)

    exceptions = db.relationship('Exception', back_populates='condition_signalment', cascade='all, delete-orphan')


    def __repr__(self):
        return f"ConditionSignalment(ID: '{self.condition_signalment_id}', Condition ID: '{self.condition_id}', Signalment ID: '{self.signalment_id}')"

class ConditionSymptom(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'condition_symptom'
    condition_symptom_id = db.Column(db.Integer, primary_key=True)
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.symptom_id'), nullable=False)

    onset = db.Column(db.String(50), nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    frequency = db.Column(db.String(50), nullable=True)
    severity = db.Column(db.String(50), nullable=True)
    triggers = db.Column(db.Text, nullable=True)
    relievers = db.Column(db.Text, nullable=True)
    associated_symptoms = db.Column(db.Text, nullable=True)
    patient_description = db.Column(db.Text, nullable=True)
    importance = db.Column(db.String(50), nullable=True)
    prevalence = db.Column(db.String(50), nullable=True)

    exceptions = db.relationship('Exception', back_populates='condition_symptom', cascade='all, delete-orphan')

    def __repr__(self):
        return f"ConditionSymptom(ID: '{self.condition_symptom_id}', Condition ID: '{self.condition_id}', Symptom ID: '{self.symptom_id}')"

class ConditionSign(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'condition_sign'
    condition_sign_id = db.Column(db.Integer, primary_key=True)
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=False)
    sign_id = db.Column(db.Integer, db.ForeignKey('signs.sign_id'), nullable=False)

    onset = db.Column(db.String(50), nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    severity = db.Column(db.String(50), nullable=True)
    importance = db.Column(db.Text, nullable=True)
    prevalence = db.Column(db.Text, nullable=True)
    value = db.Column(db.Text, nullable=True)

    exceptions = db.relationship('Exception', back_populates='condition_sign', cascade='all, delete-orphan')

    def __repr__(self):
        return f"ConditionSign(ID: '{self.condition_sign_id}', Condition ID: '{self.condition_id}', Sign ID: '{self.sign_id}')"

class ConditionLab(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'condition_lab'
    condition_lab_id = db.Column(db.Integer, primary_key=True)
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=False)
    lab_test_id = db.Column(db.Integer, db.ForeignKey('lab_tests.lab_test_id'), nullable=False)

    reference_range_low = db.Column(db.String(50), nullable=True)
    reference_range_high = db.Column(db.String(50), nullable=True)
    confirmatory_value = db.Column(db.String(50), nullable=True)

    exceptions = db.relationship('Exception', back_populates='condition_lab', cascade='all, delete-orphan')

    def __repr__(self):
        return f"ConditionLab(ID: '{self.condition_lab_id}', Condition ID: '{self.condition_id}', Lab Test ID: '{self.lab_test_id}')"

class ConditionImaging(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'condition_imaging'
    condition_imaging_id = db.Column(db.Integer, primary_key=True)
    
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=False)
    imaging_id = db.Column(db.Integer, db.ForeignKey('imaging.imaging_id'), nullable=False)
    
    imaging_technique = db.Column(db.Text, nullable=False)
    imaging_site = db.Column(db.Text, nullable=True)
    
    confirmatory_value = db.Column(db.Text, nullable=True)
    required = db.Column(db.Boolean, default=True)
    
    exceptions = db.relationship('Exception', back_populates='condition_imaging', cascade='all, delete-orphan')

    condition = db.relationship('Condition', back_populates='condition_imaging')
    
    def __repr__(self):
        return (f"ConditionImaging(ID: '{self.condition_imaging_id}', Condition ID: '{self.condition_id}', "
                f"Imaging ID: '{self.imaging_id}', Technique: '{self.imaging_technique}', Site: '{self.imaging_site}', "
                f"Confirmatory Value: '{self.confirmatory_value}', Required: '{self.required}')")
        
class ConditionAffiliated(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'condition_affiliated'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=False)
    affiliated_condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=False)

    impact_on_primary_condition = db.Column(db.Text, nullable=True)

    exceptions = db.relationship('Exception', back_populates='condition_affiliated', cascade='all, delete-orphan')

    def __repr__(self):
        return f"ConditionAffiliated(Condition ID: '{self.condition_id}', Affiliated Condition ID: '{self.affiliated_condition_id}')"


class PatientAlerts(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'patient_alerts'
    alert_id = db.Column(db.Integer, primary_key=True, unique=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id', ondelete="CASCADE"), nullable=False)
    alert_type =  db.Column(db.String(50))
    
    alert_date = db.Column(Date, nullable=True)
    
    status = db.Column(db.String(50))
    og_message = db.Column(db.Text)
    message = db.Column(db.Text)
    filename = db.Column(db.String(380))

    def __repr__(self):
        return f"PatientAlerts('{self.alert_id}', 'Dog ID: {self.dog_id}')"
    
class PatientPreventions(db.Model):
    __table_args__ = {'extend_existing': True}
    """
    Records individual instances of preventive treatments administered to a patient.

    Attributes:
        record_id (int): Primary key.
        dog_id (int): Foreign key linking to the patient (dog).
        prevention_id (int): Foreign key linking to the Preventions table.
        administered_date (Date): Date the prevention was given.
        due_date (Date): Next scheduled date or expiration.
        status (str): Status of the prevention (e.g., 'Administered', 'Due', 'Overdue').
        notes (str): Additional patient-specific notes or reactions.
        filename (str): Filename for any related documents.
    """
    __tablename__ = 'patient_preventions'
    record_id = db.Column(db.Integer, primary_key=True, unique=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id', ondelete="CASCADE"), nullable=False)
    prevention_type =  db.Column(db.String(50))

    name = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(50))
    source_id = db.Column(db.String(100), nullable=True)
    
    prevention_id = db.Column(db.Integer, db.ForeignKey('prevention.prevention_id'), nullable=True)
    reference_id = db.Column(db.Integer, nullable=True)
    
    administered_date = db.Column(Date, nullable=True)
    due_date = db.Column(Date, nullable=True)
    duration = db.Column(db.String(50))
    
    coverage_gap_days = db.Column(db.Integer, nullable=True)
    coverage_gap_type = db.Column(db.String, nullable=True)
    
    status = db.Column(db.String(50))
    
    group_hash = db.Column(db.String(180), index=True)

    def __repr__(self):
        return f"PatientPreventions('{self.record_id}', 'Dog ID: {self.dog_id}', 'Prevention ID: {self.prevention_id}')"
    
class PatientPrescriptions(db.Model):
    __table_args__ = {'extend_existing': True}
    """
    PatientPrescriptions model representing prescription records for a dog.

    Attributes:
        id (int): Primary key.
        dog_id (int): Foreign key linking to the dog.
        name (str): Name of the medication.
        strength (str): strength of the medication.
        form (str): form of the medication.
        dosage (str): Dose of the medication.
        indications (str): Diagnosis related to the prescription.
        instructions (Text): Additional notes about the prescription.
        end_date (Date): End date of the medication.
        start_date (Date): Date the prescription was issued.
        duration (str): duration of treatment.
        status (str): status of treatment.
        filename (str): Filename of the document related to the prescription.
    """

    __tablename__ = 'patient_prescriptions'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id', ondelete="CASCADE"), nullable=False)
    
    name = db.Column(db.String(180))
    strength = db.Column(db.String(180))
    form = db.Column(db.String(180))
    dosage = db.Column(db.String(180))
    instructions = db.Column(Text)
    start_date = db.Column(Date, nullable=True)
    end_date = db.Column(Date, nullable=True)
    duration = db.Column(db.String(180))
    status = db.Column(db.String(180))
    indications = db.Column(Text)
    group_hash = db.Column(db.String, index=True)
    filename = db.Column(db.String(380))
    match_score = db.Column(db.Float)

    drug_id = db.Column(db.Integer, nullable=True)
    ingredient_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"PatientPrescriptions('{self.id}')"

class PatientDiagnoses(db.Model):
    __table_args__ = {'extend_existing': True}
    """
    PatientDiagnoses model representing diagnosis records for a dog.

    Attributes:
        condition_id (int): Primary key.
        dog_id (int): Foreign key linking to the dog.
        condition_name (str): Name of the condition.
        condition_site (str): Site of the condition.
        condition_stage (str): Stage of the condition.
        condition_treatment (str): Treatment for the condition.
        condition_notes (Text): Additional notes about the condition.
        cdiagnosed_date (Date): Date the condition was diagnosed.
        condition_next (Date): Next date related to the condition.
        condition_end (Date): End date of the condition.
        filename (str): Filename of the document related to the condition.
    """
    __tablename__ = 'patient_diagnoses'
    diagnosis_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id', ondelete="CASCADE"), nullable=False)
    
    condition_name = db.Column(db.String(180))
    
    condition_site = db.Column(db.String(180))
    condition_stage = db.Column(db.String(180))
    condition_treatment = db.Column(db.String(380))
    
    diagnosis_confidence = db.Column(db.String(180))
    diagnosis_prognosis = db.Column(db.String(180))
    diagnosis_method = db.Column(db.String(180))
    
    diagnosis_date = db.Column(Date, nullable=True)
    diagnosis_next = db.Column(Date, nullable=True)
    diagnosis_end = db.Column(Date, nullable=True)
    
    group_hash = db.Column(db.String(180), index=True)
    condition_episode = db.Column(db.Integer)
    clinical_status = db.Column(db.String(64))
    
    condition_episode = db.Column(db.Integer)
    episode_start = db.Column(Date, nullable=True)
    episode_end = db.Column(Date, nullable=True)
    episode_resolved = db.Column(db.Boolean, default=False)
    
    merged = db.Column(db.Boolean, default=False)
    score =  db.Column(db.Float, nullable=True)
    
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=True)
    condition_area = db.Column(db.Integer, nullable=True)
    condition_code = db.Column(db.Integer, nullable=True)
    
    source = db.Column(db.String(380))
    
    def __repr__(self):
        return f"PatientDiagnoses('{self.diagnosis_id}')"

class PatientSymptoms(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'patient_symptoms'

    symptom_entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id', ondelete="CASCADE"), nullable=False)

    symptom_name = db.Column(db.String(180))
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.symptom_id'), nullable=True)
    
    symptom_site = db.Column(db.String(180))
    symptom_severity = db.Column(db.String(64))
    symptom_context = db.Column(db.String(180))
    
    confidence = db.Column(db.String(64))
    observed_method = db.Column(db.String(180))
    
    symptom_start = db.Column(Date)
    symptom_end = db.Column(Date)
    duration_days = db.Column(db.Integer)

    group_hash = db.Column(db.String(180), index=True)
    clinical_status = db.Column(db.String(64))
    
    source = db.Column(db.String(64))
    score = db.Column(db.Float)

    def __repr__(self):
        return f"PatientSymptoms('{self.symptom_entry_id}', '{self.symptom_name}')"


    
class PatientDiagnostics(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'patient_diagnostics'
    diagnostic_id = db.Column(db.Integer, primary_key=True, unique=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id', ondelete="CASCADE"), nullable=False)


    diagnostic_type = db.Column(db.String(50), nullable=False)  # 'lab', 'imaging', 'pathology', etc.
    panel_id = db.Column(db.Integer, db.ForeignKey('panel.id'), nullable=True)  # If lab panel
    imaging_id = db.Column(db.Integer, db.ForeignKey('imaging.imaging_id'), nullable=True)  # If imaging
    source = db.Column(db.String(100), nullable=True)  # e.g., "PiMS", "Manual", "Inferred"
    source_id = db.Column(db.Integer, nullable=True)
    
    name =  db.Column(db.String(500))
    laboratory = db.Column(db.String(100))
    
    status = db.Column(db.String(50), nullable=True)  # 'pending', 'completed', 'declined'
    result_summary = db.Column(db.Text, nullable=True)  # e.g., "Hookworms detected"
    result = db.Column(db.String(50), nullable=True)  # 'positive', 'negative', 'abnormal'

    diagnostic_date = db.Column(Date, nullable=False)
    match_score = db.Column(db.Float, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    is_confirmatory = db.Column(db.Boolean, default=False)
    is_abnormal = db.Column(db.Boolean, default=False)

    group_hash = db.Column(db.String(180), index=True)
    
    lab_results = db.relationship('PatientLabResult', backref='diagnostic', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Diagnostic {self.diagnostic_id} - {self.diagnostic_type} on {self.diagnostic_date}>"

class PatientLabResult(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'patient_lab_results'

    lab_result_id = db.Column(db.Integer, primary_key=True)
    diagnostic_id = db.Column(db.Integer, db.ForeignKey('patient_diagnostics.diagnostic_id', ondelete="CASCADE"), nullable=False)

    result_name = db.Column(db.String(100), nullable=False)
    result_value = db.Column(db.String(50), nullable=True)
    uom = db.Column(db.String(50), nullable=True)  # e.g., mg/dL, %, etc.
    reference_low = db.Column(db.String(50), nullable=True)
    reference_high = db.Column(db.String(50), nullable=True)
    reference_critical_high = db.Column(db.String(50), nullable=True)
    reference_critical_low = db.Column(db.String(50), nullable=True)
    reference_range = db.Column(db.String(100), nullable=True)

    indicator = db.Column(db.String(50), nullable=True)  # Normal, High, Low, Abnormal
    direction = db.Column(db.String(20), nullable=True)  # up/down
    is_abnormal = db.Column(db.Boolean, default=False)

    result_comment = db.Column(db.Text, nullable=True)
    date = db.Column(Date, nullable=False)
    component_id = db.Column(db.Integer, db.ForeignKey('component.id'), nullable=True)
    
    confidence_score = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return f"<LabResult {self.result_name}: {self.result_value} ({self.indicator})>"
    
class PatientRecordLink(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'patient_record_links'
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id', ondelete="CASCADE"), nullable=False)
    record_type = db.Column(db.String(50), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    target_type = db.Column(db.String(50), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    
    confidence_score = db.Column(db.Float, nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<Patient Link: {self.record_type} {self.record_id} ↔ {self.target_type} {self.target_id}>"
    
class Weights(db.Model):
    __table_args__ = {'extend_existing': True}
    """
    Weights model representing weight records for a dog.

    Attributes:
        id (int): Primary key.
        dog_id (int): Foreign key linking to the dog.
        weight (float): Weight of the dog.
        record_date (Date): Date the weight was recorded.
    """
    __tablename__ = 'weights'
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id', ondelete="CASCADE"), nullable=False)
    weight = db.Column(db.Float, nullable=False)  # Assuming weight is stored as a float
    record_date = db.Column(Date, server_default=func.now())

    def __repr__(self):
        return f"Weights('{self.id}', '{self.dog_id}')"

class PatientInterventions(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'patient_interventions'
    id = db.Column(db.Integer, primary_key=True)
    handout_id = db.Column(db.Integer, db.ForeignKey('handouts.id', ondelete="CASCADE"), nullable=False)
    
    intervention_id = db.Column(db.Integer, nullable=False)
    intervention_type = db.Column(db.String(50), nullable=True)
    intervention_name = db.Column(Text, nullable=True)
    intervention_value = db.Column(db.String(250), nullable=False)
    
    product_name = db.Column(Text, nullable=False)
    product_code = db.Column(db.String(50), nullable=False)
    product_category = db.Column(db.String(250), nullable=False)
    
    compliant = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(50), nullable=True)
    
    start_date = db.Column(Date, server_default=func.now(), nullable=True)
    
    handout = db.relationship('Handouts', back_populates='interventions')
    condition_effects = db.relationship('InterventionEffects', back_populates='patient_intervention', cascade="all, delete-orphan")

    def __repr__(self):
        return f"PatientInterventions('{self.id}', '{self.handout_id}')"

class PatientStories(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'patient_stories'
    id = db.Column(db.Integer, primary_key=True)
    handout_id = db.Column(db.Integer, db.ForeignKey('handouts.id', ondelete="CASCADE"), nullable=False)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id', ondelete="CASCADE"), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    url = db.Column(Text)
    
    status = db.Column(Text, nullable=False, default='created')
    total_slides = db.Column(db.Integer, nullable=False, default=0)
    seen_slides = db.Column(db.Integer, nullable=False, default=0)
    completion_rate = db.Column(db.Float, nullable=True, default=0.0)
    click = db.Column(db.Boolean, default=False)
    first_click_date = db.Column(db.DateTime, nullable=True)

    story_slides = db.relationship('StorySlides', back_populates='story')
    
    def __repr__(self):
        return f"PatientStories('{self.id}', 'Patient ID: {self.dog_id}', 'Handout: {self.handout_id}')"


class Codebook(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'codebook'

    id = db.Column(db.Integer, primary_key=True)
    variable = db.Column(db.String(120))
    variable_handle = db.Column(db.String(120))
    variable_label = db.Column(db.String(120))
    category = db.Column(db.String(120))
    sub_category = db.Column(db.String(120))
    variable_type = db.Column(db.String(120))
    onboarding_question = db.Column(Text)
    value_label_map = db.Column(db.JSON, nullable=True)
    
    def __repr__(self):
        return f"Codebook('{self.id}')"
    
class CausalEdge(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'causal_edges'

    id = db.Column(db.Integer, primary_key=True)
    source_variable = db.Column(db.Integer, db.ForeignKey('codebook.id'), nullable=False)
    target_variable = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=False)
    state = db.Column(db.String(120), nullable=True)
    effect_size = db.Column(db.Float, nullable=False)
    relationship_type = db.Column(db.String(50), nullable=True)
    confidence_level = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=True)
    last_updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    def __repr__(self):
        return f"CausalEdge('{self.source_variable}', '{self.target_variable}', '{self.effect_size}')"
    
    
class Prevention(db.Model):
    __table_args__ = {'extend_existing': True}
    """
    Master table for preventive treatments (vaccines, preventive meds, exams, etc.)

    Attributes:
        prevention_id (int): Primary key.
        type (str): Type of prevention (e.g., 'Vaccine', 'Medication', 'Procedure').
        type_id (int): Id of prevention item for relationship.
    """
    
    __tablename__ = 'prevention'
    prevention_id = db.Column(db.Integer, primary_key=True, unique=True)
    type = db.Column(db.String(50), nullable=False)  # Vaccine, Medication, Procedure
    reference_id = db.Column(db.Integer)
    
    conditions = db.relationship('Condition', secondary=prevention_condition, back_populates='preventions')
    symptoms = db.relationship('Symptom', secondary=prevention_symptom, back_populates='preventions')

    def __repr__(self):
        return f"Prevention('{self.type}', '{self.reference_id}')"

class Administrations(db.Model):
    __table_args__ = {'extend_existing': True}
    """
    Table to store vaccine and preventive administration records, supporting single and multi-disease preventions.

    Attributes:
        administration_id (int): Primary key.
        name (str): Name of the vaccine or preventive (e.g., 'DHPP', 'Rabies Vaccine').
        type (str): Type of administration (e.g., 'Vaccine', 'Antiparasitic').
        protocol (str): Administration protocol details.
        dosage (str): Dosage information.
        route (str): Route of administration (e.g., 'oral', 'subcutaneous').
        interval (str): Recommended interval (e.g., 'Annually').
        combination (bool): Indicator if this is a multi-disease preventive (e.g., DHPP).
        notes (str): Additional information or special instructions.
    """

    __tablename__ = 'administrations'
    administration_id = db.Column(db.Integer, primary_key=True, unique=True)
    type = db.Column(db.String(50), nullable=False)  # Vaccine, Antiparasitic, etc.
    name = db.Column(db.String(180), nullable=False)
    secondary_names = db.Column(db.String(180))
    core = db.Column(db.Boolean, default=False)
    
    target = db.Column(db.String(180))
    target_id = db.Column(db.Integer)
    
    combination = db.Column(db.Boolean, default=False)  # True if multi-disease
    notes = db.Column(db.Text)

    def __repr__(self):
        return f"Administration('{self.name}', '{self.type}', Combination: {self.combination})"

class Procedures(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'procedures'
    procedure_id = db.Column(db.Integer, primary_key=True, unique=True)
    type = db.Column(db.String(50), nullable=False)  # Vaccine, Antiparasitic, etc.
    name = db.Column(db.String(180), nullable=False)
    secondary_names = db.Column(db.String(180))
    target = db.Column(db.String(180))
    target_id = db.Column(db.Integer)
    
    def __repr__(self):
        return f"Procedures('{self.name}', '{self.type}')"


class Panel(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'panel'

    id = db.Column(db.Integer, primary_key=True)
    laboratory = db.Column(Text, nullable=True)
    name = db.Column(Text, nullable=False, unique=True)
    code = db.Column(Text, nullable=True, unique=True)
    turnaround_time = db.Column(Text, nullable=False)
    specimen_requirements = db.Column(Text, nullable=False)
    price = db.Column(db.Float, nullable=True)

    components = db.relationship('Component', secondary=panel_components, backref=db.backref('panels', lazy=True), cascade="all, delete")

    def __init__(self, laboratory, name, code, turnaround_time, specimen_requirements, price):
        self.laboratory = laboratory
        self.name = name
        self.code = code
        self.turnaround_time = turnaround_time
        self.specimen_requirements = specimen_requirements
        self.price = price

    def __repr__(self):
        return f"Panel('{self.name}', '{self.code}')"
    
class Component(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'component'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(Text, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Component('{self.name}')"


class Drugs(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'drugs'
    drug_id = db.Column(db.Integer, unique=True, primary_key=True)
    brand_name = db.Column(db.String(180))
    active_ingredient_id = db.Column(db.Integer, db.ForeignKey('active_ingredients.ingredient_id'), nullable=False)
    manufacturer = db.Column(Text)
    approved_species = db.Column(db.String(180))
    
    ingredients = relationship("ActiveIngredients", secondary=drug_ingredients, back_populates="drugs")
    dosage_forms = db.relationship("DosageForms", secondary=drug_dosage_forms, back_populates="drugs")
    dosage_infos = relationship("DosageInfo", back_populates="drug")
    
    dosage_details = db.relationship("DosageDetails", secondary="dosage_info", viewonly=True)
    drug_exceptions = db.relationship("DrugExceptions", secondary="dosage_info", viewonly=True)
    use_cases = db.relationship("UseCases", secondary="dosage_info", viewonly=True)
    
    conditions = db.relationship('Condition', secondary=drug_condition, back_populates='drugs')

class DosageForms(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'dosage_forms'
    dosage_form_id = db.Column(db.Integer, primary_key=True)
    dosage_form = db.Column(db.String(180))
    drug_id = db.Column(db.Integer, db.ForeignKey('drugs.drug_id'))

    # Relationship back to Drug
    drugs = db.relationship("Drugs", secondary=drug_dosage_forms, back_populates="dosage_forms")
    dosage_infos = relationship("DosageInfo", back_populates="dosage_form")

class DosageInfo(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'dosage_info'
    dosage_info_id = db.Column(db.Integer, primary_key=True)
    drug_id = db.Column(db.Integer, db.ForeignKey('drugs.drug_id'), nullable=False)
    dosage_form_id = db.Column(db.Integer, db.ForeignKey('dosage_forms.dosage_form_id'), nullable=False)
    dosage_text = db.Column(db.Text)

    # Relationships back to Drug and DosageForm
    drug = relationship("Drugs", back_populates="dosage_infos")
    dosage_form = relationship("DosageForms", back_populates="dosage_infos")
    dosage_details = db.relationship("DosageDetails", back_populates="dosage_info", cascade="all, delete-orphan")
    drug_exceptions = db.relationship("DrugExceptions", back_populates="dosage_info", cascade="all, delete-orphan")
    use_cases = db.relationship("UseCases", back_populates="dosage_info", cascade="all, delete-orphan")

class DosageDetails(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'dosage_details'
    dosage_details_id = db.Column(db.Integer, primary_key=True)
    dosage_info_id = db.Column(db.Integer, db.ForeignKey('dosage_info.dosage_info_id'), nullable=False)
    
    dosage_amount_value = db.Column(db.String(50))
    dosage_amount_unit = db.Column(db.String(50))
    dosage_weight_value = db.Column(db.String(50))
    dosage_weight_unit = db.Column(db.String(50))
    dosage_frequency_value = db.Column(db.String(50))
    dosage_frequency_unit = db.Column(db.String(50))
    route_of_administration = db.Column(db.String(250))
    species = db.Column(db.String(250))

    # Relationship back to DosageInfo
    dosage_info = db.relationship("DosageInfo", back_populates="dosage_details")

class DrugExceptions(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'drug_exceptions'
    exception_id = db.Column(db.Integer, primary_key=True)
    dosage_info_id = db.Column(db.Integer, db.ForeignKey('dosage_info.dosage_info_id'), nullable=False)

    exception_name = db.Column(db.String(150))
    exception_value = db.Column(Text)

    # Relationship back to DosageInfo
    dosage_info = db.relationship("DosageInfo", back_populates="drug_exceptions")

class UseCases(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'use_cases'
    use_case_id = db.Column(db.Integer, primary_key=True)
    dosage_info_id = db.Column(db.Integer, db.ForeignKey('dosage_info.dosage_info_id'), nullable=False)
    
    use_case = db.Column(db.String(180))  # Restore this original column definition
    grade = db.Column(db.String(180))
    specified_cause = db.Column(db.Text)
    purpose = db.Column(db.Text)
    description = db.Column(db.Text)
    
    target_id = db.Column(db.Integer, nullable=True)
    target_type = db.Column(db.String(150), nullable=True)
    etiology_id = db.Column(db.Integer, nullable=True)
    etiology_type = db.Column(db.String(150), nullable=True)
    
    # Relationship back to DosageInfo
    dosage_info = db.relationship("DosageInfo", back_populates="use_cases")
    
class ActiveIngredients(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'active_ingredients'
    ingredient_id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(180), unique=True)
    common_dosage_range = db.Column(db.String(180))
    common_routes = db.Column(Text)
    known_side_effects = db.Column(Text)

    drugs = relationship("Drugs", secondary=drug_ingredients, back_populates="ingredients")


class AuditLog(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(64))
    column_name = db.Column(db.String(64))
    record_id = db.Column(db.Integer)
    old_value = db.Column(Text)
    new_value = db.Column(Text)
    timestamp = db.Column(DateTime, server_default=func.now())
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id'))
    action = db.Column(db.String(64))

    def __repr__(self):
        return f"<AuditLog {self.table_name} {self.action} by {self.dog_id}>"

class WebContent(db.Model):
    """
    Holds content for website

    Attributes:
        id (int): Primary key.
        title (Text): Title of content.
        description (Text): Description of content.
        content (Text): Content itself.
        type (str): Type of content (faq, quick, blog, etc.).
        created_at (Date): Creation date and time.
        updated_at (Date): Update date and time.
        engagement_count (int): Number of clicks.
        popularity_score (float): Nimber of engagements (time-spent).
        author (str): Who wrote it.
        tags (Text): Tags.
        icon (Text): Icon name for accessing
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'web_content'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    title = db.Column(Text)
    description = db.Column(Text)
    content = db.Column(Text, nullable=True)
    type = db.Column(db.String(64))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    engagement_count = db.Column(db.Integer, default=0)
    popularity_score = db.Column(db.Float, default=0.0)
    author = db.Column(db.String(164))
    tags = db.Column(Text)
    icon = db.Column(Text)
    position = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"WebContent('{self.id}')"

class ErrorLog(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'error_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(Date, server_default=func.now(), nullable=False)
    resolved = db.Column(db.Boolean, default=False, nullable=False)
    resolved_at = db.Column(Date, nullable=True)
    
    level = db.Column(db.String(20), default='ERROR', nullable=False)  # e.g. ERROR, WARNING, INFO
    message = db.Column(db.Text, nullable=True)
    stack_trace = db.Column(db.Text, nullable=True)
    
    route = db.Column(db.String(200), nullable=True)
    function_name = db.Column(db.String(200), nullable=True)
    
    # If you want to tie to a specific vet or dog:
    vet_id = db.Column(db.Integer, db.ForeignKey('vet.vet_id'), nullable=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id'), nullable=True)
    
    def __repr__(self):
        return f"<ErrorLog id={self.id} level={self.level} resolved={self.resolved}>"

class Flag(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'flags'
    flag_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(DateTime, server_default=func.now(), nullable=True)
    status = db.Column(db.Text, nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('vet.vet_id'), nullable=False)
    reviewer_comments = db.Column(db.Text, nullable=True)
    priority = db.Column(db.Integer, nullable=True)

    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.condition_id'), nullable=False)
    entry_id = db.Column(db.Integer, nullable=False)
    entry_type = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Flag('{self.flag_id}')"
    
class Feedback(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id'), nullable=True)
    vet_id = db.Column(db.Integer, db.ForeignKey('vet.vet_id'), nullable=False)
    timestamp = db.Column(DateTime, server_default=func.now(), nullable=True)
    reported = db.Column(DateTime, server_default=func.now(), nullable=True)
    step = db.Column(db.Text, nullable=True)
    message = db.Column(db.Text, nullable=True)
    browser = db.Column(db.Text, nullable=True)
    device = db.Column(db.Text, nullable=True)
    os = db.Column(db.Text, nullable=True)
    network = db.Column(db.JSON, nullable=True)
    
    patient = db.relationship('Dog', backref='feedback')
    vet = db.relationship('Vet', backref='feedback')
    
    status = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Feedback('{self.id}')"

class ProcessingStatus(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "processing_status"

    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.String, nullable=False)
    source_dog_id = db.Column(db.String, nullable=False)
    vet_id = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    error_message = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)