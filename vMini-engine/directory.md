Last login: Fri Jan 10 21:33:41 on ttys006
cmcoca@Mac vMini-engine % tree -L 4
.
├── Dockerfile
├── deploy
│   ├── aws
│   │   ├── deploy-infra.sh
│   │   ├── deploy-service.sh
│   │   ├── ecr.yml
│   │   ├── ecs-service.yml
│   │   ├── ecs.yml
│   │   ├── policies
│   │   │   ├── ec2-policy.json
│   │   │   ├── ecr-policy.json
│   │   │   ├── ecs-policy.json
│   │   │   ├── ecs-task-role-policy.json
│   │   │   ├── ecs-task-role-trust.json
│   │   │   ├── parameter-store-policy.json
│   │   │   ├── vmini-engine-combined-policy.json
│   │   │   ├── vmini-engine-task-role-policy.json
│   │   │   └── vpc-policy.json
│   │   ├── redis.yml
│   │   ├── requirements.txt
│   │   ├── security.yml
│   │   ├── task-definition.json
│   │   └── vpc.yml
│   └── deploy.sh
├── deployment.md
├── directory.md
├── docker-compose.yml
├── logs
│   ├── api.log
│   ├── embedding.log
│   ├── final_edit.log
│   ├── framework_generation.log
│   ├── llm.log
│   ├── orchestration.log
│   ├── story_bible.log
│   ├── story_framework.log
│   ├── story_generation.log
│   ├── story_improvement.log
│   ├── story_pipeline.log
│   └── world_generation.log
├── output
│   └── frameworks
│       └── intermediate
├── pytest.ini
├── requirements.txt
├── run.sh
├── setup.py
├── src
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   └── output
│   │       ├── bible_expansion_"area": "Artifact De_20250102_185122.json
│   │       ├── bible_expansion_"area": "Character B_20250102_183847.json
│   │       ├── bible_expansion_"area": "Character B_20250102_184934.json
│   │       ├── bible_expansion_"area": "Cultural El_20250102_185221.json
│   │       ├── bible_expansion_"area": "Faction Rel_20250102_183739.json
│   │       ├── bible_expansion_"area": "Historical _20250102_183549.json
│   │       ├── bible_expansion_"area": "Mars Colony_20250102_183445.json
│   │       ├── bible_expansion_"area": "Political S_20250102_185028.json
│   │       ├── bible_expansion_"area": "Technology _20250102_183643.json
│   │       ├── bible_expansion_"area": "Technology _20250102_184841.json
│   │       ├── bible_expansion_"detail": "Character_20250102_184953.json
│   │       ├── bible_expansion_"detail": "Mars Colo_20250102_185240.json
│   │       ├── bible_expansion_"detail": "Need more_20250102_184902.json
│   │       ├── bible_expansion_"detail": "Require m_20250102_185043.json
│   │       ├── bible_expansion_"detail": "The Beaco_20250102_185144.json
│   │       ├── bible_expansion_"details": "Main cha_20250102_183916.json
│   │       ├── bible_expansion_"details": "Need to _20250102_183505.json
│   │       ├── bible_expansion_"details": "Require _20250102_183659.json
│   │       ├── bible_expansion_"details": "Should f_20250102_183608.json
│   │       ├── bible_expansion_"details": "The rela_20250102_183801.json
│   │       ├── bible_expansion_"recommended_expansi_20250102_183407.json
│   │       ├── bible_expansion_"recommended_expansi_20250102_184815.json
│   │       ├── bible_expansion_1. Artifact details _20241228_193419.json
│   │       ├── bible_expansion_1. Detailed history _20250102_182315.json
│   │       ├── bible_expansion_1. Details on Mars c_20241229_165912.json
│   │       ├── bible_expansion_1. Expand the geolog_20241229_152519.json
│   │       ├── bible_expansion_1. Mars Base One nee_20250101_190426.json
│   │       ├── bible_expansion_1. Mars Colony Infra_20241230_061925.json
│   │       ├── bible_expansion_1. Mars Colony Infra_20250102_181046.json
│   │       ├── bible_expansion_1. Martian Colony In_20241228_192338.json
│   │       ├── bible_expansion_2. Ancient Civilizat_20250102_181102.json
│   │       ├── bible_expansion_2. Mars colony infra_20241228_193430.json
│   │       ├── bible_expansion_2. Specific technolo_20241229_165929.json
│   │       ├── bible_expansion_2. Specific technolo_20250102_182338.json
│   │       ├── bible_expansion_2. The Artifact requ_20250101_190442.json
│   │       ├── bible_expansion_2. The Meridian Devi_20241228_192350.json
│   │       ├── bible_expansion_3. Character Relatio_20250102_181121.json
│   │       ├── bible_expansion_3. Cultural dynamics_20250102_182354.json
│   │       ├── bible_expansion_3. Political structu_20241229_165945.json
│   │       ├── bible_expansion_3. Pre-Discovery His_20241228_192405.json
│   │       ├── bible_expansion_3. The relationship _20250101_190459.json
│   │       ├── bible_expansion_4. Background on pre_20250102_182416.json
│   │       ├── bible_expansion_4. Earth's Political_20250102_181143.json
│   │       ├── bible_expansion_4. Inter-Faction Pol_20241228_192423.json
│   │       ├── bible_expansion_4. More detailed his_20241229_170002.json
│   │       ├── bible_expansion_4. The 2142-2147 tim_20250101_190521.json
│   │       ├── bible_expansion_5. Alien Civilizatio_20241228_192436.json
│   │       ├── bible_expansion_5. Character backgro_20250101_190542.json
│   │       ├── bible_expansion_5. Development of Ma_20241229_170018.json
│   │       ├── bible_expansion_5. Economic system o_20250102_182435.json
│   │       ├── bible_expansion_5. Secondary Technol_20250102_181157.json
│   │       ├── bible_expansion_]_20250102_183940.json
│   │       ├── bible_expansion_]_20250102_185317.json
│   │       ├── bible_expansion_{_20250102_183355.json
│   │       ├── bible_expansion_{_20250102_183423.json
│   │       ├── bible_expansion_{_20250102_183528.json
│   │       ├── bible_expansion_{_20250102_183631.json
│   │       ├── bible_expansion_{_20250102_183725.json
│   │       ├── bible_expansion_{_20250102_183829.json
│   │       ├── bible_expansion_{_20250102_184801.json
│   │       ├── bible_expansion_{_20250102_184826.json
│   │       ├── bible_expansion_{_20250102_184921.json
│   │       ├── bible_expansion_{_20250102_185014.json
│   │       ├── bible_expansion_{_20250102_185107.json
│   │       ├── bible_expansion_{_20250102_185206.json
│   │       ├── bible_expansion_},_20250102_183516.json
│   │       ├── bible_expansion_},_20250102_183619.json
│   │       ├── bible_expansion_},_20250102_183715.json
│   │       ├── bible_expansion_},_20250102_183815.json
│   │       ├── bible_expansion_},_20250102_184912.json
│   │       ├── bible_expansion_},_20250102_185003.json
│   │       ├── bible_expansion_},_20250102_185055.json
│   │       ├── bible_expansion_},_20250102_185154.json
│   │       ├── bible_expansion_}_20250102_183929.json
│   │       ├── bible_expansion_}_20250102_183953.json
│   │       ├── bible_expansion_}_20250102_185253.json
│   │       ├── bible_expansion_}_20250102_185328.json
│   │       ├── bible_initial_20241228_192319.json
│   │       ├── bible_initial_20241228_193359.json
│   │       ├── bible_initial_20241229_152455.json
│   │       ├── bible_initial_20241229_165848.json
│   │       ├── bible_initial_20241230_061902.json
│   │       ├── bible_initial_20250101_190403.json
│   │       ├── bible_initial_20250102_181023.json
│   │       ├── bible_initial_20250102_182254.json
│   │       ├── bible_initial_20250102_183333.json
│   │       └── bible_initial_20250102_184741.json
│   ├── api
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   └── main.cpython-311.pyc
│   │   └── main.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   └── config.cpython-311.pyc
│   │   └── config.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   └── __init__.cpython-311.pyc
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   ├── location.py
│   │   │   ├── story.py
│   │   │   ├── story_bible.py
│   │   │   ├── story_framework.py
│   │   │   └── timeline.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   ├── embedding_service.py
│   │   │   ├── framework_generation_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── redis_service.py
│   │   │   ├── story_framework_service.py
│   │   │   ├── story_generation_service.py
│   │   │   ├── story_improvement_service.py
│   │   │   ├── story_orchestration_service.py
│   │   │   ├── validation_service.py
│   │   │   ├── vector_store_service.py
│   │   │   └── world_generation_service.py
│   │   └── utils
│   │       ├── __pycache__
│   │       └── logging_config.py
│   └── tests
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-311.pyc
│       │   ├── __init__.cpython-313.pyc
│       │   ├── conftest.cpython-311-pytest-7.4.3.pyc
│       │   ├── test_embedding.cpython-311-pytest-7.4.3.pyc
│       │   ├── test_final_edit.cpython-311-pytest-7.4.3.pyc
│       │   ├── test_framework_generation.cpython-311-pytest-7.4.3.pyc
│       │   ├── test_pinecone.cpython-311-pytest-7.4.3.pyc
│       │   ├── test_story_framework.cpython-311-pytest-7.4.3.pyc
│       │   ├── test_story_generation.cpython-311-pytest-7.4.3.pyc
│       │   ├── test_story_improvement.cpython-311-pytest-7.4.3.pyc
│       │   ├── test_story_orchestration.cpython-311-pytest-7.4.3.pyc
│       │   ├── test_story_pipeline.cpython-311-pytest-7.4.3.pyc
│       │   ├── test_validation.cpython-311-pytest-7.4.3.pyc
│       │   ├── test_world_generation.cpython-311-pytest-7.4.3.pyc
│       │   ├── test_world_generation.cpython-311.pyc
│       │   └── test_world_generation.cpython-313.pyc
│       ├── test_embedding.py
│       ├── test_framework_generation.py
│       ├── test_story_framework.py
│       ├── test_story_framework_isolation.py
│       ├── test_story_generation.py
│       ├── test_story_orchestration.py
│       └── test_world_generation.py
├── test.sh
├── troubleshooting.log
└── venv
    ├── bin
    │   ├── Activate.ps1
    │   ├── __pycache__
    │   │   └── jp.cpython-311.pyc
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── dotenv
    │   ├── f2py
    │   ├── jp.py
    │   ├── normalizer
    │   ├── numpy-config
    │   ├── pinecone
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.11
    │   ├── py.test
    │   ├── pytest
    │   ├── python -> python3.11
    │   ├── python3 -> python3.11
    │   ├── python3.11 -> /opt/homebrew/opt/python@3.11/bin/python3.11
    │   ├── tqdm
    │   └── uvicorn
    ├── include
    │   └── python3.11
    ├── lib
    │   └── python3.11
    │       └── site-packages
    └── pyvenv.cfg

33 directories, 207 files
cmcoca@Mac vMini-engine % 
