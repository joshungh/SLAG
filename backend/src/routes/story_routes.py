from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from ..services.auth_service import AuthService
from ..services.dynamodb_service import DynamoDBService
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
auth_service = AuthService()
db_service = DynamoDBService()

@router.post("/stories/test")
async def test_create_story(
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
) -> Dict[str, Any]:
    """
    Test endpoint to create a story with example data matching the exact structure.
    """
    try:
        # Example story data matching the provided structure
        example_story = {
            "bible": {
                "title": "Micah's Lost Sole",
                "genre": "Historical Fantasy/Comedy",
                "created": "2025-01-14T23:39:10.152396",
                "universe": {
                    "setting": "Ancient Greece with a modern twist",
                    "era": "480 BCE meets contemporary elements"
                },
                "characters": [
                    {
                        "name": "Micah",
                        "role": "Protagonist",
                        "description": "A determined young boy with one shoe who refuses to back down from any challenge",
                        "traits": None,
                        "background": None,
                        "relationships": None,
                        "arc": None
                    },
                    {
                        "name": "King Leonidas",
                        "role": "Antagonist",
                        "description": "Leader of the 300 Spartans who found and claimed Micah's lost shoe as a war trophy",
                        "traits": None,
                        "background": None,
                        "relationships": None,
                        "arc": None
                    },
                    {
                        "name": "Sandalia",
                        "role": "Supporting Character",
                        "description": "A magical cobbler who gives Micah advice on his quest",
                        "traits": None,
                        "background": None,
                        "relationships": None,
                        "arc": None
                    }
                ],
                "locations": [
                    {
                        "name": "The Hot Gates",
                        "description": "The narrow coastal passage where the Spartans have made their camp",
                        "significance": None,
                        "features": None,
                        "hazards": None,
                        "infrastructure": None
                    },
                    {
                        "name": "The Cobbler's Cave",
                        "description": "Mystical workshop where Sandalia crafts magical footwear",
                        "significance": None,
                        "features": None,
                        "hazards": None,
                        "infrastructure": None
                    },
                    {
                        "name": "The Shoelace Forest",
                        "description": "A maze-like forest where strings and laces hang from trees",
                        "significance": None,
                        "features": None,
                        "hazards": None,
                        "infrastructure": None
                    }
                ],
                "factions": [
                    {
                        "name": "The 300 Spartans",
                        "description": "Elite warriors who believe the shoe holds divine power",
                        "goals": [
                            "Defend the shoe",
                            "Maintain their honor",
                            "Protect Sparta"
                        ],
                        "relationships": {
                            "Micah": "adversarial",
                            "Athens": "hostile"
                        },
                        "resources": None,
                        "territory": None
                    },
                    {
                        "name": "The Cobbler's Guild",
                        "description": "Ancient order of magical shoemakers",
                        "goals": [
                            "Preserve shoe-making arts",
                            "Help the shoeless"
                        ],
                        "relationships": {
                            "Micah": "friendly",
                            "Spartans": "neutral"
                        },
                        "resources": None,
                        "territory": None
                    }
                ],
                "technology": [
                    {
                        "name": "The Lost Shoe",
                        "description": "A seemingly ordinary sneaker with unexpectedly magical properties",
                        "limitations": None,
                        "requirements": None,
                        "risks": None,
                        "development_stage": None
                    },
                    {
                        "name": "Enchanted Shoehorn",
                        "description": "Magical tool that helps Micah in his quest",
                        "limitations": None,
                        "requirements": None,
                        "risks": None,
                        "development_stage": None
                    }
                ],
                "timeline": {
                    "the_great_shoe_war": [
                        {
                            "year": "480 BCE",
                            "event": "Micah loses his shoe",
                            "details": "Shoe flies off during a game of kickball",
                            "impact": None,
                            "key_figures": None
                        },
                        {
                            "year": "480 BCE",
                            "event": "Spartans find the shoe",
                            "details": "Declare it a gift from the gods",
                            "impact": None,
                            "key_figures": None
                        },
                        {
                            "year": "480 BCE",
                            "event": "The Final Showdown",
                            "details": "Micah challenges the 300 to a dance-off for his shoe",
                            "impact": None,
                            "key_figures": None
                        }
                    ]
                },
                "themes": [
                    "Determination against overwhelming odds",
                    "The importance of standing up for what's yours",
                    "Don't judge a shoe by its laces",
                    "Comedy in the face of adversity"
                ],
                "notes": [
                    "Blend historical accuracy with modern elements for humor",
                    "Keep the tone light and adventurous",
                    "Include running gags about various types of footwear",
                    "Incorporate actual Greek mythology in unexpected ways"
                ],
                "social_structure": None,
                "infrastructure": None,
                "environmental_systems": None,
                "resource_management": None,
                "transportation_network": None
            },
            "framework": {
                "title": "The Last Sneaker of Sparta",
                "genre": "Historical Fantasy Comedy",
                "created": "2025-01-14T23:39:10.162013",
                "main_conflict": "A determined boy must retrieve his lost sneaker from 300 of history's most fearsome warriors who believe it's a divine artifact",
                "central_theme": "Sometimes the biggest battles are fought over the smallest things",
                "arcs": [
                    {
                        "name": "The Lost Sole",
                        "description": "Micah discovers where his shoe has ended up and seeks help",
                        "beats": [
                            {
                                "name": "The Cobbler's Prophecy",
                                "description": "Micah visits Sandalia in her mystical cave-workshop, where she reveals through a magical shoe-shine that his sneaker has been claimed by the Spartans. She gifts him an enchanted shoehorn that glows when pointed toward his lost shoe.",
                                "characters_involved": [
                                    "Micah",
                                    "Sandalia"
                                ],
                                "location": "The Cobbler's Cave"
                            }
                        ],
                        "themes": [
                            "Destiny",
                            "The beginning of adventure"
                        ],
                        "character_arcs": {
                            "Micah": "From frustrated kid to determined hero",
                            "Sandalia": "From mysterious mentor to invested ally"
                        }
                    },
                    {
                        "name": "Laces of Destiny",
                        "description": "Micah must navigate supernatural challenges to reach the Spartans",
                        "beats": [
                            {
                                "name": "The Tangled Path",
                                "description": "Micah faces the bizarre Shoelace Forest, where sentient laces try to trip and tie him up. He cleverly uses his remaining shoe as a weapon and learns to 'go with the flow' of the forest's strange physics.",
                                "characters_involved": [
                                    "Micah"
                                ],
                                "location": "The Shoelace Forest"
                            }
                        ],
                        "themes": [
                            "Adaptability",
                            "Creative problem-solving"
                        ],
                        "character_arcs": {
                            "Micah": "Learning to think outside the box"
                        }
                    },
                    {
                        "name": "The Final Standoff",
                        "description": "Micah confronts King Leonidas and the 300",
                        "beats": [
                            {
                                "name": "Dance Battle at the Gates",
                                "description": "Arriving at the Hot Gates, Micah challenges Leonidas to a dance-off for his shoe. The Spartans, impressed by his boldness, accept. What follows is an absurd but epic dance battle where Micah's modern moves clash with traditional Spartan war dances. His hopping on one foot proves surprisingly effective.",
                                "characters_involved": [
                                    "Micah",
                                    "King Leonidas",
                                    "The 300 Spartans"
                                ],
                                "location": "The Hot Gates"
                            }
                        ],
                        "themes": [
                            "David vs Goliath",
                            "Traditional vs Modern",
                            "The power of being yourself"
                        ],
                        "character_arcs": {
                            "Micah": "Proves his worth through perseverance and creativity",
                            "King Leonidas": "Learns to respect that great power can come in small packages"
                        }
                    }
                ]
            },
            "story": {
                "title": "The Last Sneaker of Sparta",
                "author": "AI Story Engine",
                "genre": "Historical Fantasy Comedy",
                "content": "The cave entrance looked more like a shoe store display gone wrong, with mismatched footwear dangling from strings that stretched across the opening. Micah ducked under a pair of worn ballet slippers and sidestepped a massive steel-toed boot as he made his way inside. The air grew thick with the mingled scents of leather polish and incense.\n\n\"Hello?\" His voice echoed against the rough stone walls. \"Sandalia?\"\n\nA warm glow emanated from deeper within the cave, and the soft tapping of hammer on leather led him forward. Around a bend, he found her hunched over a workbench, her silver hair catching the light of dozens of floating candles. Without looking up from the oxford shoe she was mending, she spoke in a voice that reminded Micah of wind through autumn leaves.\n\n\"You've lost something precious, young one.\"\n\nMicah shifted uncomfortably, his sock-clad right foot cold against the stone floor. \"My sneaker. It just... disappeared during gym class.\"\n\nSandalia finally looked up, her eyes twinkling like polished buttons. \"Nothing just disappears.\" She reached for a crystal bottle filled with an iridescent liquid. \"Show me the remaining shoe.\"\n\nMicah untied his remaining sneaker and handed it to Sandalia, who turned it over in her weathered hands. She uncorked the crystal bottle and let a single drop of the shimmering liquid fall onto the shoe's tongue. The droplet spread like quicksilver, coating the entire surface with a metallic sheen before sinking into the fabric.\n\n\"Your shoes are linked,\" she said, returning his sneaker. \"As all pairs are. The lost one has been pulled into the Shoelace Forest. If you wish to retrieve it, that's where you must go.\"\n\nShe gestured toward a narrow passageway behind her workbench. Where the stone walls met the floor, hundreds of shoelaces writhed like serpents, their aglets clicking against the rock like tiny teeth.\n\n\"But be warned,\" Sandalia added as Micah clutched his enchanted sneaker. \"The forest has a mind of its own. The laces will try to bind you, trap you, trip you. Trust in the connection between your shoes, and remember - sometimes the only way to untangle a knot is to follow its twists.\"\n\nMicah swallowed hard and stepped into the passage. The writhing laces immediately reached for his ankles, but he jumped back, swinging his sneaker like a weapon. The laces recoiled from its silvery glow, hissing as they retreated into the shadows.\n\n\"Right,\" he muttered, gripping his sneaker tighter. \"One step at a time.\" He ventured deeper into the passage, where the walls gradually gave way to towering columns made entirely of interwoven shoelaces in every color imaginable. The ground beneath his feet became a springy mesh of knotted cords, and somewhere in the distance, he heard the familiar squeak of rubber soles against a gymnasium floor.\n\nHis missing shoe was here, somewhere in this impossible place. He just had to figure out how to reach it without becoming hopelessly entangled along the way.\n\nThe squeaking grew louder as Micah ventured deeper into the Shoelace Forest, his enchanted sneaker glowing brighter with each step. Through gaps in the woven columns, he caught flashes of movement - bronze shields and crimson cloaks. The forest suddenly opened into a vast clearing, where three hundred Spartan warriors stood in perfect formation, their spears raised toward a towering gate made of interlaced leather straps.\n\nAnd there, balanced precariously atop the highest crossbeam, was his missing sneaker.\n\nKing Leonidas himself stood at the front of his men, Micah's shoe tucked under one muscled arm. The Spartan king's beard was intricately braided with shoelaces, their aglets clicking together when he spoke. \"So, you've come for this?\" He held up the sneaker. \"We found it on our sacred training grounds. Such strange armor for one's foot.\"\n\nMicah squared his shoulders, though his voice quavered slightly. \"I challenge you to a dance battle for my shoe.\"\n\nA ripple of surprised murmurs passed through the Spartan ranks. Leonidas raised an eyebrow, then threw back his head and laughed. \"Bold words from a boy with one shoe! Very well - we accept. Show us your warrior's dance, if you dare.\"\n\nThe Spartans formed a circle, their shields creating a makeshift arena. One warrior stepped forward with a drum made from stretched leather and began a thunderous beat. Leonidas moved first, performing a traditional Pyrrhic war dance, his feet stamping complex patterns while he wielded an invisible sword and shield.\n\nMicah waited for his turn, his heart pounding in time with the drum. When Leonidas finished, the boy stepped into the circle. He took a deep breath, then launched into the only dance he knew well - the routine from his school's production of \"Singin' in the Rain.\" Hopping on his one shoe-clad foot, he splashed in imaginary puddles and twirled an invisible umbrella.\n\nTo his surprise, the Spartans began to nod appreciatively at his one-footed performance. His enchanted sneaker pulsed with silver light in time with his movements, casting strange shadows that made it seem like he was dancing with multiple partners. As he spun and hopped, the shoelaces of the forest swayed in rhythm, creating a whispered accompaniment to the drum.",
                "word_count": 859,
                "framework_id": "The Last Sneaker of Sparta",
                "bible_id": "Micah's Lost Sole",
                "file_path": "s3://vmini-engine-stories-production/story/the_last_sneaker_of_sparta/20250115_072826.md",
                "created": "2025-01-15T07:28:26.853504"
            },
            "word_count": 859
        }
        
        # Extract story data for saving
        story_data = {
            "title": example_story["story"]["title"],
            "genre": example_story["story"]["genre"],
            "content": example_story["story"]["content"],
            "word_count": example_story["story"]["word_count"],
            "bible": example_story["bible"],
            "framework": example_story["framework"],
            "created_at": example_story["story"]["created"]
        }
        
        # Save to DynamoDB
        saved_story = await db_service.save_story(current_user.get('user_id'), story_data)
        
        return {
            'id': saved_story['id'],
            'message': 'Test story created successfully',
            'story': saved_story
        }
        
    except Exception as e:
        logger.error(f"Error creating test story: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create test story: {str(e)}"
        )

@router.post("/stories")
async def create_story(
    story_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
) -> Dict[str, Any]:
    """
    Create a new story and save it to DynamoDB.
    """
    try:
        # Save to DynamoDB
        saved_story = await db_service.save_story(current_user.get('user_id'), story_data)
        
        return {
            'id': saved_story['id'],
            'message': 'Story created successfully',
            'story': saved_story
        }
        
    except Exception as e:
        logger.error(f"Error creating story: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create story: {str(e)}"
        )

@router.get("/stories")
async def get_user_stories(
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
) -> Dict[str, Any]:
    """
    Get all stories for the current user.
    """
    try:
        stories = await db_service.get_user_stories(current_user.get('user_id'))
        return {
            'stories': stories,
            'count': len(stories)
        }
        
    except Exception as e:
        logger.error(f"Error getting stories: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get stories: {str(e)}"
        )

@router.get("/stories/{story_id}")
async def get_story(
    story_id: str,
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
) -> Dict[str, Any]:
    """
    Get a specific story by ID.
    """
    try:
        story = await db_service.get_story(current_user.get('user_id'), story_id)
        if not story:
            raise HTTPException(status_code=404, detail="Story not found")
            
        return story
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting story: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get story: {str(e)}"
        )

@router.delete("/stories/{story_id}")
async def delete_story(
    story_id: str,
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
) -> Dict[str, Any]:
    """
    Delete a story by ID.
    """
    try:
        success = await db_service.delete_story(current_user.get('user_id'), story_id)
        if not success:
            raise HTTPException(status_code=404, detail="Story not found")
            
        return {
            'message': 'Story deleted successfully'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting story: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete story: {str(e)}"
        ) 