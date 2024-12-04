from src.chat import DevelopmentChat
from src.config import Config
import logging
import os

logging.basicConfig(**Config.get_logging_config())
logger = logging.getLogger(__name__)

def test_hello_world():
    """Test creating a simple Hello World program"""
    chat = DevelopmentChat(max_rounds=10)
    
    task = """
    Create a Python script that:
    1. Prints "Hello, World!"
    2. Includes a main function
    3. Has proper documentation
    4. Follows Python best practices
    
    Save this as 'hello_world.py' in the coding directory.
    """
    
    try:
        # Ensure coding directory exists
        os.makedirs("coding", exist_ok=True)
        
        print("\n=== Creating Hello World Program ===")
        result = chat._plan_and_execute(task)
        
        print("\n=== Results ===")
        print(f"Status: {result['status']}")
        if result.get('results'):
            print("\nResults:")
            print(result['results'])
        
        # Check if file was created
        if os.path.exists("coding/hello_world.py"):
            print("\nFile created successfully!")
            with open("coding/hello_world.py", "r") as f:
                print("\nFile contents:")
                print(f.read())
        
        return result['status'] == 'completed'
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        return False

def test_framework():
    """Run all framework tests"""
    print("\n=== Testing AutoGen Framework with GPT-4 ===")
    print(f"Model: {Config.OPENAI_MODEL}")
    print(f"Temperature: {Config.OPENAI_TEMPERATURE}")
    print("==========================================\n")
    
    # Run hello world test
    success = test_hello_world()
    
    print("\n=== Test Summary ===")
    print(f"Framework Test: {'✅ Passed' if success else '❌ Failed'}")
    print("===================\n")
    
    return success

if __name__ == "__main__":
    test_framework() 