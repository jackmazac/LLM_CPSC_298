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
from src.agents.debugger import DebuggingAgent
from src.agents.reviewer import ReviewAgent

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
        
        # Debugging agent for error analysis
        self.debugger = DebuggingAgent(
            llm_config=Config.get_openai_config()
        )
        
        # Review agent for code quality
        self.reviewer = ReviewAgent(
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
    
    def _handle_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle errors using the debugging agent"""
        try:
            # Get error details
            error_message = str(error)
            stack_trace = None
            if hasattr(error, '__traceback__'):
                import traceback
                stack_trace = ''.join(traceback.format_tb(error.__traceback__))
            
            # Get analysis from debugger
            debug_result = self.debugger.analyze_error(
                error_message=error_message,
                stack_trace=stack_trace,
                context=context
            )
            
            if debug_result.get('success'):
                return {
                    'status': 'debug',
                    'analysis': debug_result['analysis'],
                    'error': error_message,
                    'stack_trace': stack_trace
                }
            else:
                return {
                    'status': 'failed',
                    'error': error_message
                }
                
        except Exception as e:
            logger.error(f"Error in debugging: {str(e)}", exc_info=True)
            return {
                'status': 'failed',
                'error': str(e)
            }
    
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
    
    def _review_code(self, code: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Review code quality"""
        try:
            return self.reviewer.review_code(code, context)
        except Exception as e:
            logger.error(f"Error in code review: {str(e)}", exc_info=True)
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
            
            # Process code if generated
            test_results = None
            review_results = None
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
                        
                        # Run tests
                        test_results = self._run_tests(code, latest_file.name)
                        
                        # Review code
                        review_results = self._review_code(code, {
                            'task': task,
                            'filename': latest_file.name
                        })
                        
                        # If tests fail, get debug analysis
                        if not test_results.get('success'):
                            debug_results = self._handle_error(
                                Exception(test_results.get('error', 'Test failure')),
                                {'code': code, 'test_results': test_results}
                            )
                            test_results['debug_analysis'] = debug_results.get('analysis')
            
            # Record task result
            self.monitor.record_task_result(success)
            
            return {
                'status': 'completed' if success else 'ongoing',
                'results': last_message,
                'test_results': test_results,
                'review_results': review_results,
                'metrics': self.monitor.get_metrics()
            }
            
        except Exception as e:
            logger.error(f"Task execution error: {str(e)}", exc_info=True)
            # Get debug analysis
            debug_results = self._handle_error(e, {'task': task})
            # Record task failure
            self.monitor.record_task_result(False)
            return {
                'status': 'failed',
                'error': str(e),
                'debug_analysis': debug_results.get('analysis'),
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
                            if 'debug_analysis' in test_results:
                                print("\n=== Debug Analysis ===")
                                print(test_results['debug_analysis'])
                        print("===================")
                    
                    # Display review results if available
                    if result.get('review_results'):
                        print("\n=== Code Review ===")
                        review = result['review_results']
                        if review['success']:
                            print("\nMetrics:")
                            for key, value in review.get('metrics', {}).items():
                                print(f"- {key}: {value}")
                            print("\nSuggestions:")
                            for suggestion in review.get('suggestions', []):
                                print(f"- {suggestion}")
                        else:
                            print("❌ Review failed")
                            print(f"Error: {review.get('error')}")
                        print("===================")
                        
                elif result['status'] == 'failed':
                    print(f"\n❌ Task failed: {result.get('error')}")
                    if result.get('debug_analysis'):
                        print("\n=== Debug Analysis ===")
                        print(result['debug_analysis'])
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