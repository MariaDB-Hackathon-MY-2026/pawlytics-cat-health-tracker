"""
Data Models Module
Pydantic models for data validation and type safety
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum


# ==========================================
# ENUMS
# ==========================================

class Gender(str, Enum):
    """Cat gender enumeration"""
    MALE = "Male"
    FEMALE = "Female"
    UNKNOWN = "Unknown"


class ConditionScore(str, Enum):
    """Body condition score categories"""
    UNDERWEIGHT = "Underweight"
    IDEAL = "Ideal"
    OVERWEIGHT = "Overweight"
    OBESE = "Obese"


class ActivityLevel(str, Enum):
    """Cat activity level"""
    SEDENTARY = "Sedentary"
    MODERATE = "Moderate"
    ACTIVE = "Active"
    VERY_ACTIVE = "Very Active"


class MealTime(str, Enum):
    """Meal time categories"""
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    SNACK = "Snack"


class Appetite(str, Enum):
    """Appetite levels"""
    POOR = "Poor"
    NORMAL = "Normal"
    GOOD = "Good"
    EXCELLENT = "Excellent"


class KibbleRating(str, Enum):
    """Quality rating grades"""
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


# ==========================================
# KIBBLE MODELS
# ==========================================

class KibbleBase(BaseModel):
    """Base kibble model with common fields"""
    brand_name: str = Field(..., min_length=1, max_length=100)
    product_line: Optional[str] = Field(default="General", max_length=100)
    
    protein_pct: float = Field(..., ge=0, le=100)
    fat_pct: float = Field(..., ge=0, le=100)
    fiber_pct: float = Field(..., ge=0, le=100)
    moisture_pct: float = Field(..., ge=0, le=100)
    ash_pct: Optional[float] = Field(default=0.0, ge=0, le=100)
    
    price_per_kg: Optional[float] = Field(default=0.0, ge=0)
    
    ingredients_list: Optional[str] = None
    has_grain: Optional[bool] = False
    aafco_approved: Optional[bool] = False
    
    @validator('protein_pct', 'fat_pct', 'fiber_pct', 'moisture_pct', 'ash_pct')
    def validate_percentages(cls, v):
        """Ensure percentage values are valid"""
        if v < 0 or v > 100:
            raise ValueError("Percentage must be between 0 and 100")
        return round(v, 2)
    
    @property
    def nfe_pct(self) -> float:
        """Calculate Nitrogen-Free Extract (carbohydrates)"""
        return round(100 - (self.protein_pct + self.fat_pct + self.fiber_pct + self.moisture_pct + self.ash_pct), 2)
    
    @property
    def protein_dmb(self) -> float:
        """Calculate protein on dry matter basis"""
        if self.moisture_pct >= 100:
            return 0.0
        return round((self.protein_pct / (100 - self.moisture_pct)) * 100, 2)


class KibbleCreate(KibbleBase):
    """Model for creating new kibble entry"""
    rating: Optional[KibbleRating] = None


class KibbleResponse(KibbleBase):
    """Model for kibble API response"""
    id: int
    rating: KibbleRating
    nfe_pct: float
    protein_dmb: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==========================================
# CAT MODELS
# ==========================================

class CatBase(BaseModel):
    """Base cat model"""
    name: str = Field(..., min_length=1, max_length=50)
    age_months: int = Field(..., gt=0, le=300)
    weight_kg: float = Field(..., gt=0, le=30)
    
    gender: Gender = Gender.UNKNOWN
    neutered: bool = False
    
    condition_score: ConditionScore = ConditionScore.IDEAL
    bcs_numeric: Optional[int] = Field(default=5, ge=1, le=9)
    
    activity_level: ActivityLevel = ActivityLevel.MODERATE
    health_conditions: Optional[str] = None
    
    owner_name: Optional[str] = Field(default=None, max_length=100)
    contact_email: Optional[EmailStr] = None
    
    @validator('age_months')
    def validate_age(cls, v):
        """Validate age is reasonable"""
        if v > 300:  # ~25 years
            raise ValueError("Age seems unrealistic for a cat")
        return v
    
    @validator('weight_kg')
    def validate_weight(cls, v):
        """Validate weight is reasonable"""
        if v < 0.5 or v > 30:
            raise ValueError("Weight must be between 0.5kg and 30kg")
        return round(v, 2)
    
    @property
    def daily_calories_need(self) -> int:
        """
        Calculate Resting Energy Requirement (RER)
        Formula: 70 × (body weight in kg)^0.75
        Then multiply by activity factor
        """
        rer = 70 * (self.weight_kg ** 0.75)
        
        activity_multipliers = {
            ActivityLevel.SEDENTARY: 1.0,
            ActivityLevel.MODERATE: 1.2,
            ActivityLevel.ACTIVE: 1.4,
            ActivityLevel.VERY_ACTIVE: 1.6
        }
        
        multiplier = activity_multipliers.get(self.activity_level, 1.2)
        mer = rer * multiplier
        
        return round(mer)
    
    @property
    def age_category(self) -> str:
        """Determine life stage based on age"""
        if self.age_months < 12:
            return "Kitten"
        elif self.age_months < 96:  # < 8 years
            return "Adult"
        else:
            return "Senior"


class CatCreate(CatBase):
    """Model for creating new cat profile"""
    pass


class CatResponse(CatBase):
    """Model for cat API response"""
    id: int
    daily_calories_need: int
    age_category: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==========================================
# FEEDING LOG MODELS
# ==========================================

class FeedingLogBase(BaseModel):
    """Base feeding log model"""
    cat_id: int
    kibble_id: int
    
    date_recorded: date = Field(default_factory=date.today)
    meal_time: MealTime = MealTime.DINNER
    
    amount_grams: Optional[float] = Field(default=0, ge=0, le=1000)
    appetite: Appetite = Appetite.NORMAL
    notes: Optional[str] = None


class FeedingLogCreate(FeedingLogBase):
    """Model for creating feeding log"""
    pass


class FeedingLogResponse(FeedingLogBase):
    """Model for feeding log response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==========================================
# ANALYTICS MODELS
# ==========================================

class KibbleAnalytics(BaseModel):
    """Model for kibble analytics data"""
    id: int
    brand_name: str
    product_line: Optional[str]
    protein_pct: float
    fat_pct: float
    nfe_pct: float
    protein_dmb: float
    price_per_kg: float
    rating: KibbleRating
    cats_fed: int
    total_feedings: int
    protein_value_ratio: Optional[float]
    avg_appetite_score: Optional[float]


class CatHealthSummary(BaseModel):
    """Model for cat health summary"""
    id: int
    name: str
    age_months: int
    weight_kg: float
    condition_score: ConditionScore
    activity_level: ActivityLevel
    daily_calories_need: int
    brands_tried: int
    total_meals_logged: int
    last_feeding_date: Optional[date]
    days_since_last_log: Optional[int]


# ==========================================
# API REQUEST/RESPONSE MODELS
# ==========================================

class ScanLabelRequest(BaseModel):
    """Request model for label scanning"""
    image_base64: str
    filename: str


class ScanLabelResponse(BaseModel):
    """Response model for label scanning"""
    success: bool
    data: Optional[Dict]
    error: Optional[str]


class AnalyzeCatRequest(BaseModel):
    """Request model for cat analysis"""
    image_base64: str
    filename: str


class AnalyzeCatResponse(BaseModel):
    """Response model for cat analysis"""
    success: bool
    data: Optional[Dict]
    error: Optional[str]


# ==========================================
# VALIDATION HELPERS
# ==========================================

def validate_kibble_data(data: dict) -> tuple[bool, List[str]]:
    """
    Validate kibble data dictionary
    
    Returns:
        (is_valid, list_of_errors)
    """
    errors = []
    
    required_fields = ['brand_name', 'protein_pct', 'fat_pct', 'fiber_pct', 'moisture_pct']
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate percentages sum to ≤ 100
    if all(f in data for f in ['protein_pct', 'fat_pct', 'fiber_pct', 'moisture_pct']):
        total = sum([
            float(data['protein_pct']),
            float(data['fat_pct']),
            float(data['fiber_pct']),
            float(data['moisture_pct']),
            float(data.get('ash_pct', 0))
        ])
        
        if total > 100:
            errors.append(f"Total percentages exceed 100%: {total}%")
    
    return (len(errors) == 0, errors)


def validate_cat_data(data: dict) -> tuple[bool, List[str]]:
    """
    Validate cat profile data
    
    Returns:
        (is_valid, list_of_errors)
    """
    errors = []
    
    required_fields = ['name', 'age_months', 'weight_kg']
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate age
    if 'age_months' in data:
        age = int(data['age_months'])
        if age < 1 or age > 300:
            errors.append("Age must be between 1 and 300 months")
    
    # Validate weight
    if 'weight_kg' in data:
        weight = float(data['weight_kg'])
        if weight < 0.5 or weight > 30:
            errors.append("Weight must be between 0.5kg and 30kg")
    
    return (len(errors) == 0, errors)
