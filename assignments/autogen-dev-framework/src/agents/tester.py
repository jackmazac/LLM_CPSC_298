from autogen import AssistantAgent
from typing import Dict, Any, Optional
import logging
from pathlib import Path
import pytest
import sys
from src.config import Config
from src.monitor import measure_time

logger = logging.getLogger(__name__)

class TestingAgent(AssistantAgent):
    """Agent specialized in writing and executing test cases"""
    
    def __init__(
        self,
        name: str = "tester",
        llm_config: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        system_message = """You are a testing specialist responsible for:
        1. Writing unit tests for Python code
        2. Validating functionality
        3. Testing edge cases
        4. Ensuring code quality
        
        Always include test documentation and clear assertions.
        Use TERMINATE when testing is complete."""
        
        super().__init__(
            name=name,
            system_message=system_message,
            llm_config=llm_config or Config.get_openai_config(),
            **kwargs
        )
        
        self.work_dir = Path(Config.WORK_DIR)
        self.work_dir.mkdir(parents=True, exist_ok=True)
    
    @measure_time
    def create_test_file(self, code: str, filename: str) -> Dict[str, Any]:
        """Create a test file for the given code"""
        try:
            # Generate test filename
            test_file = self.work_dir / f"test_{Path(filename).stem}.py"
            
            # Create test content
            test_content = f'''"""Tests for {filename}"""
import pytest
from {Path(filename).stem} import main

def test_functionality(capsys):
    """Test basic functionality"""
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, World!"

def test_edge_cases():
    """Test edge cases"""
    # Add edge case tests here
    pass

def test_error_handling():
    """Test error handling"""
    # Add error handling tests here
    pass
'''
            # Write test file
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            return {
                'success': True,
                'test_file': str(test_file)
            }
            
        except Exception as e:
            logger.error(f"Error creating test file: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }
    
    @measure_time
    def run_tests(self, test_file: str) -> Dict[str, Any]:
        """Run tests using pytest"""
        try:
            # Add work directory to Python path
            sys.path.insert(0, str(self.work_dir))
            
            # Run pytest
            result = pytest.main(['-v', test_file])
            
            return {
                'success': result == pytest.ExitCode.OK,
                'exit_code': result,
                'test_file': test_file
            }
            
        except Exception as e:
            logger.error(f"Error running tests: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            # Remove work directory from path
            sys.path.pop(0)
