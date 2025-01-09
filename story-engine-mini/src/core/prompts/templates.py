from typing import Dict
from ..models.story_models import StoryPhase
from ..utils.response_parser import ResponseParser
import json

class PromptTemplates:
    @staticmethod
    def create_initial_prompt(context: Dict) -> str:
        """
        Create the initial world-building prompt
        """
        return f"""You are a master storyteller tasked with creating a compelling and cohesive story. The story should be engaging, well-paced, and emotionally resonant.

Original Prompt: {context['original_prompt']}

Style Guidelines:
- Genre: {context.get('genre', 'not specified')}
- Tone: {context.get('style', {}).get('tone', 'natural')}
- Pacing: {context.get('style', {}).get('pacing', 'balanced')}
- Target Length: {context.get('target_length', 5000)} words

First, analyze the story potential and provide a structured foundation. Your response should capture the essence of what makes a great story while maintaining consistency throughout the narrative.

Please structure your response as follows:

{{
    "world_building": {{
        "setting": "Rich, atmospheric description of the world",
        "time_period": "When the story takes place and its significance",
        "atmosphere": "The emotional texture and mood that sets the tone",
        "rules": [
            "Natural laws or limitations that shape the story",
            "Magical/technological systems if applicable",
            "Social or cultural frameworks that influence characters"
        ],
        "themes": [
            "Core themes that will resonate throughout",
            "Universal truths or questions to explore"
        ]
    }},
    "story_seeds": {{
        "central_conflict": "The main tension that drives the narrative",
        "character_concepts": [
            {{
                "role": "Potential character's role in the story",
                "motivation": "What drives them",
                "arc": "How they might grow or change"
            }}
        ],
        "plot_threads": [
            {{
                "thread": "Potential storyline or subplot",
                "purpose": "How it serves the larger narrative",
                "resolution": "Possible ways it could conclude"
            }}
        ]
    }},
    "narrative_considerations": {{
        "pacing_notes": [
            "Key moments that need breathing room",
            "Sections that should move quickly"
        ],
        "emotional_beats": [
            "Critical emotional moments to hit",
            "Character relationships to develop"
        ],
        "thematic_elements": [
            "How themes will be woven through the story",
            "Symbols or motifs to employ"
        ]
    }}
}}

Focus on creating a rich foundation that will support a compelling narrative. Think about what makes stories memorable and emotionally impactful."""

    @staticmethod
    def get_max_tokens() -> int:
        """Return maximum tokens for Claude 3"""
        return 200000  # Using Claude's full context window 

    @staticmethod
    def create_character_prompt(context: Dict, world_context: str) -> str:
        """
        Create the character development prompt
        """
        world_data = ResponseParser.parse_json_response(world_context)
        story_seeds = world_data['story_seeds']
        
        return f"""Based on our established world and initial concepts, develop the characters in detail. Use the previous world-building and initial character concepts as a foundation.

Previous World Context:
{json.dumps(world_data['world_building'], indent=2)}

Initial Character Concepts:
{json.dumps(story_seeds['character_concepts'], indent=2)}

Please develop these characters fully in the following JSON structure:

{{
    "characters": [
        {{
            "name": "Character's full name",
            "role": "Role in the story",
            "physical_description": "Vivid but concise description",
            "personality": {{
                "traits": ["Key personality traits"],
                "strengths": ["Character strengths"],
                "flaws": ["Character flaws or weaknesses"],
                "quirks": ["Unique behaviors or habits"]
            }},
            "background": {{
                "history": "Relevant backstory",
                "relationships": ["Key relationships with other characters"],
                "secrets": ["Things the character is hiding or doesn't know"]
            }},
            "arc": {{
                "starting_point": "Character's initial state",
                "internal_conflict": "Personal struggles",
                "external_conflict": "Challenges from the world/others",
                "growth_points": ["Key moments of development"],
                "resolution": "How they might change by the end"
            }},
            "narrative_role": {{
                "plot_function": "How they drive the story forward",
                "thematic_purpose": "How they embody or challenge themes",
                "relationships_dynamics": ["Key relationship arcs"]
            }}
        }}
    ],
    "relationships": [
        {{
            "characters": ["Character A", "Character B"],
            "dynamic": "Nature of their relationship",
            "evolution": "How their relationship changes",
            "conflicts": ["Sources of tension"],
            "impact": "How this relationship affects the story"
        }}
    ]
}}

Focus on creating complex, believable characters whose interactions and development will drive the story forward naturally.""" 

    @staticmethod
    def create_plot_prompt(context: Dict, world_context: str, characters: str) -> str:
        """Create plot outline prompt"""
        world_data = ResponseParser.parse_json_response(world_context)
        character_data = ResponseParser.parse_json_response(characters)
        
        return f"""Based on our established world and characters, create a detailed plot outline. 
Use the previous world-building and character development as your foundation.

World Context:
{json.dumps(world_data['world_building'], indent=2)}

Characters:
{json.dumps(character_data['characters'], indent=2)}

Please structure the plot outline in the following JSON format:

{{
    "plot_structure": {{
        "hook": "Opening scene or incident that draws readers in",
        "setup": "Initial situation and context establishment",
        "rising_action": [
            {{
                "event": "Key plot event",
                "purpose": "How it drives the story",
                "characters_involved": ["Characters involved"],
                "consequences": ["Immediate and long-term effects"]
            }}
        ],
        "midpoint": {{
            "event": "Major turning point",
            "impact": "How it changes the trajectory"
        }},
        "complications": [
            {{
                "event": "Challenge or obstacle",
                "stakes": "What's at risk",
                "resolution": "How it's addressed"
            }}
        ],
        "climax": {{
            "setup": "Building to the final confrontation",
            "peak": "The highest point of tension",
            "resolution": "How the main conflict is resolved"
        }},
        "denouement": "How the story wraps up"
    }},
    "pacing": {{
        "act_structure": ["Breakdown of major story sections"],
        "tension_points": ["Moments of heightened drama"],
        "breather_moments": ["Quieter character development scenes"]
    }},
    "thematic_development": {{
        "main_theme": "Primary theme exploration",
        "supporting_themes": ["How other themes are woven in"],
        "symbolic_elements": ["Key symbols and their evolution"]
    }}
}}

Focus on creating a compelling and well-paced plot that serves both character development and thematic resonance.""" 

    @staticmethod
    def create_narrative_prompt(context: Dict, world_context: str, characters: str, plot: str) -> str:
        """Create the final narrative prompt"""
        world_data = ResponseParser.parse_json_response(world_context)
        character_data = ResponseParser.parse_json_response(characters)
        plot_data = ResponseParser.parse_json_response(plot)
        
        return f"""Using all our previous development, create the final narrative. This should be an engaging, well-paced story that brings together our world-building, characters, and plot.

World Context:
{json.dumps(world_data['world_building'], indent=2)}

Characters:
{json.dumps(character_data['characters'], indent=2)}

Plot Structure:
{json.dumps(plot_data['plot_structure'], indent=2)}

Target Length: {context.get('target_length', 5000)} words
Style: {json.dumps(context.get('style', {}), indent=2)}

Create a compelling narrative that:
1. Follows the plot structure while allowing for organic development
2. Shows character growth through action and dialogue
3. Weaves in themes naturally
4. Maintains consistent pacing
5. Creates emotional investment

The story should feel cohesive and engaging, with each scene serving the larger narrative.""" 

    @staticmethod
    def create_completion_prompt(context: Dict, partial_story: str) -> str:
        """Create prompt to complete partial story"""
        return f"""Please complete this story, maintaining the same style and tone. 
The story so far:

{partial_story}

Continue and conclude the story naturally, resolving all plot threads and character arcs.
Target length: {context.get('target_length', 3000)} words
Style: {json.dumps(context.get('style', {}), indent=2)}""" 

    def create_opening_prompt(self, context: Dict, world_context: str, characters: str, plot_hook: str, plot_setup: str) -> str:
        """Create prompt for story opening"""
        return f"""Based on the following story context, write the opening section of the story. 
        Focus on establishing the hook and setup.

        World Context:
        {world_context}

        Characters:
        {characters}

        Hook:
        {plot_hook}

        Setup:
        {plot_setup}

        Style Guide:
        - Genre: {context.get('genre', 'general')}
        - Tone: {context.get('style', {}).get('tone', 'natural')}
        - Voice: {context.get('style', {}).get('voice', 'neutral')}

        Write an engaging opening that introduces the main character, establishes the setting, 
        and sets up the initial conflict. End this section at a natural transition point."""

    def create_scene_prompt(self, context: Dict, previous_text: str, scene_info: Dict, characters: str) -> str:
        """Create prompt for a scene"""
        return f"""Continue the story with the following scene, maintaining continuity with the previous section.

        Previous Section (ending):
        {previous_text[-500:]}  # Last 500 chars for context

        Scene to Write:
        Event: {scene_info['event']}
        Purpose: {scene_info['purpose']}
        Characters Involved: {', '.join(scene_info['characters_involved'])}

        Character Details:
        {characters}

        Write this scene with attention to:
        - Maintaining consistent character voices
        - Building tension
        - Natural transitions
        - Advancing the plot through {scene_info['purpose']}

        End the scene at a natural transition point."""

    def create_climax_prompt(self, context: Dict, previous_text: str, climax_info: Dict, characters: str) -> str:
        """Create prompt for story climax"""
        return f"""Write the climactic scene of the story, building from the previous section.

        Previous Section (ending):
        {previous_text[-500:]}

        Climax Information:
        Setup: {climax_info['setup']}
        Peak Moment: {climax_info['peak']}
        Resolution: {climax_info['resolution']}

        Character Details:
        {characters}

        Write the climax with:
        - Maximum dramatic tension
        - Character decisions that reflect their arcs
        - Clear stakes and consequences
        - Emotional resonance

        This should be the story's highest point of tension."""

    def create_resolution_prompt(self, context: Dict, previous_text: str, resolution_info: str, characters: str) -> str:
        """Create prompt for story resolution"""
        return f"""Write the resolution of the story, following the climax.

        Previous Section (ending):
        {previous_text[-500:]}

        Resolution/Denouement:
        {resolution_info}

        Character Details:
        {characters}

        Write the resolution with:
        - Emotional satisfaction
        - Tie up of major plot threads
        - Character growth demonstration
        - Thematic resonance

        End with a clear sense of completion.""" 

    def create_detailed_outline_prompt(self, context: Dict, world_context: str, characters: str, plot: str) -> str:
        """Create prompt for detailed story outline"""
        return f"""Based on our world-building, characters, and basic plot, create a detailed story outline.
        Break down the story into specific scenes and chapters, tracking character arcs and plot threads.

        World Context:
        {world_context}

        Characters:
        {characters}

        Basic Plot:
        {plot}

        Create a detailed outline following this structure:

        {{
            "title": "Story title",
            "hook": "Opening hook description",
            "central_conflict": "Main conflict description",
            "themes": ["Theme 1", "Theme 2"...],
            "chapters": [
                {{
                    "number": 1,
                    "title": "Chapter title",
                    "theme": "Chapter's thematic focus",
                    "scenes": [
                        {{
                            "id": "1.1",
                            "title": "Scene title",
                            "pov_character": "POV character name",
                            "setting": "Scene location and atmosphere",
                            "time": "Time of day/story timeline point",
                            "goal": "Scene objective",
                            "conflict": "Scene's main tension",
                            "outcome": "Scene resolution",
                            "emotional_tone": "Scene's emotional atmosphere",
                            "key_details": [
                                "Important story elements to include",
                                "Specific sensory details",
                                "Key dialogue points"
                            ],
                            "characters_present": ["Character names"],
                            "plot_points": [
                                "Specific plot developments",
                                "Character revelations",
                                "Story progression points"
                            ],
                            "transitions": {{
                                "previous": "Hook to previous scene",
                                "next": "Lead-in to next scene"
                            }}
                        }}
                    ],
                    "story_arc_point": "Position in overall story arc",
                    "character_arcs": {{
                        "Character Name": "Development in this chapter"
                    }}
                }}
            ],
            "character_arcs": {{
                "Character Name": {{
                    "starting_point": "Initial state",
                    "development_points": ["Key moments"],
                    "resolution": "Final state"
                }}
            }},
            "plot_threads": {{
                "Thread Name": [
                    {{
                        "scene_id": "1.1",
                        "development": "What happens",
                        "impact": "Effect on story"
                    }}
                ]
            }},
            "story_beats": [
                {{
                    "beat": "Story beat description",
                    "purpose": "Beat's narrative function",
                    "chapter": 1,
                    "scene": "1.1"
                }}
            ],
            "resolution_points": [
                "Key elements that need resolution",
                "Character arc completions",
                "Theme resolutions"
            ]
        }}

        Ensure each scene advances both plot and character development while maintaining narrative tension.""" 