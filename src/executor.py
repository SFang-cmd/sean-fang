"""
Executor Module for the Agentic AI App

This module is responsible for executing tasks and calling tools/APIs as needed
based on the plan created by the Planner.
"""

from typing import Dict, Any, List, Callable, Optional
from google import genai
import json
from rag_system import SATKnowledgeRAG

class Executor:
    """
    Executor class that handles the execution of planned tasks,
    including tool calling and result processing.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Executor with Gemini API access.
        
        Args:
            api_key (str): Google API key for Gemini access
        """
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        self.tools = {}
        self.rag_system = SATKnowledgeRAG(api_key=api_key)
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register built-in tools that the agent can use."""
        # Math and utility tools
        self.register_tool("calculator", self._calculator)
        
        # RAG-based knowledge base tools
        self.register_tool("search_knowledge", self._search_knowledge_rag)
        self.register_tool("get_context", self._get_context)
    
    def register_tool(self, tool_name: str, tool_func: Callable):
        """
        Register a new tool that the executor can use.
        
        Args:
            tool_name (str): The name of the tool
            tool_func (Callable): The function to call when using this tool
        """
        self.tools[tool_name] = tool_func
    
    def _calculator(self, expression: str) -> Dict[str, Any]:
        """Calculator tool for basic math operations."""
        try:
            # For safety, only allow basic math operations
            allowed_chars = set('0123456789+-*/()^. ')
            if all(c in allowed_chars for c in expression.replace('**', '^')):
                # Replace ^ with ** for Python
                safe_expression = expression.replace('^', '**')
                result = eval(safe_expression)
                return {"status": "success", "result": result, "expression": expression}
            else:
                return {"status": "error", "message": "Invalid characters in expression"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _search_knowledge_rag(self, query: str, subject: str = "all", max_results: int = 3) -> Dict[str, Any]:
        """Search the SAT knowledge base using RAG (semantic search)."""
        try:
            results = self.rag_system.search(
                query=query, 
                subject_filter=subject, 
                max_results=max_results
            )
            
            return {
                "status": "success",
                "query": query,
                "subject_filter": subject,
                "results_count": len(results),
                "results": results,
                "search_method": "RAG (semantic search)"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _get_context(self, query: str, subject: str = "all", max_context_length: int = 1500) -> Dict[str, Any]:
        """Get formatted context for a query using RAG."""
        try:
            context = self.rag_system.get_relevant_context(
                query=query,
                subject_filter=subject,
                max_context_length=max_context_length
            )
            
            return {
                "status": "success",
                "query": query,
                "subject_filter": subject,
                "context": context,
                "context_length": len(context)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def execute_task(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a single task using the LLM and available tools.
        
        Args:
            task (Dict[str, Any]): The task to execute
            context (Optional[Dict[str, Any]]): Additional context for execution
            
        Returns:
            Dict[str, Any]: The execution result
        """
        if context is None:
            context = {}
        
        # Prepare prompt for the LLM with the task description and available tools
        tools_description = ", ".join(self.tools.keys())
        prompt = f"""
        Execute the following task:
        
        TASK: {task['description']}
        
        Available tools: {tools_description}
        
        To use a tool, respond with JSON in the format:
        {{
            "tool": "tool_name",
            "parameters": {{...}}
        }}
        
        If no tool is needed, respond with your analysis and result directly.
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )
        
        # Process the response to check if a tool needs to be called
        try:
            response_text = response.text
            
            # Check if the response is requesting a tool call
            if "tool" in response_text.lower() and "{" in response_text:
                # Extract the JSON part from the response
                start_idx = response_text.find("{")
                end_idx = response_text.rfind("}") + 1
                json_str = response_text[start_idx:end_idx]
                
                try:
                    tool_request = json.loads(json_str)
                    tool_name = tool_request.get("tool")
                    parameters = tool_request.get("parameters", {})
                    
                    if tool_name in self.tools:
                        # Call the requested tool
                        tool_result = self.tools[tool_name](**parameters)
                        
                        # Process the tool result with the LLM
                        follow_up_prompt = f"""
                        Tool: {tool_name}
                        Result: {tool_result}
                        
                        Based on this result, complete the task:
                        TASK: {task['description']}
                        """
                        
                        follow_up_response = self.client.models.generate_content(
                            model='gemini-2.0-flash-exp',
                            contents=follow_up_prompt
                        )
                        return {
                            "status": "success",
                            "result": follow_up_response.text,
                            "tool_used": tool_name,
                            "tool_result": tool_result
                        }
                except json.JSONDecodeError:
                    # If JSON parsing fails, treat it as a direct response
                    pass
            
            # If no tool call is detected or JSON parsing failed, return the direct response
            return {
                "status": "success",
                "result": response_text,
                "tool_used": None,
                "tool_result": None
            }
                
        except Exception as e:
            print(f"Error executing task: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def execute_plan(self, plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute a full plan of tasks in sequence, handling dependencies.
        
        Args:
            plan (List[Dict[str, Any]]): The plan to execute
            
        Returns:
            List[Dict[str, Any]]: The results of each task execution
        """
        results = []
        context = {}
        
        for task in plan:
            # Execute each task and store results
            task_result = self.execute_task(task, context)
            results.append(task_result)
            
            # Update context with results for subsequent tasks
            context[f"task_{len(results)}"] = task_result
            
        return results
