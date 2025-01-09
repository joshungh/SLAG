from enum import Enum

class StoryPhase(Enum):
    INIT = "initialization"
    WORLD_BUILDING = "world_building"
    CHARACTER_DEV = "character_development"
    PLOT_OUTLINE = "plot_outline"
    DETAILED_OUTLINE = "detailed_outline"
    NARRATIVE = "narrative"
    FINAL = "final"

    @classmethod
    def get_file_extension(cls, phase: str) -> str:
        """Get the appropriate file extension for a phase"""
        if phase in [cls.NARRATIVE.value, cls.FINAL.value]:
            return "txt"
        return "json"

    @classmethod
    def validate_phase(cls, phase: str) -> bool:
        """Validate that a phase name is valid"""
        return phase in [member.value for member in cls]

    @classmethod
    def get_phase_by_value(cls, value: str) -> 'StoryPhase':
        """Get phase enum by value"""
        for phase in cls:
            if phase.value == value:
                return phase
        raise ValueError(f"Invalid phase value: {value}") 