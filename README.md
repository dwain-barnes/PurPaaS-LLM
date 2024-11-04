# PurPaaS (Purple Teaming as a Service)
## Autonomous Local LLM Security Testing Framework

PurPaaS is an innovative open-source security testing platform that implements purple teaming (combined red and blue team approaches) to evaluate local LLM models through Ollama. By orchestrating autonomous agents, PurPaaS provides comprehensive security assessment of locally deployed AI models.

![main](main.png)

### What is Purple Teaming?
Purple teaming combines:
- 🔴 Red Team (Offensive) - Autonomous prompt injection and security testing
- 🔵 Blue Team (Defensive) - Real-time analysis and vulnerability assessment
- 🟣 Purple Team Integration - Synchronized offensive and defensive testing for comprehensive security evaluation

![Agent Selection Tab](agents.png)

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


![Target LLM](target.png)


### Requirements:
- Python 3.10+
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



# ⚠️ Important Notice

## Disclaimer and Intended Use
PurPaaS LLM is designed as a security testing tool for local language models. By using this software, you agree to the following conditions:

### 🎯 Intended Purpose
- This tool is exclusively for security testing and validation of LOCAL Language Models through Ollama
- Meant for legitimate security research and model improvement
- Should be used in controlled, authorized testing environments

### ⚠️ Disclaimers
- The creator(s) take NO responsibility for any misuse of this tool
- Any malicious use of this software is strictly prohibited
- Users are solely responsible for how they use and implement this tool
- This tool should NOT be used against commercial or cloud-based LLMs

### 🚧 Alpha Preview Status
- This is an ALPHA preview release
- Features may be unstable or function incorrectly
- Performance and results may vary
- Breaking changes may occur without notice

### 🤖 Model Compatibility
- Different LLMs may perform better in red team or blue team roles
- Performance varies between models
- Testing and experimentation needed to find optimal configurations
- Limited to Ollama-compatible models only

### 📝 Prompts
- No default prompts are provided with this tool
- Users must supply their own testing prompts via CSV
- Sample prompts can be found in various GitHub repositories
- We take no responsibility for any prompts used with this tool

### 💼 Commercial Use
- This tool is NOT designed for testing commercial LLMs
- Do NOT use against any cloud-based or API-based models
- Intended for testing self-hosted, local models only

By using PurPaaS LLM, you acknowledge and agree to these terms and conditions.


# 🚀 Roadmap & Coming Soon

## Upcoming Features

### 📊 Report Writer Agent
- Autonomous report generation based on test results
- Comprehensive security analysis documentation
- Vulnerability classification and prioritization
- Actionable recommendations for model improvements
- Exportable reports in multiple formats (PDF, HTML, MD)
- Custom report templates

### 🔄 Enhanced Query Customization
- Customizable initial prompts for agents
- Template library for different testing scenarios
- Agent role customization
- Adjustable testing parameters
- Custom test case creation interface

### 🌟 Also Planned
- Extended model compatibility testing
- Performance benchmarking tools
- Advanced visualization of test results 
- Custom agent behavior profiles
- Batch testing capabilities
- Test scenario templates

## Current Status: Alpha Preview
The current version focuses on core functionality. These upcoming features will enhance the testing and reporting capabilities of PurPaaS LLM.

## Community Input
We welcome suggestions and feedback on these planned features. Please use the Issues section to:
- Share feature ideas
- Report bugs
- Discuss improvements
- Contribute to development


## License 📄

MIT License - feel free to use this project however you'd like!

## Acknowledgments 🙏

- Built with [OpenAI Swarm](https://github.com/openai/swarm)
- Powered by [Ollama](https://ollama.ai/)
- Created with [Streamlit](https://streamlit.io/)
