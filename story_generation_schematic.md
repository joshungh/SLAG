# SLAG (Story & Literature Auto Generation) System Design

## Overview
A recursive, RAG-enabled story generation system utilizing Claude's full 200k token capacity through multiple expansion phases.

## Generation Flow

### Phase 0: Genre Analysis & Story Bible Initialization
INPUT: User prompt (simple, web-dashboard friendly)
OUTPUT: 
- Genre-specific framework
- Initial story bible structure
- Base metadata schemas
TOKENS: 200k
RAG: Genre-specific reference documents
INDEX: Yes, story_bible namespace

### Phase 1: Universe Building (Parallel Processing)
INPUT: Genre framework from Phase 0
OUTPUT: Detailed expansions of:
1. Physical Universe
   - Locations/Worlds
   - Maps & Geography
   - Natural Laws/Physics
   
2. Civilizations
   - Political Systems
   - Economic Systems
   - Social Structures
   
3. Culture & Religion
   - Belief Systems
   - Traditions
   - Art & Entertainment
   
4. Technology
   - Tech Levels
   - Scientific Advancement
   - Innovations
   
5. Military & Conflict
   - Forces & Factions
   - Warfare Methods
   - Power Dynamics

Each category undergoes recursive expansion:
- Level 1: Basic Framework (200k tokens)
- Level 2: Detailed Expansion (200k tokens per subcategory)
- Level 3: Specific Elements (200k tokens per element)

PARALLEL PROCESSING: All categories expand simultaneously
RAG: Cross-referencing between categories
INDEX: Hierarchical namespaces for each category
STORY BIBLE: Continuous updates

### Phase 2: Character Universe
INPUT: Phase 1 output
OUTPUT: Character ecosystem
PARALLEL PROCESSING:
1. Major Characters
   - Detailed backgrounds
   - Personality profiles
   - Story arcs
   
2. Supporting Characters
   - Relationship webs
   - Role definitions
   
3. Groups & Factions
   - Internal dynamics
   - External relations

Each character/group undergoes recursive expansion similar to Phase 1
TOKENS: 200k per expansion
RAG: Full universe context
INDEX: character_universe namespace

### Phase 3: Story Framework
INPUT: Phases 0-2
OUTPUT: Three-part novel framework
TOKENS: 200k
RAG: Full story bible
INDEX: story_framework namespace

### Phase 4: Act Development
INPUT: Each part from Phase 3
OUTPUT: 4 acts per part (12 total)
TOKENS: 200k per act
RAG: Full story bible + previous acts
INDEX: story_acts namespace

### Phase 5: Chapter Development
INPUT: Each act from Phase 4
OUTPUT: 4 chapters per act (48 total)
TOKENS: 200k per chapter outline
RAG: Full story bible + all previous content
INDEX: story_chapters namespace

### Phase 6: Narrative Generation
INPUT: Each chapter from Phase 5
OUTPUT: Complete narrative text
TOKENS: 200k per chapter
RAG: Full context
INDEX: story_narrative namespace

## Story Bible & Metadata

### Story Bible Structure
- Namespace: story_bible_{story_id}
- Living document updated after each generation
- Hierarchical organization matching generation phases
- Version control for each update
- Conflict resolution system for contradictions
- Automatic cross-referencing
- Isolated per story/novel

### Metadata Schema Evolution

#### Phase 0: Base Schema Templates
- Generated based on genre analysis
- Contains expected entity types
- Defines basic relationship types
- Establishes core attributes
- Templates evolve with story development

Example Base Schema:
```json
{
    "base_templates": {
        "character": {
            "required_attributes": ["name", "role"],
            "optional_attributes": ["background", "motivation"],
            "relationship_types": ["ally", "enemy", "neutral"],
            "development_stages": ["introduced", "active", "resolved"]
        },
        "location": {
            "required_attributes": ["name", "type"],
            "optional_attributes": ["description", "significance"],
            "connection_types": ["physical", "political", "economic"]
        },
        "faction": {
            "required_attributes": ["name", "type", "alignment"],
            "optional_attributes": ["leadership", "resources"],
            "relationship_types": ["allied", "hostile", "neutral"]
        }
    }
}
```

#### Dynamic Schema Growth
- Schemas evolve during generation phases
- New attributes added based on story needs
- Relationship types expand with complexity
- Custom fields for unique story elements
- Version control for schema changes

Example Evolution:
```json
{
    "character": {
        "base_attributes": {
            "name": "string",
            "role": "enum"
        },
        "story_specific_attributes": {
            "magical_abilities": ["spell_ids"],
            "faction_loyalty": "float",
            "personal_quest": "string"
        },
        "dynamic_relationships": {
            "character_id": "string",
            "relationship_type": "enum",
            "relationship_strength": "float",
            "relationship_history": ["event_ids"]
        }
    }
}
```

### Namespace Strategy
STRUCTURE:
```
story_bible_{story_id}/
├── universe/
│   ├── physical/
│   ├── civilizations/
│   ├── culture/
│   ├── technology/
│   └── military/
├── characters/
│   ├── major/
│   ├── supporting/
│   └── factions/
├── plot/
│   ├── main_arc/
│   └── subplots/
└── timeline/
    ├── past/
    ├── present/
    └── future/
```

INDEXING:
- Each section indexed separately
- Cross-references maintain story boundaries
- Metadata evolves within story context
- Version control per section
- Conflict resolution at namespace level

## Feedback Loops

### Continuous Refinement
- Each phase can suggest updates to previous phases
- Changes propagate forward through remaining phases
- Conflicts resolved through predefined rules
- Story bible maintains consistency

### Implementation
1. Generation produces suggested updates
2. Updates evaluated for conflicts
3. Changes applied to story bible
4. Subsequent generations use updated context

## Technical Considerations

1. Parallel Processing
- Independent elements generate simultaneously
- Dependency graph manages relationships
- Results merge into story bible
- Conflict resolution system handles contradictions

2. Error Handling
- Retry logic with backoff
- Alternative generation paths
- Context preservation on failure
- Partial result handling

3. Quality Metrics
- Coherence scoring
- Consistency checking
- Genre adherence
- Character voice consistency

4. Performance
- Caching strategy for frequent contexts
- Efficient RAG retrieval
- Optimized parallel processing
- Resource allocation management