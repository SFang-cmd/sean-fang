"""
Memory Module for the Agentic AI App

This module is responsible for storing and retrieving context and information
across interactions with the agent.
"""

import os
import json
import datetime
from typing import Dict, Any, List, Optional
import numpy as np
from pathlib import Path

class Memory:
    """
    Memory class for storing and retrieving information across interactions.
    
    This implementation provides:
    1. Short-term working memory (in-memory storage)
    2. Long-term storage (file-based)
    3. Simple vector embedding for semantic retrieval
    """
    
    def __init__(self, storage_dir: str = "./memory_storage"):
        """
        Initialize the Memory module.
        
        Args:
            storage_dir (str): Directory to store persistent memory
        """
        self.storage_dir = storage_dir
        Path(storage_dir).mkdir(parents=True, exist_ok=True)
        
        # Short-term (session) memory
        self.working_memory = []
        
        # Placeholder for vector store (would use a real embedding model in production)
        self.vectors = []
        self.memories = []
    
    def store(self, item: Dict[str, Any], permanent: bool = False) -> str:
        """
        Store an item in memory.
        
        Args:
            item (Dict[str, Any]): The information to store
            permanent (bool): Whether to store in long-term memory
            
        Returns:
            str: The ID of the stored memory
        """
        # Add timestamp and generate ID
        timestamp = datetime.datetime.now().isoformat()
        memory_id = f"mem_{len(self.working_memory)}_{timestamp}"
        
        # Add metadata
        memory_item = {
            "id": memory_id,
            "timestamp": timestamp,
            "content": item,
        }
        
        # Add to working memory
        self.working_memory.append(memory_item)
        
        # Simple mock vector embedding (just use the memory_id as a stand-in)
        # In a real implementation, we would use an embedding model here
        mock_vector = np.random.rand(128)  # Random 128-dim vector as a placeholder
        self.vectors.append(mock_vector)
        self.memories.append(memory_item)
        
        # Store permanently if requested
        if permanent:
            self._save_to_disk(memory_item)
        
        return memory_id
    
    def retrieve_by_id(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific memory by ID.
        
        Args:
            memory_id (str): The ID of the memory to retrieve
            
        Returns:
            Optional[Dict[str, Any]]: The retrieved memory or None if not found
        """
        # Check working memory first
        for item in self.working_memory:
            if item["id"] == memory_id:
                return item
        
        # Check persistent storage
        try:
            memory_path = os.path.join(self.storage_dir, f"{memory_id}.json")
            if os.path.exists(memory_path):
                with open(memory_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error retrieving memory {memory_id}: {e}")
        
        return None
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant memories using the query.
        
        Args:
            query (str): The search query
            limit (int): Maximum number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of relevant memories
        """
        # This is a simplified mock implementation
        # In a real system, we would:
        # 1. Generate a vector embedding for the query
        # 2. Compare it to stored vectors using cosine similarity
        # 3. Return the most similar items
        
        # For now, just return the most recent items
        results = []
        for memory in reversed(self.working_memory):
            # Simple keyword matching
            if query.lower() in str(memory["content"]).lower():
                results.append(memory)
                if len(results) >= limit:
                    break
        
        # If we don't have enough results, check disk storage
        if len(results) < limit:
            try:
                for filename in os.listdir(self.storage_dir):
                    if not filename.endswith(".json"):
                        continue
                    
                    with open(os.path.join(self.storage_dir, filename), 'r') as f:
                        memory = json.load(f)
                        if query.lower() in str(memory["content"]).lower():
                            if memory not in results:
                                results.append(memory)
                                if len(results) >= limit:
                                    break
            except Exception as e:
                print(f"Error searching disk storage: {e}")
        
        return results
    
    def summarize(self) -> str:
        """
        Create a summary of the current working memory.
        
        Returns:
            str: A summary of the key information in memory
        """
        if not self.working_memory:
            return "No items in memory."
        
        # Count total items
        total_items = len(self.working_memory)
        
        # Get time range
        start_time = self.working_memory[0]["timestamp"]
        end_time = self.working_memory[-1]["timestamp"]
        
        # Create a simple summary
        summary = f"Memory contains {total_items} items from {start_time} to {end_time}."
        
        # In a real implementation, we might use an LLM to generate a more meaningful summary
        
        return summary
    
    def _save_to_disk(self, memory_item: Dict[str, Any]) -> None:
        """
        Save a memory item to persistent storage.
        
        Args:
            memory_item (Dict[str, Any]): The memory to save
        """
        try:
            memory_path = os.path.join(self.storage_dir, f"{memory_item['id']}.json")
            with open(memory_path, 'w') as f:
                json.dump(memory_item, f, indent=2)
        except Exception as e:
            print(f"Error saving memory to disk: {e}")
    
    def clear_working_memory(self) -> None:
        """Clear the current working memory."""
        self.working_memory = []
        
    def clear_all(self) -> None:
        """Clear all memory, including persistent storage (use with caution)."""
        self.working_memory = []
        
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.endswith(".json"):
                    os.remove(os.path.join(self.storage_dir, filename))
        except Exception as e:
            print(f"Error clearing persistent memory: {e}")
