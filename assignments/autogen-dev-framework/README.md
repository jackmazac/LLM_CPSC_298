# AutoGen Development Framework

A streamlined development framework using Microsoft's AutoGen library for automated software development. This framework integrates specialized AI agents for coding, testing, debugging, and performance monitoring.

## Features

- **AI-Powered Development**
  - Code generation with GPT-4
  - Automated testing and validation
  - Intelligent error debugging
  - Performance monitoring

- **Agent Architecture**
  - Assistant Agent: Main development and code generation
  - User Proxy Agent: Task management and code execution
  - Testing Agent: Test creation and validation
  - Debugging Agent: Error analysis and resolution

## Prerequisites

- Python 3.10+
- OpenAI API Key
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/memaxo/LLM_CPSC_298.git
cd LLM_CPSC_298/assignments/autogen-dev-framework
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your configuration:
```env
# OpenAI Configuration
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7

# System Configuration
DEBUG_MODE=True
LOG_LEVEL=INFO

# Agent Configuration
MAX_CONSECUTIVE_AUTO_REPLY=3
WORK_DIR=./coding

# Performance Settings
TIMEOUT=600
MAX_RETRIES=3
CACHE_SEED=42
```

## Usage

1. **Run the Development Framework**:
```bash
python -m src.test_framework
```

2. **Example Tasks**:
```python
# Create a Hello World program
Create a Python script that:
1. Prints "Hello, World!"
2. Includes a main function
3. Has proper documentation
4. Follows Python best practices
```

## Project Structure

```
autogen-dev-framework/
├── src/
│   ├── agents/
│   │   ├── debugger.py   # Error analysis and debugging
│   │   ├── tester.py     # Test generation and execution
│   │   └── __init__.py   # Agent exports
│   ├── chat.py           # Main chat implementation
│   ├── config.py         # Configuration management
│   ├── monitor.py        # Performance monitoring
│   └── test_framework.py # Test framework implementation
├── .env                  # Environment configuration
├── .gitignore           # Git ignore rules
└── requirements.txt      # Project dependencies
```

## Features in Detail

### Development Chat
- Interactive development environment
- AI-powered code generation
- Real-time code execution
- Error handling and recovery

### Testing Framework
- Automated test generation
- PyTest integration
- Test result reporting
- Edge case validation

### Debugging System
- Intelligent error analysis
- Stack trace interpretation
- Fix suggestions
- Bug pattern recognition

### Performance Monitoring
- Task execution timing
- Success rate tracking
- System resource monitoring
- Detailed metrics output

## Error Handling

The framework provides comprehensive error handling:
1. **Error Detection**: Captures runtime errors and test failures
2. **Analysis**: Uses DebuggingAgent to analyze error patterns
3. **Resolution**: Provides detailed debug analysis and fix suggestions
4. **Monitoring**: Tracks error patterns and resolution success rates

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Microsoft AutoGen Team
- OpenAI GPT-4
- Python Community