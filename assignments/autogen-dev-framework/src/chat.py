import asyncio
from autogen import AssistantAgent, UserProxyAgent
import logging
from src.config import Config

logging.basicConfig(**Config.get_logging_config())
logger = logging.getLogger(__name__)

class DevelopmentChat:
    def __init__(self, max_rounds: int = 10):
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
    
    def _plan_and_execute(self, task: str) -> dict:
        """Execute development task"""
        try:
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
            
            return {
                'status': 'completed' if success else 'ongoing',
                'results': last_message
            }
            
        except Exception as e:
            logger.error(f"Task execution error: {str(e)}", exc_info=True)
            return {
                'status': 'failed',
                'error': str(e)
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
                elif result['status'] == 'failed':
                    print(f"\n❌ Task failed: {result.get('error')}")
                else:
                    print("\n⏳ Task is ongoing...")
        
        except KeyboardInterrupt:
            print("\n\nChat session terminated by user.")
        except Exception as e:
            logger.error("Chat loop error", exc_info=True)
            print(f"\nError in chat loop: {str(e)}")

def main():
    """Entry point for the chat application"""
    chat = DevelopmentChat()
    chat.chat_loop()

if __name__ == "__main__":
    main()