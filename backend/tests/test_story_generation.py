import pytest
from src.services.story_engine_service import StoryEngineService
from src.services.story_arc_manager import StoryArcManager
from src.services.continuity_checker import ContinuityChecker
from src.models.story_schema import StoryState, PlotThread, ChapterSummary, PlotStatus, CharacterArc
from src.utils.initialize_services import initialize_services
import logging
import asyncio

logger = logging.getLogger(__name__)

@pytest.fixture
async def story_engine(rag_service):
    """Initialize story engine with awaited RAG service"""
    rag = await rag_service
    engine = await StoryEngineService.initialize(rag)
    return engine

async def get_rich_context(rag, query_params):
    """Get context from multiple namespaces"""
    contexts = {
        'unresolved_plots': [],  # Initialize empty list for first chapter
        'style': await rag.query_knowledge(
            query="Asimov and Haldeman writing style characteristics and techniques",
            filters={"type": "style_guide"},
            namespace="style_guides",
            top_k=3
        ),
        'technical': await rag.query_knowledge(
            query=f"Technical systems and specifications for {query_params.get('location', 'Station Omega')}",
            filters={"type": "technical"},
            namespace="technical",
            top_k=3
        ),
        'location': await rag.query_knowledge(
            query=f"Details about {query_params.get('location', 'Station Omega')}",
            filters={"type": "location"},
            namespace="locations",
            top_k=2
        ),
        'world': await rag.query_knowledge(
            query="Current world state and relevant background",
            filters={"type": "world_building"},
            namespace="world",
            top_k=2
        ),
        'narrative': await rag.query_knowledge(
            query=query_params.get('narrative_query', 'Story framework and crisis scenarios'),
            filters={"type": "plot_framework"},
            namespace="narrative",
            top_k=2
        )
    }
    return contexts

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
    engine = await story_engine
    
    # Simulate 5 chapters of tension
    for i in range(5):
        engine.arc_manager.tension_curve[i] = 0.2 * (i + 1)  # Rising tension
    
    analysis = await engine.arc_manager.analyze_tension_patterns(5)
    
    assert analysis["patterns"]["steady_rise"]
    assert analysis["optimal_next_tension"] > engine.arc_manager.tension_curve[4]
    assert "build_conflict" in analysis["suggested_techniques"]

@pytest.mark.asyncio
async def test_continuity_checking(story_engine):
    """Test continuity validation"""
    engine = await story_engine
    
    test_scene = {
        "content": "Dr. Chen activated the quantum resonance scanner...",
        "characters": ["Dr. James Chen"],
        "location": "Station Omega",
        "technology": ["quantum resonance scanner"]
    }
    
    issues = await engine.continuity_checker.validate_scene(
        test_scene,
        engine.story_state
    )
    
    assert len(issues) == 0, f"Unexpected continuity issues: {issues}"

@pytest.mark.asyncio
async def test_full_chapter_generation(story_engine):
    """Test generation of a complete chapter with scenes"""
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
        unresolved_plots=[],  # Initialize empty list
        unresolved_cliffhangers=[]
    )
    
    # Get initial context
    context = await get_rich_context(engine.rag, {
        "location": "Station Omega",
        "narrative_query": "Initial crisis scenarios and Fragment behavior"
    })
    
    # Generate chapter plan
    chapter_plan = await engine.chapter_handler.generate_chapter_plan(
        engine.story_state, 
        context
    )
    
    assert chapter_plan is not None, "Should generate chapter plan"
    assert chapter_plan.theme, "Chapter should have a theme"
    assert len(chapter_plan.scene_plans) > 0, "Should have scene plans"
    
    # Create output file
    with open("chapter_1_narrative.md", "w") as f:
        f.write(f"# Chapter 1: {chapter_plan.theme}\n\n")
        
        # Generate scenes sequentially
        for i, scene_plan in enumerate(chapter_plan.scene_plans, 1):
            logger.info(f"\nGenerating scene {i}/{len(chapter_plan.scene_plans)}...")
            
            try:
                # Get scene-specific context
                scene_context = await get_rich_context(engine.rag, {
                    "location": scene_plan.location,
                    "narrative_query": f"Scene development for {scene_plan.scene_type}"
                })
                
                # Generate scene
                scene = await engine.generate_scene_content(
                    scene_plan,
                    scene_context
                )
                
                # Log scene details
                logger.info(f"\n--- Scene {i} ---")
                logger.info(f"Location: {scene['location']}")
                logger.info(f"Characters: {', '.join(scene['characters'])}")
                logger.info(f"Content length: {len(scene['content'])} chars")
                
                # Write to file
                f.write(f"\n## Scene {i}\n")
                f.write(f"Location: {scene['location']}\n")
                f.write(f"Characters: {', '.join(scene['characters'])}\n\n")
                f.write(f"{scene['content']}\n")
                f.write("\n---\n")
                
                # Basic validation
                assert scene['content'], f"Scene {i} should have content"
                assert len(scene['content']) >= 200, f"Scene {i} content too short"
                assert scene['characters'], f"Scene {i} should have characters"
                assert scene['location'], f"Scene {i} should have location"
                
            except Exception as e:
                logger.error(f"Error generating scene {i}: {str(e)}")
                f.write(f"\n## Scene {i} - Generation Failed\n")
                f.write(f"Error: {str(e)}\n\n---\n")
    
    return chapter_plan

@pytest.mark.asyncio
async def test_act_transitions(story_engine):
    """Test proper handling of act transitions and tension progression"""
    engine = await story_engine
    chapter_plan, scenes = await test_full_chapter_generation(engine)
    
    # Validate tension progression
    for act_num in range(1, 5):
        act = next(a for a in chapter_plan.acts if a.act_number == act_num)
        act_scenes = [s for s in scenes if s.get('act_number') == act_num]
        
        logger.info(f"\n=== Act {act_num} Tension Analysis ===")
        logger.info(f"Target Tension: {act.tension_level}")
        
        # Calculate average scene tension
        scene_tensions = [s.get('tension_level', 0) for s in act_scenes]
        avg_tension = sum(scene_tensions) / len(scene_tensions) if scene_tensions else 0
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

@pytest.mark.asyncio
async def test_scene_indexing(story_engine):
    """Test that scenes are properly indexed after generation"""
    engine = await story_engine
    
    logger.info("\n=== Starting Scene Indexing Test ===")
    
    await engine.initialize_story(
        main_characters=["Dr. James Chen"],
        starting_location="Station Omega",
        initial_plot_thread="initial_crisis"
    )
    logger.info("Story initialized")

    # Generate first scene
    logger.info("Generating first scene...")
    scene = await engine.generate_next_scene()
    logger.info(f"Scene generated with {len(scene['content'])} characters")
    
    # Add a small delay to allow for indexing
    await asyncio.sleep(1)
    logger.info("Querying for indexed scene...")
    
    # Verify scene was indexed via semantic search
    results = await engine.rag.query_knowledge(
        query=scene["content"][:100],  # Use first 100 chars as query
        filters={
            "type": "generated_scene",
            "chapter_number": engine.story_state.current_chapter,
            "scene_number": 1
        },
        namespace=f"chapter_{engine.story_state.current_chapter}"
    )
    
    # Detailed verification
    assert len(results) > 0, "No results found for indexed scene"
    assert results[0]["metadata"]["scene_number"] == 1, f"Wrong scene number: {results[0]['metadata']['scene_number']}"
    assert results[0]["metadata"]["type"] == "generated_scene", "Wrong metadata type"
    assert results[0]["metadata"]["chapter_number"] == engine.story_state.current_chapter, "Wrong chapter number"
    
    # Verify key scene elements instead of exact content match
    retrieved_content = results[0]["metadata"]["content"]
    assert "Dr. James Chen" in retrieved_content, "Missing main character"
    assert "Fragment" in retrieved_content, "Missing key story element"
    assert len(retrieved_content) > 100, "Scene content too short"

    logger.info(f"Found {len(results)} matching scenes")
    logger.info(f"Scene metadata: {results[0]['metadata']}")
    logger.info("Scene indexing test passed")
    logger.info("=== Scene Indexing Test Complete ===\n")

@pytest.mark.asyncio
async def test_full_chapter_generation_with_output(story_engine):
    """Test complete chapter generation and output all scenes for review"""
    engine = await story_engine
    
    logger.info("\n=== Starting Full Chapter Generation Test ===")
    
    # Initialize story state
    await engine.initialize_story(
        main_characters=["Dr. James Chen"],
        starting_location="Station Omega",
        initial_plot_thread="initial_crisis"
    )
    logger.info("Story initialized")

    # Create a file to store the chapter output
    chapter_file = "chapter_1_output.md"
    with open(chapter_file, "w") as f:
        f.write("# Chapter 1: Fragment Crisis\n\n")
        
        # Generate all 48 scenes
        for scene_num in range(1, 49):
            logger.info(f"\nGenerating scene {scene_num}/48...")
            
            try:
                scene = await engine.generate_next_scene()
                
                # Verify scene was generated
                if not scene:
                    logger.error(f"Scene {scene_num} generation returned None")
                    continue
                    
                if 'content' not in scene:
                    logger.error(f"Scene {scene_num} missing content field")
                    logger.error(f"Scene data: {scene}")
                    continue

                # Write scene to file with metadata
                f.write(f"\n## Scene {scene_num}\n")
                f.write(f"Location: {scene.get('location', 'Unknown')}\n")
                f.write(f"Characters: {', '.join(scene.get('characters', []))}\n")
                if 'metadata' in scene:
                    f.write(f"Focus: {scene['metadata'].get('focus', 'Unknown')}\n")
                    f.write(f"Plot Thread: {scene['metadata'].get('plot_thread', 'Unknown')}\n")
                f.write("\n")
                f.write(scene.get('content', '[Scene content generation failed]'))
                f.write("\n\n---\n")
                
                # Log progress
                logger.info(f"Scene {scene_num} generated and written to file")
                logger.info(f"Location: {scene.get('location', 'Unknown')}")
                logger.info(f"Characters: {', '.join(scene.get('characters', []))}")
                logger.info(f"Content length: {len(scene.get('content', ''))}")
                
            except Exception as e:
                logger.error(f"Error generating scene {scene_num}: {str(e)}")
                # Write error to file
                f.write(f"\n## Scene {scene_num} - Generation Failed\n")
                f.write(f"Error: {str(e)}\n\n---\n")
                continue
            
            # Add a small delay between scenes
            await asyncio.sleep(1)
    
    logger.info(f"\nChapter generation complete. Output written to {chapter_file}")
    logger.info("=== Full Chapter Generation Test Complete ===\n")
    
    # Return the file path for review
    return chapter_file

@pytest.mark.asyncio
async def test_full_story_generation_flow():
    """Test the complete story generation process from outline to scenes"""
    # Initialize services
    services = await initialize_services()
    story_engine = await StoryEngineService.initialize(services["rag"])
    
    logger.info("\n=== Starting Full Story Generation Test ===")
    
    # Initialize story
    initialized = await story_engine.initialize_story(
        main_characters=["Dr. James Chen"],
        starting_location="Station Omega",
        initial_plot_thread="initial_crisis"
    )
    assert initialized, "Story should initialize successfully"
    logger.info("Story initialized")
    
    # Generate chapter outline
    logger.info("\n=== Generating Chapter Outline ===")
    chapter_plan = await story_engine.generate_chapter_outline()
    assert chapter_plan is not None, "Should generate chapter plan"
    assert len(chapter_plan.scene_plans) == 48, "Should have 48 scenes planned"
    
    # Generate each scene
    logger.info("\n=== Generating Scene Narratives ===")
    
    # Create output file
    with open("chapter_1_narrative.md", "w") as f:
        f.write(f"# Chapter 1: {chapter_plan.theme}\n\n")
        
        # Generate scenes sequentially
        for scene_number in range(1, 49):
            logger.info(f"\nGenerating scene {scene_number}/48...")
            
            try:
                scene = await story_engine.generate_scene_narrative(scene_number)
                
                # Log scene details
                logger.info(f"\n--- Scene {scene_number} ---")
                logger.info(f"Location: {scene['location']}")
                logger.info(f"Characters: {', '.join(scene['characters'])}")
                logger.info(f"Content length: {len(scene['content'])} chars")
                
                # Write to file
                f.write(f"\n## Scene {scene_number}\n")
                f.write(f"Location: {scene['location']}\n")
                f.write(f"Characters: {', '.join(scene['characters'])}\n\n")
                f.write(f"{scene['content']}\n")
                f.write("\n---\n")
                
                # Validate scene content
                assert scene['content'], f"Scene {scene_number} should have content"
                assert len(scene['content']) >= 100, f"Scene {scene_number} content too short"
                assert scene['characters'], f"Scene {scene_number} should have characters"
                assert scene['location'], f"Scene {scene_number} should have location"
                
            except Exception as e:
                logger.error(f"Error generating scene {scene_number}: {str(e)}")
                f.write(f"\n## Scene {scene_number} - Generation Failed\n")
                f.write(f"Error: {str(e)}\n\n---\n")

@pytest.mark.asyncio
async def test_multi_chapter_generation(story_engine):
    """Test generation of first three chapters"""
    engine = await story_engine
    chapters = []
    
    for chapter_num in range(1, 4):
        logger.info(f"\n{'='*20} Generating Chapter {chapter_num} {'='*20}")
        
        # Update story state for new chapter
        engine.story_state = StoryState(
            current_chapter=chapter_num,
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
            chapter_summaries=chapters,  # Pass previous chapters
            unresolved_plots=[],
            unresolved_cliffhangers=[]
        )
        
        # Get initial context including previous chapters
        context = await get_rich_context(engine.rag, {
            "location": "Station Omega",
            "narrative_query": f"Chapter {chapter_num} development and progression"
        })
        
        # Generate chapter plan
        chapter_plan = await engine.chapter_handler.generate_chapter_plan(
            engine.story_state, 
            context
        )
        
        assert chapter_plan is not None, f"Should generate plan for chapter {chapter_num}"
        assert chapter_plan.theme, f"Chapter {chapter_num} should have a theme"
        assert len(chapter_plan.scene_plans) > 0, f"Chapter {chapter_num} should have scene plans"
        
        # Create output file for this chapter
        with open(f"chapter_{chapter_num}_narrative.md", "w") as f:
            f.write(f"# Chapter {chapter_num}: {chapter_plan.theme}\n\n")
            
            # Generate scenes sequentially
            for i, scene_plan in enumerate(chapter_plan.scene_plans, 1):
                logger.info(f"\nGenerating scene {i}/{len(chapter_plan.scene_plans)}...")
                
                try:
                    # Get scene-specific context
                    scene_context = await get_rich_context(engine.rag, {
                        "location": scene_plan.location,
                        "narrative_query": f"Scene development for {scene_plan.scene_type}"
                    })
                    
                    # Generate scene
                    scene = await engine.generate_scene_content(
                        scene_plan,
                        scene_context
                    )
                    
                    # Log scene details
                    logger.info(f"\n--- Scene {i} ---")
                    logger.info(f"Location: {scene['location']}")
                    logger.info(f"Characters: {', '.join(scene['characters'])}")
                    logger.info(f"Content length: {len(scene['content'])} chars")
                    
                    # Write to file
                    f.write(f"\n## Scene {i}\n")
                    f.write(f"Location: {scene['location']}\n")
                    f.write(f"Characters: {', '.join(scene['characters'])}\n\n")
                    f.write(f"{scene['content']}\n")
                    f.write("\n---\n")
                    
                    # Basic validation
                    assert scene['content'], f"Scene {i} should have content"
                    assert len(scene['content']) >= 200, f"Scene {i} content too short"
                    assert scene['characters'], f"Scene {i} should have characters"
                    assert scene['location'], f"Scene {i} should have location"
                    
                except Exception as e:
                    logger.error(f"Error generating scene {i}: {str(e)}")
                    f.write(f"\n## Scene {i} - Generation Failed\n")
                    f.write(f"Error: {str(e)}\n\n---\n")
        
        # Store chapter summary for continuity
        chapters.append(ChapterSummary(
            chapter_number=chapter_num,
            theme=chapter_plan.theme,
            major_developments=[scene.expected_outcome for scene in chapter_plan.scene_plans],
            unresolved_plots=[plot for plot in engine.story_state.active_plot_threads 
                            if plot.status == PlotStatus.ACTIVE],
            character_developments=engine.story_state.character_states
        ))
        
        logger.info(f"\nCompleted Chapter {chapter_num}: {chapter_plan.theme}")
    
    return chapters