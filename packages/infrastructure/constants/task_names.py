"""AI 태스크 이름 상수."""

from enum import Enum


class TaskName(str, Enum):
    """AI 태스크 이름들."""
    
    GENERATE_SIDE_JOBS = "generate_side_jobs"
    REGENERATE_SIDE_JOBS = "regenerate_side_jobs"
    GENERATE_MISSIONS = "generate_missions"
    GENERATE_MISSION_STEPS = "generate_mission_steps"
