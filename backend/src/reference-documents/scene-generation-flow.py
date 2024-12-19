# Core Components

import boto3
import pinecone
import json
from datetime import datetime

class StoryEngine:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime')
        self.dynamodb = boto3.resource('dynamodb')
        self.s3 = boto3.client('s3')
        self.pinecone = pinecone.init()
        
    async def generate_new_scene(self, event_trigger):
        """Main pipeline for generating a new scene"""
        
        # 1. Gather Context
        context = await self.gather_story_context()
        
        # 2. Generate Scene
        scene = await self.generate_scene_content(context)
        
        # 3. Generate Image
        image = await self.generate_scene_image(scene)
        
        # 4. Update State
        await self.update_story_state(scene)
        
        # 5. Publish Content
        await self.publish_content(scene, image)
        
    async def gather_story_context(self):
        """Gather relevant context for scene generation"""
        
        # Get current story state
        story_state = self.dynamodb.Table('StoryState').get_item(
            Key={'story_id': 'current'}
        )['Item']
        
        # Generate embedding for current plot point
        current_plot = story_state['current_plot_point']
        embedding = await self._generate_embedding(current_plot)
        
        # Find similar scenes
        similar_scenes = self.pinecone.query(
            namespace='scenes',
            vector=embedding,
            top_k=3
        )
        
        # Compile context package
        return {
            'state': story_state,
            'similar_scenes': similar_scenes,
            'characters': story_state['active_characters'],
            'plot_threads': story_state['active_plots']
        }
    
    async def generate_scene_content(self, context):
        """Generate new scene using Claude"""
        
        prompt = self._construct_scene_prompt(context)
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet',
            body=json.dumps({
                "prompt": prompt,
                "max_tokens": 2000,
                "temperature": 0.7
            })
        )
        
        return json.loads(response['body'].read())['completion']
    
    async def generate_scene_image(self, scene):
        """Generate image for scene using Stable Diffusion"""
        
        image_prompt = self._extract_image_prompt(scene)
        
        response = self.bedrock.invoke_model(
            modelId='stability.stable-diffusion-xl',
            body=json.dumps({
                "text_prompts": [{"text": image_prompt}],
                "cfg_scale": 7,
                "steps": 50,
            })
        )
        
        return response['artifacts'][0]['base64']
    
    async def update_story_state(self, scene):
        """Update story state in DynamoDB and Pinecone"""
        
        # Generate embedding for new scene
        embedding = await self._generate_embedding(scene)
        
        # Update Pinecone
        self.pinecone.upsert(
            vectors=[(str(datetime.now()), embedding)],
            namespace='scenes'
        )
        
        # Update DynamoDB state
        self.dynamodb.Table('StoryState').update_item(
            Key={'story_id': 'current'},
            UpdateExpression='SET current_scene = :scene',
            ExpressionAttributeValues={':scene': scene}
        )
    
    async def publish_content(self, scene, image):
        """Publish content to website and social media"""
        
        # Save to S3
        scene_key = f'scenes/{datetime.now().isoformat()}.json'
        image_key = f'images/{datetime.now().isoformat()}.png'
        
        self.s3.put_object(
            Bucket='story-content',
            Key=scene_key,
            Body=json.dumps(scene)
        )
        
        self.s3.put_object(
            Bucket='story-content',
            Key=image_key,
            Body=image
        )
        
        # Trigger website update (Next.js revalidation)
        # Post to Twitter
        # Update WebSocket clients

    def _construct_scene_prompt(self, context):
        """Construct prompt for Claude"""
        return f"""
        Previous Scene Summary: {context['state']['current_scene']}
        Active Characters: {context['characters']}
        Active Plot Threads: {context['plot_threads']}
        World State: {context['state']['world_state']}
        
        Please generate the next scene following these requirements:
        1. Advance the plot thread: {context['state']['primary_plot']}
        2. Maintain consistency with previous events
        3. Include character development
        4. Create a vivid, memorable scene
        
        Format the scene with:
        - Setting description
        - Character interactions
        - Plot advancement
        - Emotional impact
        - Clear scene conclusion
        """

# Example Usage
async def lambda_handler(event, context):
    engine = StoryEngine()
    await engine.generate_new_scene(event)
