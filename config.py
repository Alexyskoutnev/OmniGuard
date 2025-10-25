"""
Configuration file for Construction Safety Video Analysis with NVIDIA OmniVinci
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
MODEL_DIR = PROJECT_ROOT / "models" / "omnivinci"
DATASET_DIR = PROJECT_ROOT / "src" / "data" / "datasets"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Model configuration
OMNIVINCI_MODEL_PATH = str(MODEL_DIR)
NEMOTRON_MODEL_PATH = str(PROJECT_ROOT / "models" / "NVIDIA-Nemotron-Nano-9B-v2")

# Dataset configuration
DATASET_CONFIG = {
    "type": "local",  # "local", "huggingface", or "auto"
    "local_path": str(DATASET_DIR),
    "huggingface_dataset": None,  # e.g., "username/construction-safety-dataset"
    "huggingface_split": "train",  # train, validation, test
    "streaming": False,  # For large datasets
    "cache_dir": str(OUTPUT_DIR / "cache"),
    "validate_format": True,  # Validate dataset format
    "convert_format": True,  # Convert to training format
}

# Example HuggingFace dataset configurations
HF_DATASET_EXAMPLES = {
    "public_construction_safety": {
        "dataset_name": "your-username/construction-safety-videos",
        "description": "Construction safety video analysis dataset",
        "splits": ["train", "validation", "test"],
        "features": ["video_path", "conversation", "safety_annotations"]
    },
    "private_company_dataset": {
        "dataset_name": "company/internal-safety-dataset",
        "description": "Internal company construction safety data",
        "private": True,
        "token_required": True
    }
}

# Video processing configuration
VIDEO_CONFIG = {
    "max_frames": 128,  # OmniVinci supports up to 128 frames
    "fps": 4,  # 4 FPS for processing (balance between detail and performance)
    "resolution": (224, 224),  # Standard input resolution
    "max_duration": 30,  # Maximum video duration in seconds
}

# Audio processing configuration
AUDIO_CONFIG = {
    "sample_rate": 16000,  # Standard audio sample rate
    "max_duration": 30,  # Maximum audio duration in seconds
    "load_audio": True,  # Enable audio processing for OmniVinci
}

# Training configuration
TRAINING_CONFIG = {
    "batch_size": 1,  # Start with 1 for memory efficiency on H100
    "learning_rate": 5e-5,
    "num_epochs": 3,
    "warmup_steps": 100,
    "max_grad_norm": 1.0,
    "gradient_accumulation_steps": 8,  # Effective batch size = 8
    "save_steps": 500,
    "eval_steps": 250,
}

# Fine-tuning configuration (LoRA/QLoRA)
LORA_CONFIG = {
    "r": 16,  # LoRA rank
    "lora_alpha": 32,  # LoRA alpha
    "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"],  # Target attention modules
    "lora_dropout": 0.1,
    "bias": "none",
    "task_type": "CAUSAL_LM",
}

# Safety annotation schema
SAFETY_SCHEMA = {
    "incident_types": [
        "fall_hazard",
        "equipment_malfunction",
        "ppe_violation",
        "unsafe_behavior",
        "environmental_hazard",
        "structural_concern",
        "electrical_hazard",
        "material_handling_risk"
    ],
    "risk_levels": ["low", "medium", "high", "critical"],
    "remediation_categories": [
        "immediate_action",
        "training_required",
        "equipment_replacement",
        "policy_enforcement",
        "environmental_control",
        "supervision_increase"
    ]
}

# Construction safety prompts
SAFETY_PROMPTS = {
    "analysis": """Analyze this construction site video for safety concerns.
    Look for:
    - Workers wearing proper PPE (hard hats, safety vests, gloves, safety glasses)
    - Safe use of equipment and machinery
    - Proper scaffolding and fall protection
    - Hazardous materials handling
    - Environmental safety conditions

    Provide a structured analysis with:
    1. Current safety status
    2. Identified hazards or violations
    3. Risk assessment (low/medium/high/critical)
    4. Specific remediation recommendations
    5. Accident prediction if current conditions persist""",

    "prediction": """Based on the observed conditions in this construction video, predict potential accidents that could occur if the current situation continues. Consider factors like worker behavior, equipment condition, environmental hazards, and safety protocol adherence.""",

    "remediation": """Provide specific, actionable safety remediation steps for the hazards identified in this construction site video. Include immediate actions, training needs, equipment requirements, and policy enforcement measures."""
}

# Agent system configuration
AGENT_CONFIG = {
    "brain_model_path": NEMOTRON_MODEL_PATH,
    "enable_agents": True,
    "auto_execute_low_risk": True,
    "approval_timeout_minutes": 5,
    "max_concurrent_actions": 10,
    "log_all_actions": True,
}

# Communication system configuration
COMMUNICATION_CONFIG = {
    "sms": {
        "provider": "twilio",  # or "aws_sns"
        "account_sid": os.getenv("TWILIO_ACCOUNT_SID"),
        "auth_token": os.getenv("TWILIO_AUTH_TOKEN"),
        "from_number": os.getenv("TWILIO_FROM_NUMBER"),
        "rate_limit_per_hour": 50
    },
    "email": {
        "provider": "sendgrid",  # or "aws_ses"
        "api_key": os.getenv("SENDGRID_API_KEY"),
        "from_email": os.getenv("SENDGRID_FROM_EMAIL"),
        "rate_limit_per_hour": 100
    },
    "slack": {
        "bot_token": os.getenv("SLACK_BOT_TOKEN"),
        "webhook_url": os.getenv("SLACK_WEBHOOK_URL"),
        "default_channels": ["#safety-alerts", "#site-management"],
        "rate_limit_per_hour": 200
    },
    "teams": {
        "webhook_url": os.getenv("TEAMS_WEBHOOK_URL"),
        "rate_limit_per_hour": 200
    }
}

# Site control system configuration
SITE_CONTROL_CONFIG = {
    "alarm_system": {
        "provider": "generic_api",  # Vendor-specific integration
        "api_endpoint": os.getenv("ALARM_SYSTEM_API"),
        "api_key": os.getenv("ALARM_SYSTEM_KEY"),
        "default_alarm_duration": 30,  # seconds
        "rate_limit_per_hour": 5
    },
    "pa_system": {
        "provider": "generic_api",
        "api_endpoint": os.getenv("PA_SYSTEM_API"),
        "api_key": os.getenv("PA_SYSTEM_KEY"),
        "max_announcement_length": 200,  # characters
        "rate_limit_per_hour": 10
    }
}

# Emergency contacts and escalation
EMERGENCY_CONFIG = {
    "emergency_contacts": {
        "site_supervisor": {
            "name": "Site Supervisor",
            "phone": os.getenv("SITE_SUPERVISOR_PHONE", "+1-555-0101"),
            "email": os.getenv("SITE_SUPERVISOR_EMAIL", "supervisor@site.com"),
            "role": "immediate_response"
        },
        "safety_officer": {
            "name": "Safety Officer",
            "phone": os.getenv("SAFETY_OFFICER_PHONE", "+1-555-0102"),
            "email": os.getenv("SAFETY_OFFICER_EMAIL", "safety@site.com"),
            "role": "safety_expertise"
        },
        "management": {
            "name": "Site Management",
            "phone": os.getenv("MANAGEMENT_PHONE", "+1-555-0103"),
            "email": os.getenv("MANAGEMENT_EMAIL", "management@site.com"),
            "role": "escalation"
        },
        "emergency_services": {
            "name": "Emergency Services",
            "phone": "911",
            "role": "emergency_response"
        }
    },
    "escalation_rules": {
        "critical": ["site_supervisor", "safety_officer", "management"],
        "high": ["site_supervisor", "safety_officer"],
        "medium": ["site_supervisor"],
        "low": ["safety_officer"]
    }
}

# Approval system configuration
APPROVAL_CONFIG = {
    "auto_approve_actions": [
        "send_sms_blast",
        "send_email_alert",
        "notify_slack_teams",
        "prepare_emergency_info",
        "prepare_phone_call_info",
        "log_incident",
        "schedule_follow_up"
    ],
    "approval_timeouts": {
        "low": 30,      # 30 minutes
        "medium": 5,    # 5 minutes
        "high": 2,      # 2 minutes
        "critical": 1   # 1 minute
    },
    "approvers": {
        "site_supervisor": {
            "email": os.getenv("SITE_SUPERVISOR_EMAIL"),
            "phone": os.getenv("SITE_SUPERVISOR_PHONE"),
            "max_risk_level": "medium"
        },
        "safety_manager": {
            "email": os.getenv("SAFETY_MANAGER_EMAIL"),
            "phone": os.getenv("SAFETY_MANAGER_PHONE"),
            "max_risk_level": "high"
        },
        "emergency_coordinator": {
            "email": os.getenv("EMERGENCY_COORDINATOR_EMAIL"),
            "phone": os.getenv("EMERGENCY_COORDINATOR_PHONE"),
            "max_risk_level": "critical"
        }
    }
}

# MCP server configuration
MCP_CONFIG = {
    "server_name": "construction-safety-agent",
    "transport": "stdio",  # or "websocket"
    "host": "localhost",
    "port": 8080,
    "enable_logging": True,
    "log_level": "INFO"
}

# Ensure directories exist
def setup_directories():
    """Create necessary directories if they don't exist."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "models").mkdir(exist_ok=True)
    (OUTPUT_DIR / "logs").mkdir(exist_ok=True)
    (OUTPUT_DIR / "predictions").mkdir(exist_ok=True)

if __name__ == "__main__":
    print("Construction Safety Video Analysis Configuration")
    print("=" * 60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"OmniVinci Model: {OMNIVINCI_MODEL_PATH}")
    print(f"Dataset Directory: {DATASET_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")

    # Check if model exists
    if MODEL_DIR.exists():
        print("OmniVinci model found locally")
    else:
        print("OmniVinci model not found")

    # Check if dataset exists
    if DATASET_DIR.exists():
        videos = list(DATASET_DIR.glob("*.mp4"))
        print(f"Found {len(videos)} video files in dataset")
        for video in videos:
            print(f"   - {video.name}")
    else:
        print("Dataset directory not found")

    setup_directories()
    print("Configuration complete!")