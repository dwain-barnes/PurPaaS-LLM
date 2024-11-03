# PurPaaS (Purple Teaming as a Service)
## Autonomous Local LLM Security Testing Framework

PurPaaS is an innovative open-source security testing platform that implements purple teaming (combined red and blue team approaches) to evaluate local LLM models through Ollama. By orchestrating autonomous agents, PurPaaS provides comprehensive security assessment of locally deployed AI models.

### What is Purple Teaming?
Purple teaming combines:
- 🔴 Red Team (Offensive) - Autonomous prompt injection and security testing
- 🔵 Blue Team (Defensive) - Real-time analysis and vulnerability assessment
- 🟣 Purple Team Integration - Synchronized offensive and defensive testing for comprehensive security evaluation

### Key Features:

- **Local-First Architecture**: 
  - Fully local testing environment
  - No cloud dependencies
  - Complete privacy and control
  - Works with any Ollama-compatible model

- **Autonomous Purple Team Testing**: 
  - Coordinated red and blue team operations
  - Autonomous prompt injection attacks
  - Real-time defensive analysis
  - Comprehensive security assessment

- **Real-time Agent Chat Interface**: 
  - Monitor live red team injection attempts
  - Track blue team defensive responses
  - Observe purple team coordination in action

- **Comprehensive Security Analysis**: 
  - Systematic vulnerability assessment
  - Defense effectiveness evaluation
  - Detailed remediation recommendations

- **Advanced Reporting**: 
  - Security assessment reports
  - Attack success rate analytics
  - Defensive coverage metrics

- **Streamlit-based Interface**: 
  - Intuitive testing configuration
  - Real-time test monitoring
  - Interactive results visualization

### Requirements:
- Python 3.8+
- Ollama
- Required Python packages (see requirements.txt)

### Quick Start:
```bash
git clone https://github.com/dwain-barnes/PurPaaS-LLM/
cd purpaas
pip install -r requirements.txt
streamlit run main.py
```

### Technical Architecture 🏗️

combines three powerful technologies:
- **OpenAI Swarm**: Handles agent communication and conversation flow
- **Ollama**: Provides local inference capabilities for various open-source language models
- **Streamlit**: Creates the beautiful UI and handles real-time updates

## Troubleshooting 🔍

Common issues and solutions:

1. **Model Loading Errors**:
   - Ensure Ollama is running (`ollama serve`)
   - Check available models (`ollama list`)
   - Verify model is downloaded (`ollama pull model_name`)

2. **Conversation Stalls**:
   - Check Ollama service status
   - Monitor system resources
   - Try restarting the application

3. **Model Switching Issues**:
   - Clear chat history before switching models
   - Ensure both models are fully downloaded
   - Check model compatibility

## License 📄

MIT License - feel free to use this project however you'd like!

## Acknowledgments 🙏

- Built with [OpenAI Swarm](https://github.com/openai/swarm)
- Powered by [Ollama](https://ollama.ai/)
- Created with [Streamlit](https://streamlit.io/)
