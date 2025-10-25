from enum import Enum

from pydantic import BaseModel, Field


class SafetyStatus(str, Enum):
    SAFE = "SAFE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    EXTREME = "EXTREME"


class IncidentType(str, Enum):
    # FALL & HEIGHT-RELATED HAZARDS
    FALL_HAZARD = "Fall Hazard (Height)"
    TRIP_SLIP = "Trip/Slip Hazard (Ground)"
    UNSECURED_PLATFORM = "Unsecured Working Platform"

    # EQUIPMENT & COLLISION HAZARDS
    STRUCK_BY = "Struck-by (Moving Equipment/Vehicle)"
    CRUSH_PROXIMITY = "Crush/Proximity Hazard (Blind Spot)"
    CAUGHT_IN_MACHINERY = "Caught-in/Caught-between Machinery"
    DROPPED_OBJECT = "Dropped Object Hazard"
    COLLISION_RISK = "Equipment-Equipment Collision Risk"
    EQUIPMENT_INSTABILITY = "Equipment Instability/Tip-over Risk"

    # PERSONAL PROTECTIVE EQUIPMENT (PPE) HAZARDS
    PPE_VIOLATION = "PPE Violation (Missing/Incorrect)"

    # ENERGY & UTILITY HAZARDS
    ELECTRICAL_HAZARD = "Electrical Hazard (Exposed Wire/Damage)"
    LOTO_VIOLATION = "Lockout/Tagout Violation"
    IMPROPER_LIFTING = "Improper Lifting/Rigging"
    PRESSURIZED_GAS = "Pressurized Gas/Cylinder Hazard"

    # ENVIRONMENTAL & EXPOSURE HAZARDS
    FIRE_HAZARD = "Fire/Explosion Hazard"
    CONFINED_SPACE = "Confined Space Entry Violation"
    CHEMICAL_EXPOSURE = "Chemical Exposure/Spill"
    EXCESSIVE_NOISE = "Excessive Noise Exposure"
    HEAT_COLD_STRESS = "Heat/Cold Stress"

    # MATERIAL & WORK PRACTICE HAZARDS
    IMPROPER_STORAGE = "Improper Material Storage/Stacking"
    IMPROPER_TOOL_USE = "Improper Tool Use"
    TRENCH_CAVE_IN = "Trench/Excavation Cave-in Risk"
    UNGUARDED_OPENING = "Unguarded Floor/Wall Opening"

    # INJURY & MEDICAL HAZARDS
    LACERATION_BLEEDING = "Laceration/Severe Bleeding"
    STRAIN_SPRAIN = "Muscle Strain/Sprain Injury"
    EYE_INJURY = "Eye Injury/Foreign Object"
    BURN_INJURY = "Burn/Thermal Injury"

    # Emergency & MISCELLANEOUS Hazards
    CALL_911 = "Call 911 - Emergency Services Required"
    FIRE_DEPARTMENT = "Fire Department Required"
    MEDICAL_EMERGENCY = "Medical Emergency - First Aid/Ambulance"
    EVACUATION_REQUIRED = "Evacuation Required"
    ACTIVE_FIRE = "Active Fire/Smoke"
    PERSON_DOWN = "Person Down/Injured"
    HAZMAT_INCIDENT = "Hazmat/Chemical Incident Response"
    STRUCTURAL_COLLAPSE = "Structural Collapse/Damage"

    # DEFAULT/CATCH-ALL
    UNSAFE_BEHAVIOR = "Unsafe Worker Behavior/Distraction"
    OTHER_SAFETY_CONCERN = "Other Safety Concern"
    NO_HAZARD = "No Hazard Detected"


class Predictions(BaseModel):
    probability: float = Field(
        ge=0.0, le=1.0, description="Probability of incident occurring (0.0 to 1.0)"
    )
    incident_type: IncidentType


class Event(BaseModel):
    video_id: str
    safety_status: SafetyStatus
    scene_description: str
    predictions: Predictions
    safety_response: str
