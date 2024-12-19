import pytest
from src.services.story_engine_service import StoryEngineService
from src.services.story_arc_manager import StoryArcManager
from src.services.continuity_checker import ContinuityChecker
from src.models.story_schema import StoryState, PlotThread, ChapterSummary, PlotStatus, CharacterArc
import logging

logger = logging.getLogger(__name__)

@pytest.fixture
async def story_engine(rag_service):
    """Initialize story engine with awaited RAG service"""
    engine = StoryEngineService(await rag_service)
    return engine

@pytest.mark.asyncio
async def test_chapter_generation(story_engine):
    """Test complete chapter generation flow"""
    # First await the story_engine fixture
    engine = await story_engine
    
    # Initialize story state
    engine.story_state = StoryState(
        current_chapter=1,
        current_scene=0,
        active_plot_threads=[
            PlotThread(
                id="initial_crisis",
                title="Strange Fragment Behavior",
                status=PlotStatus.ACTIVE,
                priority=1,
                related_characters=["Dr. James Chen"]
            )
        ],
        character_states={
            "Dr. James Chen": CharacterArc(
                character_id="Dr. James Chen",
                current_state="Working",
                development_goals=["Understand Fragment behavior"],
                relationships={"Commander Drake": "professional"},
                location="Station Omega"
            )
        },
        chapter_summaries=[],
        unresolved_cliffhangers=[]
    )
    
    # Generate first scene
    scene = await engine.generate_next_scene()
    
    # Add logging for debugging
    logger.info(f"Generated scene: {scene}")
    
    assert scene is not None, "Scene should not be None"
    assert "content" in scene, "Scene should have content"
    assert "characters" in scene, "Scene should have characters"
    assert "location" in scene, "Scene should have location"

@pytest.mark.asyncio
async def test_tension_curve(story_engine):
    """Test tension management"""
    arc_manager = story_engine.arc_manager
    
    # Simulate 5 chapters of tension
    for i in range(5):
        arc_manager.tension_curve[i] = 0.2 * (i + 1)  # Rising tension
    
    analysis = await arc_manager.analyze_tension_patterns(5)
    
    assert analysis["patterns"]["steady_rise"]
    assert analysis["optimal_next_tension"] > arc_manager.tension_curve[4]
    assert "build_conflict" in analysis["suggested_techniques"]

@pytest.mark.asyncio
async def test_continuity_checking(story_engine):
    """Test continuity validation"""
    test_scene = {
        "content": "Dr. Chen activated the quantum resonance scanner...",
        "characters": ["Dr. James Chen"],
        "location": "Station Omega",
        "technology": ["quantum resonance scanner"]
    }
    
    issues = await story_engine.continuity_checker.validate_scene(
        test_scene,
        story_engine.story_state
    )
    
    assert len(issues) == 0, f"Unexpected continuity issues: {issues}" 

@pytest.mark.asyncio
async def test_full_chapter_generation(story_engine):
    """Test generation of a complete chapter with 48 scenes in 4 acts"""
    engine = await story_engine
    
    # Initialize story state
    engine.story_state = StoryState(
        current_chapter=1,
        current_scene=0,
        active_plot_threads=[
            PlotThread(
                id="initial_crisis",
                title="Strange Fragment Behavior",
                status=PlotStatus.ACTIVE,
                priority=1,
                related_characters=["Dr. James Chen"]
            )
        ],
        character_states={
            "Dr. James Chen": CharacterArc(
                character_id="Dr. James Chen",
                current_state="Working",
                development_goals=["Understand Fragment behavior"],
                relationships={"Commander Drake": "professional"},
                location="Station Omega"
            ),
            "Commander Drake": CharacterArc(
                character_id="Commander Drake",
                current_state="Monitoring situation",
                development_goals=["Maintain station safety"],
                relationships={"Dr. James Chen": "professional"},
                location="Command Center"
            )
        },
        chapter_summaries=[],
        unresolved_cliffhangers=[]
    )
    
    # Generate chapter plan
    chapter_context = await engine.get_chapter_context()
    chapter_plan = await engine.chapter_handler.generate_chapter_plan(
        engine.story_state, 
        chapter_context
    )
    
    # Log chapter plan overview
    logger.info("\n=== Chapter Plan Overview ===")
    logger.info(f"Theme: {chapter_plan.theme}")
    logger.info(f"Total Scenes: {len(chapter_plan.scene_plans)}")
    
    # Log act structure
    logger.info("\n=== Act Structure ===")
    for act in chapter_plan.acts:
        logger.info(f"\nAct {act.act_number}: {act.act_theme}")
        logger.info(f"Tension Level: {act.tension_level}")
        
        # Log scenes in this act
        act_scenes = [s for s in chapter_plan.scene_plans if s.act == act.act_number]
        logger.info(f"Scenes in Act {act.act_number}: {len(act_scenes)}")
    
    # Validate act structure
    assert len(chapter_plan.acts) == 4, "Should have exactly 4 acts"
    assert len(chapter_plan.scene_plans) == 48, "Should have exactly 48 scenes"
    
    # Generate and validate all scenes
    scenes = []
    current_act = 0
    
    for scene_plan in chapter_plan.scene_plans:
        # Log act transitions
        if scene_plan.act != current_act:
            current_act = scene_plan.act
            logger.info(f"\n{'='*20} Beginning Act {current_act} {'='*20}")
            act_data = next(act for act in chapter_plan.acts if act.act_number == current_act)
            logger.info(f"Act Theme: {act_data.act_theme}")
            logger.info(f"Target Tension Level: {act_data.tension_level}")
        
        # Log scene generation
        logger.info(f"\n--- Generating Scene {scene_plan.scene_number} ---")
        logger.info(f"Type: {scene_plan.scene_type}")
        logger.info(f"Location: {scene_plan.location}")
        logger.info(f"Time: {scene_plan.time_of_day}")
        logger.info(f"Characters: {', '.join(scene_plan.key_characters)}")
        logger.info(f"Objective: {scene_plan.objective}")
        
        # Generate scene
        scene = await engine.generate_scene_content(scene_plan)
        scenes.append(scene)
        
        # Log scene content
        logger.info("\n=== Scene Content ===")
        logger.info(f"Location: {scene['location']}")
        logger.info(f"Characters: {scene['characters']}")
        logger.info("\nNarration:")
        logger.info("---")
        logger.info(scene['content'])
        logger.info("---")
        
        # Validate scene structure
        assert scene is not None, f"Scene {scene_plan.scene_number} should not be None"
        assert "content" in scene, f"Scene {scene_plan.scene_number} should have content"
        assert "characters" in scene, f"Scene {scene_plan.scene_number} should have characters"
        assert "location" in scene, f"Scene {scene_plan.scene_number} should have location"
        
        # Validate character presence
        assert all(char in scene['characters'] for char in scene_plan.key_characters), \
            f"Scene {scene_plan.scene_number} missing required characters"
    
    # Validate chapter completion
    assert len(scenes) == 48, "Should generate all 48 scenes"
    
    # Log chapter outcomes
    logger.info("\n=== Chapter Outcomes ===")
    logger.info("\nPlot Developments:")
    for dev in chapter_plan.expected_outcomes.plot_developments:
        logger.info(f"- {dev}")
    
    logger.info("\nCharacter Developments:")
    for dev in chapter_plan.expected_outcomes.character_developments:
        logger.info(f"- {dev}")
    
    logger.info("\nWorld Changes:")
    for change in chapter_plan.expected_outcomes.world_changes:
        logger.info(f"- {change}")
    
    logger.info("\nNext Chapter Setup:")
    for setup in chapter_plan.next_chapter_setup:
        logger.info(f"- {setup}")
    
    return chapter_plan, scenes

@pytest.mark.asyncio
async def test_act_transitions(story_engine):
    """Test proper handling of act transitions and tension progression"""
    engine = await story_engine
    chapter_plan, scenes = await test_full_chapter_generation(engine)
    
    # Validate tension progression
    for act_num in range(1, 5):
        act = next(a for a in chapter_plan.acts if a.act_number == act_num)
        act_scenes = [s for s in chapter_plan.scene_plans if s.act == act_num]
        
        logger.info(f"\n=== Act {act_num} Tension Analysis ===")
        logger.info(f"Target Tension: {act.tension_level}")
        
        # Calculate average scene tension
        scene_tensions = [s.tension_level for s in act_scenes]
        avg_tension = sum(scene_tensions) / len(scene_tensions)
        logger.info(f"Average Scene Tension: {avg_tension:.2f}")
        
        # Analyze tension progression
        tension_delta = scene_tensions[-1] - scene_tensions[0]
        logger.info(f"Tension Progression: {tension_delta:+.2f}")
        
        # Verify tension alignment with act structure
        if act_num < 4:  # Not the final act
            assert scene_tensions[-1] >= scene_tensions[0], \
                f"Act {act_num} should generally build tension"
        
        # Verify scene count
        assert len(act_scenes) == 12, f"Act {act_num} should have exactly 12 scenes"