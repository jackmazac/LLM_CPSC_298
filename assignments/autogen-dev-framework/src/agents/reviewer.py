from autogen import AssistantAgent
from typing import Dict, Any, Optional, List
import logging
from pathlib import Path
import ast
from src.config import Config
from src.monitor import measure_time

logger = logging.getLogger(__name__)

class ReviewAgent(AssistantAgent):
    """Agent specialized in code review and quality assurance"""
    
    def __init__(
        self,
        name: str = "reviewer",
        llm_config: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        system_message = """You are a code review specialist responsible for:
        1. Code quality assessment
        2. Best practices validation
        3. Security review
        4. Performance optimization
        5. Documentation review
        
        Provide detailed feedback and suggestions for improvement.
        Use TERMINATE when review is complete."""
        
        super().__init__(
            name=name,
            system_message=system_message,
            llm_config=llm_config or Config.get_openai_config(),
            **kwargs
        )
    
    @measure_time
    def analyze_code_quality(self, code: str) -> Dict[str, Any]:
        """Analyze code quality and structure"""
        try:
            # Parse code into AST
            tree = ast.parse(code)
            
            # Basic metrics
            metrics = {
                'num_functions': len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
                'num_classes': len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]),
                'has_docstrings': bool(ast.get_docstring(tree)),
                'imports': [n.names[0].name for n in ast.walk(tree) if isinstance(n, ast.Import)]
            }
            
            return {
                'success': True,
                'metrics': metrics
            }
            
        except Exception as e:
            logger.error(f"Error in code quality analysis: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }
    
    @measure_time
    def review_code(
        self,
        code: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform comprehensive code review"""
        try:
            # Get code quality metrics
            quality_result = self.analyze_code_quality(code)
            
            # Create review prompt
            review_prompt = f"""
            Review the following code:
            
            ```python
            {code}
            ```
            
            Context:
            {context}
            
            Code Metrics:
            {quality_result.get('metrics', {})}
            
            Provide review focusing on:
            1. Code Quality
               - Clean code principles
               - Function/class design
               - Variable naming
            
            2. Best Practices
               - Python conventions
               - Error handling
               - Type hints
            
            3. Security
               - Input validation
               - Data sanitization
               - Security best practices
            
            4. Performance
               - Algorithm efficiency
               - Resource usage
               - Optimization opportunities
            
            5. Documentation
               - Docstrings
               - Comments
               - API documentation
            """
            
            # Get review from LLM
            response = self.generate_reply([{
                "role": "user",
                "content": review_prompt
            }])
            
            return {
                'success': True,
                'review': response,
                'metrics': quality_result.get('metrics', {}),
                'suggestions': self._extract_suggestions(response)
            }
            
        except Exception as e:
            logger.error(f"Error in code review: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_suggestions(self, review: str) -> List[str]:
        """Extract actionable suggestions from review"""
        suggestions = []
        
        # Look for common suggestion patterns
        lines = review.split('\n')
        for line in lines:
            line = line.strip()
            if any(pattern in line.lower() for pattern in [
                'suggest', 'consider', 'recommend', 'could', 'should', 'might'
            ]):
                suggestions.append(line)
        
        return suggestions 