import asyncio
from autogen import AssistantAgent, UserProxyAgent
import logging
import os
import re
from pathlib import Path
from typing import Dict, Any
from src.config import Config
from src.monitor import PerformanceMonitor, measure_time
from src.agents.tester import TestingAgent

logging.basicConfig(**Config.get_logging_config())
logger = logging.getLogger(__name__)

class DevelopmentChat:
    def __init__(self, max_rounds: int = 10):
        self.monitor = PerformanceMonitor()
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize basic agent setup"""
        # User proxy for task management and code execution
        self.user_proxy = UserProxyAgent(
            name="user_proxy",
            system_message="You are a user proxy that helps with development tasks. Use TERMINATE when task is complete.",
            code_execution_config={
                "work_dir": "coding",
                "use_docker": False,
            },
            human_input_mode="NEVER"
        )
        
        # Main assistant for development
        self.assistant = AssistantAgent(
            name="assistant",
            system_message="""You are a helpful AI coding assistant. You can:
            1. Write and modify code
            2. Debug issues
            3. Test solutions
            4. Explain your work
            
            Always ensure code is complete and follows best practices.
            When a task is completed successfully, include 'TERMINATE' in your response.""",
            llm_config=Config.get_openai_config()
        )
        
        # Testing agent for code validation
        self.tester = TestingAgent(
            llm_config=Config.get_openai_config()
        )
    
    def _extract_code_from_message(self, message: str) -> str:
        """Extract code from message and clean it"""
        # Find code between triple backticks
        code_match = re.search(r'```python\n(.*?)\n```', message, re.DOTALL)
        if not code_match:
            return ""
        
        # Clean and normalize the code
        code = code_match.group(1)
        code = code.replace('\\n', '\n')  # Replace escaped newlines
        code = code.strip()
        
        return code
    
    def _run_tests(self, code: str, filename: str) -> Dict[str, Any]:
        """Run tests for the generated code"""
        try:
            # Create test file
            test_result = self.tester.create_test_file(code, filename)
            if not test_result['success']:
                return test_result
            
            # Run tests
            return self.tester.run_tests(test_result['test_file'])
            
        except Exception as e:
            logger.error(f"Error running tests: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }
    
    @measure_time
    def _plan_and_execute(self, task: str) -> dict:
        """Execute development task"""
        try:
            # Record task start
            self.monitor.record_metric('last_task', task)
            
            # Initiate chat between user proxy and assistant
            result = self.user_proxy.initiate_chat(
                self.assistant,
                message=task,
                max_turns=3
            )
            
            # Get the last message from chat history
            last_message = None
            if hasattr(result, 'chat_history') and result.chat_history:
                last_message = result.chat_history[-1].get('content', '')
            
            # Check if task completed successfully
            success = last_message and "TERMINATE" in last_message
            
            # Run tests if code was generated
            test_results = None
            if success and os.path.exists("coding"):
                # Find the most recently modified Python file
                files = list(Path("coding").glob("*.py"))
                if files:
                    latest_file = max(files, key=lambda p: p.stat().st_mtime)
                    # Extract and clean code from the message
                    code = self._extract_code_from_message(last_message)
                    if code:
                        # Write clean code to file
                        with open(latest_file, 'w') as f:
                            f.write(code)
                        test_results = self._run_tests(code, latest_file.name)
            
            # Record task result
            self.monitor.record_task_result(success)
            
            return {
                'status': 'completed' if success else 'ongoing',
                'results': last_message,
                'test_results': test_results,
                'metrics': self.monitor.get_metrics()
            }
            
        except Exception as e:
            logger.error(f"Task execution error: {str(e)}", exc_info=True)
            # Record task failure
            self.monitor.record_task_result(False)
            return {
                'status': 'failed',
                'error': str(e),
                'metrics': self.monitor.get_metrics()
            }

    def chat_loop(self):
        """Simple chat loop for development tasks"""
        try:
            while True:
                user_input = input("\nEnter your task (or 'exit' to quit): ")
                if user_input.lower() == 'exit':
                    break
                
                result = self._plan_and_execute(user_input)
                
                if result['status'] == 'completed':
                    print("\n✅ Task completed successfully!")
                    if result.get('results'):
                        print(f"\nResults:\n{result['results']}")
                    
                    # Display test results if available
                    if result.get('test_results'):
                        print("\n=== Test Results ===")
                        test_results = result['test_results']
                        if test_results['success']:
                            print("✅ All tests passed")
                        else:
                            print("❌ Some tests failed")
                            if 'error' in test_results:
                                print(f"Error: {test_results['error']}")
                        print("===================")
                        
                elif result['status'] == 'failed':
                    print(f"\n❌ Task failed: {result.get('error')}")
                else:
                    print("\n⏳ Task is ongoing...")
                
                # Display metrics in debug mode
                if Config.DEBUG_MODE and result.get('metrics'):
                    print("\n=== Performance Metrics ===")
                    metrics = result['metrics']
                    print(f"Task Duration: {metrics.get('_plan_and_execute_duration', 0):.2f}s")
                    print(f"Success Rate: {metrics.get('success_rate', 0):.1f}%")
                    print(f"Total Tasks: {metrics.get('total_tasks', 0)}")
                    
                    system = metrics.get('system', {})
                    print(f"CPU Usage: {system.get('cpu_percent', 0):.1f}%")
                    print(f"Memory Usage: {system.get('memory_mb', 0):.1f}MB")
                    print("=========================")
        
        except KeyboardInterrupt:
            print("\n\nChat session terminated by user.")
            if Config.DEBUG_MODE:
                print("\n=== Final Metrics ===")
                print(self.monitor.get_metrics())
        except Exception as e:
            logger.error("Chat loop error", exc_info=True)
            print(f"\nError in chat loop: {str(e)}")

def main():
    """Entry point for the chat application"""
    chat = DevelopmentChat()
    chat.chat_loop()

if __name__ == "__main__":
    main()