"""
Main Application for SAT Step-by-Step Agentic AI App

Two-tab interface:
1. SAT Problem Solver - Step-by-step solutions for individual SAT questions
2. Knowledge Base Q&A - Answer questions using SAT study materials
"""

import os
import streamlit as st
from dotenv import load_dotenv
from planner import Planner
from executor import Executor
from memory import Memory

# Load environment variables
load_dotenv()

class SATAgent:
    """
    Main SAT tutoring agent that coordinates planning, execution, and memory.
    """
    
    def __init__(self):
        """Initialize the SAT agent with all core modules."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Initialize core modules
        self.planner = Planner(api_key)
        self.executor = Executor(api_key)
        self.memory = Memory()
        
        # Initialize session state
        if 'problem_solver_history' not in st.session_state:
            st.session_state.problem_solver_history = []
        if 'knowledge_qa_history' not in st.session_state:
            st.session_state.knowledge_qa_history = []
    
    def solve_sat_problem(self, question: str, question_type: str = "auto") -> dict:
        """
        Solve a SAT problem through the complete agentic pipeline.
        
        Args:
            question (str): The SAT question to solve
            question_type (str): Type of question (math, english, or auto-detect)
            
        Returns:
            dict: Complete response with plan, execution results, and memory
        """
        try:
            # Store the question in memory
            question_memory = {
                "type": "sat_problem",
                "content": question,
                "question_type": question_type
            }
            memory_id = self.memory.store(question_memory)
            
            # Create a plan for solving the SAT problem
            plan = self.planner.create_plan(f"""
            Solve this SAT question step by step:
            
            Question: {question}
            Question Type: {question_type}
            
            Create a detailed plan that:
            1. Identifies what type of SAT question this is (math/english subtype)
            2. If helpful, searches knowledge base for relevant strategies using search_knowledge tool
            3. Breaks down the solution into clear, logical steps
            4. Explains the reasoning and strategy for each step
            5. Shows all work for math problems or analysis for english
            6. Provides the final answer with confidence explanation
            
            Available knowledge base tools if needed:
            - search_knowledge(query, subject="all", max_results=3): Semantic search using RAG
            - get_context(query, subject="all"): Get formatted context for concepts
            - calculator(expression): Perform calculations
            
            Make this educational - explain WHY each step is taken.
            """)
            
            # Execute the plan
            results = self.executor.execute_plan(plan)
            
            # Store results in memory
            results_memory = {
                "type": "sat_solution",
                "content": results,
                "related_question": memory_id
            }
            self.memory.store(results_memory)
            
            # Create response
            response = {
                "question": question,
                "question_type": question_type,
                "plan": plan,
                "results": results,
                "memory_id": memory_id,
                "status": "success"
            }
            
            # Add to problem solver history
            st.session_state.problem_solver_history.append(response)
            
            return response
            
        except Exception as e:
            error_response = {
                "question": question,
                "error": str(e),
                "status": "error"
            }
            st.session_state.problem_solver_history.append(error_response)
            return error_response
    
    def answer_problem_question(self, question: str, problem_context: str, answer_context: str) -> dict:
        """
        Answer a question about a specific problem and its explanation.
        
        Args:
            question (str): Question about the specific problem
            problem_context (str): The original problem statement
            answer_context (str): The provided answer/explanation
            
        Returns:
            dict: Response with contextualized answer
        """
        try:
            # Store the question in memory
            question_memory = {
                "type": "problem_question",
                "content": question,
                "problem_context": problem_context,
                "answer_context": answer_context
            }
            memory_id = self.memory.store(question_memory)
            
            # Create a plan for answering using the specific problem context
            plan = self.planner.create_plan(f"""
            Answer this question about a specific SAT problem and its solution:
            
            ORIGINAL PROBLEM: {problem_context}
            
            PROVIDED ANSWER/EXPLANATION: {answer_context}
            
            USER'S QUESTION: {question}
            
            Create a plan that:
            1. Analyzes the original problem and provided explanation
            2. Identifies what specific aspect the user is asking about
            3. Provides a clear, educational answer based on the context
            4. References specific parts of the problem or explanation as needed
            5. Offers additional insights or alternative approaches if relevant
            
            Make this helpful for understanding the specific problem and solution provided.
            """)
            
            # Execute the plan
            results = self.executor.execute_plan(plan)
            
            # Store results in memory
            results_memory = {
                "type": "problem_answer",
                "content": results,
                "related_question": memory_id
            }
            self.memory.store(results_memory)
            
            # Create response
            response = {
                "question": question,
                "problem_context": problem_context,
                "answer_context": answer_context,
                "plan": plan,
                "results": results,
                "memory_id": memory_id,
                "status": "success"
            }
            
            # Add to knowledge Q&A history
            st.session_state.knowledge_qa_history.append(response)
            
            return response
            
        except Exception as e:
            error_response = {
                "question": question,
                "error": str(e),
                "status": "error"
            }
            st.session_state.knowledge_qa_history.append(error_response)
            return error_response

    def answer_knowledge_question(self, question: str, topic_focus: str = "all") -> dict:
        """
        Answer a question about SAT concepts using the knowledge base.
        
        Args:
            question (str): Question about SAT concepts
            topic_focus (str): Focus area (math, english, or all)
            
        Returns:
            dict: Response with answer and source documents
        """
        try:
            # Store the question in memory
            question_memory = {
                "type": "knowledge_question",
                "content": question,
                "topic_focus": topic_focus
            }
            memory_id = self.memory.store(question_memory)
            
            # Create a plan for answering using knowledge base
            plan = self.planner.create_plan(f"""
            Answer this question about SAT concepts using available study materials:
            
            Question: {question}
            Topic Focus: {topic_focus}
            
            Create a plan that:
            1. Identifies which SAT topics/concepts are relevant to this question
            2. Searches the knowledge base for relevant study materials using search_knowledge tool
            3. Retrieves specific topic content if needed using get_topic_content tool
            4. Synthesizes information from multiple sources
            5. Provides a comprehensive, educational answer with citations
            
            Available knowledge base tools:
            - search_knowledge(query, subject="all", max_results=3): Semantic search using RAG
            - get_context(query, subject="all", max_context_length=1500): Get formatted context
            
            Make this helpful for SAT preparation - include examples and tips where relevant.
            """)
            
            # Execute the plan
            results = self.executor.execute_plan(plan)
            
            # Store results in memory
            results_memory = {
                "type": "knowledge_answer",
                "content": results,
                "related_question": memory_id
            }
            self.memory.store(results_memory)
            
            # Create response
            response = {
                "question": question,
                "topic_focus": topic_focus,
                "plan": plan,
                "results": results,
                "memory_id": memory_id,
                "status": "success"
            }
            
            # Add to knowledge Q&A history
            st.session_state.knowledge_qa_history.append(response)
            
            return response
            
        except Exception as e:
            error_response = {
                "question": question,
                "error": str(e),
                "status": "error"
            }
            st.session_state.knowledge_qa_history.append(error_response)
            return error_response

def render_sat_problem_solver_tab(agent):
    """Render the SAT Problem Solver tab."""
    st.header("🧮 SAT Problem Solver")
    st.markdown("*Enter a specific SAT question and get a detailed, step-by-step solution*")
    
    # Question type selection
    col1, col2 = st.columns([3, 1])
    with col2:
        question_type = st.selectbox(
            "Question Type",
            ["auto", "math", "english"],
            help="Select the type of SAT question for better processing"
        )
    
    # Question input
    with col1:
        question = st.text_area(
            "Enter your SAT question:",
            placeholder="Example: If 3x + 7 = 22, what is the value of x?",
            height=120,
            help="Paste the complete SAT question you need help solving"
        )
    
    # Solve button
    if st.button("🎯 Solve Problem", type="primary", disabled=not question.strip()):
        if question.strip():
            with st.spinner("Analyzing and solving your SAT problem..."):
                response = agent.solve_sat_problem(question.strip(), question_type)
            
            # Display results
            if response["status"] == "success":
                st.success("✅ Problem solved successfully!")
                
                # Show the solution plan
                st.subheader("📋 Solution Strategy")
                for i, step in enumerate(response["plan"], 1):
                    with st.expander(f"Planning Step {i}", expanded=True):
                        st.write(step.get('description', 'No description available'))
                        if step.get('tools'):
                            st.info(f"**Tools needed:** {', '.join(step['tools'])}")
                
                # Show detailed solution
                st.subheader("🎯 Step-by-Step Solution")
                for i, result in enumerate(response["results"], 1):
                    with st.expander(f"Solution Step {i}", expanded=True):
                        if result.get("status") == "success":
                            st.write(result.get("result", "No result available"))
                            if result.get("tool_used"):
                                st.info(f"**Tool used:** {result['tool_used']}")
                        else:
                            st.error(f"Error in step {i}: {result.get('message', 'Unknown error')}")
            
            else:
                st.error(f"❌ Error solving problem: {response.get('error', 'Unknown error')}")
    
    # Show recent problems
    if st.session_state.problem_solver_history:
        st.subheader("📚 Recent Problems")
        for i, entry in enumerate(reversed(st.session_state.problem_solver_history[-3:]), 1):
            with st.expander(f"Problem {i}: {entry['question'][:50]}..."):
                st.write(f"**Question:** {entry['question']}")
                st.write(f"**Type:** {entry.get('question_type', 'Unknown')}")
                if entry.get("status") == "success":
                    st.write("**Status:** ✅ Solved")
                else:
                    st.write("**Status:** ❌ Error")

def render_knowledge_qa_tab(agent):
    """Render the Knowledge Base Q&A tab."""
    st.header("📚 SAT Knowledge Q&A")
    st.markdown("*Ask questions about SAT concepts or get help with specific problems*")
    
    # Create sub-tabs for different Q&A modes
    qa_tab1, qa_tab2 = st.tabs(["💡 General SAT Concepts", "📝 Specific Problem Q&A"])
    
    with qa_tab1:
        st.subheader("Ask About SAT Concepts")
        st.markdown("*Get answers from our comprehensive study materials*")
        
        # Topic focus selection
        col1, col2 = st.columns([3, 1])
        with col2:
            topic_focus = st.selectbox(
                "Focus Area",
                ["all", "math", "english"],
                help="Focus the search on specific SAT subject areas"
            )
        
        # Question input
        with col1:
            concept_question = st.text_area(
                "Ask about SAT concepts:",
                placeholder="Example: What are the key strategies for solving linear equations on the SAT?",
                height=120,
                help="Ask about SAT concepts, strategies, formulas, or study tips",
                key="concept_question"
            )
        
        # Answer button
        if st.button("🔍 Find Answer", type="primary", disabled=not concept_question.strip(), key="concept_answer_btn"):
            if concept_question.strip():
                with st.spinner("Searching knowledge base and generating answer..."):
                    response = agent.answer_knowledge_question(concept_question.strip(), topic_focus)
                
                # Display results
                if response["status"] == "success":
                    st.success("✅ Answer found!")
                    
                    # Show the research plan
                    st.subheader("🔍 Research Strategy")
                    for i, step in enumerate(response["plan"], 1):
                        with st.expander(f"Research Step {i}"):
                            st.write(step.get('description', 'No description available'))
                            if step.get('tools'):
                                st.info(f"**Tools used:** {', '.join(step['tools'])}")
                    
                    # Show the answer
                    st.subheader("💡 Knowledge Base Answer")
                    for i, result in enumerate(response["results"], 1):
                        with st.expander(f"Answer Part {i}", expanded=True):
                            if result.get("status") == "success":
                                st.write(result.get("result", "No result available"))
                                if result.get("tool_used"):
                                    st.info(f"**Source:** {result['tool_used']}")
                            else:
                                st.error(f"Error in part {i}: {result.get('message', 'Unknown error')}")
                
                else:
                    st.error(f"❌ Error finding answer: {response.get('error', 'Unknown error')}")
    
    with qa_tab2:
        st.subheader("Ask About a Specific Problem")
        st.markdown("*Provide a problem and its solution, then ask specific questions about it*")
        
        # Problem context input
        problem_context = st.text_area(
            "Enter the original problem:",
            placeholder="Example: If 3x + 7 = 22, what is the value of x?",
            height=100,
            help="Paste the original SAT problem you want to ask about",
            key="problem_context"
        )
        
        # Answer context input  
        answer_context = st.text_area(
            "Enter the answer/explanation:",
            placeholder="Example: To solve for x, subtract 7 from both sides: 3x = 15. Then divide by 3: x = 5.",
            height=120,
            help="Provide the solution or explanation for the problem",
            key="answer_context"
        )
        
        # Question about the problem
        problem_question = st.text_area(
            "What do you want to know about this problem?",
            placeholder="Example: Why do we subtract 7 first instead of dividing by 3?",
            height=80,
            help="Ask specific questions about the problem or its solution",
            key="problem_question"
        )
        
        # Answer button
        if st.button(
            "🎯 Get Explanation", 
            type="primary", 
            disabled=not (problem_context.strip() and answer_context.strip() and problem_question.strip()),
            key="problem_answer_btn"
        ):
            if problem_context.strip() and answer_context.strip() and problem_question.strip():
                with st.spinner("Analyzing the problem and generating explanation..."):
                    response = agent.answer_problem_question(
                        problem_question.strip(), 
                        problem_context.strip(), 
                        answer_context.strip()
                    )
                
                # Display results
                if response["status"] == "success":
                    st.success("✅ Explanation generated!")
                    
                    # Show the context being analyzed
                    with st.expander("📋 Problem Context", expanded=False):
                        st.write("**Original Problem:**")
                        st.write(problem_context)
                        st.write("**Provided Solution:**")
                        st.write(answer_context)
                        st.write("**Your Question:**")
                        st.write(problem_question)
                    
                    # Show the analysis plan
                    st.subheader("🧠 Analysis Strategy")
                    for i, step in enumerate(response["plan"], 1):
                        with st.expander(f"Analysis Step {i}"):
                            st.write(step.get('description', 'No description available'))
                            if step.get('tools'):
                                st.info(f"**Tools used:** {', '.join(step['tools'])}")
                    
                    # Show the explanation
                    st.subheader("💡 Detailed Explanation")
                    for i, result in enumerate(response["results"], 1):
                        with st.expander(f"Explanation Part {i}", expanded=True):
                            if result.get("status") == "success":
                                st.write(result.get("result", "No result available"))
                                if result.get("tool_used"):
                                    st.info(f"**Analysis method:** {result['tool_used']}")
                            else:
                                st.error(f"Error in part {i}: {result.get('message', 'Unknown error')}")
                
                else:
                    st.error(f"❌ Error generating explanation: {response.get('error', 'Unknown error')}")
    
    # Show recent questions (for both types)
    if st.session_state.knowledge_qa_history:
        st.subheader("🗂️ Recent Questions")
        for i, entry in enumerate(reversed(st.session_state.knowledge_qa_history[-5:]), 1):
            with st.expander(f"Q{i}: {entry['question'][:50]}..."):
                st.write(f"**Question:** {entry['question']}")
                
                # Show different info based on question type
                if entry.get('topic_focus'):
                    st.write(f"**Type:** General SAT Concepts")
                    st.write(f"**Focus:** {entry.get('topic_focus', 'All topics')}")
                elif entry.get('problem_context'):
                    st.write(f"**Type:** Specific Problem Q&A")
                    st.write(f"**Problem:** {entry.get('problem_context', '')[:100]}...")
                
                if entry.get("status") == "success":
                    st.write("**Status:** ✅ Answered")
                else:
                    st.write("**Status:** ❌ Error")

def main():
    """Main Streamlit application with 2-tab interface."""
    st.set_page_config(
        page_title="SAT Step-by-Step AI Tutor",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 SAT Step-by-Step AI Tutor")
    st.markdown("*An agentic AI that helps you master SAT questions and concepts*")
    
    # Initialize the agent
    try:
        if 'agent' not in st.session_state:
            st.session_state.agent = SATAgent()
        agent = st.session_state.agent
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.info("Please make sure you have a `.env` file with your `GEMINI_API_KEY`")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("Agent Status")
        memory_summary = agent.memory.summarize()
        st.text(memory_summary)
        
        if st.button("Clear All Memory"):
            agent.memory.clear_working_memory()
            st.session_state.problem_solver_history = []
            st.session_state.knowledge_qa_history = []
            st.success("All memory cleared!")
        
        st.markdown("---")
        st.markdown("**How to use:**")
        st.markdown("• **Problem Solver**: Get step-by-step solutions")
        st.markdown("• **Knowledge Q&A**: Learn SAT concepts and strategies")
    
    # Create two tabs
    tab1, tab2 = st.tabs(["🧮 Problem Solver", "📚 Knowledge Q&A"])
    
    with tab1:
        render_sat_problem_solver_tab(agent)
    
    with tab2:
        render_knowledge_qa_tab(agent)

if __name__ == "__main__":
    main()