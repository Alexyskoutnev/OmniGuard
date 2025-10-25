from enum import Enum

from pydantic import BaseModel


class RiskLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class HazardType(str, Enum):
    # FALL & HEIGHT-RELATED HAZARDS
    FALL_HAZARD = "Fall Hazard (Height)"
    TRIP_SLIP = "Trip/Slip Hazard (Ground)"
    UNSECURED_PLATFORM = "Unsecured Working Platform"

    # EQUIPMENT & COLLISION HAZARDS
    STRUCK_BY = "Struck-by (Moving Equipment/Vehicle)"
    CRUSH_PROXIMITY = "Crush/Proximity Hazard (Blind Spot)"
    DROPPED_OBJECT = "Dropped Object Hazard"
    COLLISION_RISK = "Equipment-Equipment Collision Risk"

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

    # DEFAULT/CATCH-ALL
    UNSAFE_BEHAVIOR = "Unsafe Worker Behavior/Distraction"
    OTHER_SAFETY_CONCERN = "Other Safety Concern"


class Hazard(BaseModel):
    hazard_type: HazardType
    description: str
    risk_level: RiskLevel
    recommended_actions: list[str]


class Event(BaseModel):
    video_id: str
    location_description: str
    hazards: list[Hazard]
