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
git clone [repository-url]
cd purpaas
pip install -r requirements.txt
streamlit run main.py
