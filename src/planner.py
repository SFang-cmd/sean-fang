"""
Planner Module for the Agentic AI App

This module is responsible for breaking down user tasks into subtasks
and planning the execution steps.
"""

from typing import List, Dict, Any
from google import genai

class Planner:
    """
    Planner class that breaks down user tasks into actionable subtasks.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Planner with Gemini API access.
        
        Args:
            api_key (str): Google API key for Gemini access
        """
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
    
    def create_plan(self, user_input: str) -> List[Dict[str, Any]]:
        """
        Create a plan by breaking down the user input into subtasks.
        
        Args:
            user_input (str): The user's request or task
            
        Returns:
            List[Dict[str, Any]]: A list of subtasks with their details
        """
        prompt = f"""
        Break down the following user task into a series of subtasks that can be executed:
        
        USER TASK: {user_input}
        
        For each subtask, provide:
        1. A clear, concise description
        2. Any required tools or APIs
        3. Dependencies on other subtasks (if any)
        
        Format your response as a JSON list of subtasks.
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )
        
        try:
            # Extract and parse the plan from the response
            # This is a simplified version - in a real app, you'd want more robust parsing
            plan_text = response.text
            # For now, we'll return a simple list with the raw response
            return [{"description": plan_text, "tools": [], "dependencies": []}]
        except Exception as e:
            print(f"Error creating plan: {e}")
            return [{"description": "Error creating plan", "tools": [], "dependencies": []}]
    
    def refine_plan(self, plan: List[Dict[str, Any]], feedback: str) -> List[Dict[str, Any]]:
        """
        Refine an existing plan based on feedback or new information.
        
        Args:
            plan (List[Dict[str, Any]]): The existing plan
            feedback (str): Feedback or new information
            
        Returns:
            List[Dict[str, Any]]: The refined plan
        """
        # This is a placeholder for plan refinement logic
        # In a real implementation, you would send the existing plan and feedback to the LLM
        # and get back a refined plan
        return plan
