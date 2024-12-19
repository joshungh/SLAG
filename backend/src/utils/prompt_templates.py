class PromptTemplates:
    @staticmethod
    def get_scene_generation_prompt(context: 'FullContext') -> str:
        return f"""You are generating the next scene in an epic science fiction graphic novel. 
        The date is {context.chapter.date.strftime('%d.%m.%Y')} (2400 years in the future).

        World Context:
        {context.story.world_rules}

        Recent Events:
        {context.scene.previous_scenes[-1] if context.scene.previous_scenes else 'Chapter beginning'}

        Active Characters:
        {', '.join(context.scene.active_characters)}

        Current Situation:
        {context.scene.current_situation}

        Please generate the next scene that:
        1. Advances one or more active plot threads
        2. Maintains consistency with the established world and characters
        3. Creates vivid, cinematic moments suitable for graphic novel illustration
        4. Includes both dialogue and narrative description
        
        Format the scene with:
        - Setting description
        - Character interactions
        - Plot advancement
        - Scene conclusion
        """

    @staticmethod
    def get_image_generation_prompt(scene_text: str) -> str:
        return f"""Create a graphic novel panel in the style of AKIRA and Moebius:
        - Bold, detailed linework
        - Dynamic composition
        - Science fiction elements
        - Dramatic lighting
        
        Scene description:
        {scene_text}
        
        Style requirements:
        - High contrast
        - Strong sense of scale
        - Detailed mechanical/architectural elements
        - Cinematic framing
        """ 