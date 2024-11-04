import streamlit as st
# Must be the first Streamlit command
st.set_page_config(page_title="LLM Security Testing", layout="wide")

import os
import logging
import sys
import asyncio
import time
import json
from datetime import datetime
import nest_asyncio
import pandas as pd
import requests
from swarm import Swarm, Agent

from security_tester import SecurityTestingSystem
from test_generator import SecurityTestGenerator
from agent_prompts import AGENT_PROMPTS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

nest_asyncio.apply()

# Configure Ollama
os.environ["OPENAI_API_KEY"] = "fake-key"
os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
os.environ["OPENAI_MODEL_NAME"] = "mistral:latest"

# Initialize Swarm client
client = Swarm()

# Function to get local Ollama models
def get_ollama_models():
    try:
        logger.info("🔍 Fetching available Ollama models...")
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            logger.info(f"✅ Found models: {model_names}")
            return model_names
        logger.warning("⚠️ Failed to fetch models, using defaults")
        return ["mistral", "llama2", "codellama"]
    except Exception as e:
        logger.error(f"❌ Error fetching models: {str(e)}")
        return ["mistral", "llama2", "codellama"]

# Function to pull model from Ollama
def pull_ollama_model(model_name):
    """Pull a model from Ollama"""
    try:
        logger.info(f"🚀 Starting download of model: {model_name}")
        response = requests.post(
            'http://localhost:11434/api/pull',
            json={'name': model_name},
            stream=True
        )
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if 'status' in data:
                    logger.info(f"📥 {model_name}: {data.get('status')} - {data.get('completed', '')} {data.get('total', '')}")
                    status_text.text(f"Status: {data.get('status')}")
                    
                    if 'completed' in data and 'total' in data:
                        try:
                            progress = int(data['completed']) / int(data['total'])
                            progress_bar.progress(progress)
                        except:
                            pass
                            
                if data.get('status') == 'success':
                    logger.info(f"✅ Successfully downloaded {model_name}")
                    progress_bar.progress(1.0)
                    return True
        return False
    except Exception as e:
        logger.error(f"❌ Error pulling model: {str(e)}")
        return False

# Initialize session state
if 'setup_complete' not in st.session_state:
    st.session_state.setup_complete = False
if 'red_team_model' not in st.session_state:
    st.session_state.red_team_model = "mistral:latest"
if 'target_model' not in st.session_state:
    st.session_state.target_model = "mistral:latest"
if 'blue_team_model' not in st.session_state:
    st.session_state.blue_team_model = "mistral:latest"
if 'test_results' not in st.session_state:
    st.session_state.test_results = []
if 'test_in_progress' not in st.session_state:
    st.session_state.test_in_progress = False
if 'custom_prompts' not in st.session_state:
    st.session_state.custom_prompts = []
if 'live_chat_messages' not in st.session_state:
    st.session_state.live_chat_messages = []
if 'chat_placeholder' not in st.session_state:
    st.session_state.chat_placeholder = None
if 'model_settings' not in st.session_state:
    st.session_state.model_settings = {
        'target': {'temperature': 1.0, 'top_p': 1.0, 'max_tokens': 2048},
        'red_team': {'temperature': 1.5, 'top_p': 0.9},
        'blue_team': {'temperature': 0.7, 'top_p': 0.8}
    }

# CSS Styles
st.markdown("""
<style>
.agent-box {
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.red-team { 
    background-color: rgba(255, 99, 71, 0.1); 
    border: 1px solid rgba(255, 99, 71, 0.3);
}
.target { 
    background-color: rgba(100, 149, 237, 0.1);
    border: 1px solid rgba(100, 149, 237, 0.3);
}
.blue-team { 
    background-color: rgba(60, 179, 113, 0.1);
    border: 1px solid rgba(60, 179, 113, 0.3);
}
.test-result {
    padding: 10px;
    border-radius: 5px;
    margin: 5px 0;
}
.success { background-color: rgba(0, 255, 0, 0.1); }
.failure { background-color: rgba(255, 0, 0, 0.1); }
.stButton>button {
    width: 100%;
}
.model-settings {
    padding: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 5px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

async def run_test_with_chat_updates(prompt, security_system, client):
    try:
        # Add test start message
        st.session_state.live_chat_messages.append({
            "role": "system",
            "content": f"Starting test with prompt: {prompt}",
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Run the test
        result = await security_system.test_prompt(
            prompt,
            st.session_state.red_team_model,
            st.session_state.target_model,
            st.session_state.blue_team_model,
            client
        )
        
        # Update chat with results
        for message in result.get('conversation', []):
            st.session_state.live_chat_messages.append(message)
            # Force refresh of chat display
            if st.session_state.chat_placeholder:
                with st.session_state.chat_placeholder.container():
                    for msg in st.session_state.live_chat_messages:
                        with st.chat_message(msg['role'], avatar='🔴' if msg['role'] == 'user' else '🎯'):
                            st.write(msg['content'])
                            st.caption(f"Time: {msg['timestamp']}")
        
        return result
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Setup Page
if not st.session_state.setup_complete:
    st.title("🛡️ PurPaaS LLM Testing Setup")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Target Configuration", "Agent Models", "Test Settings", "Download Models"])
    
    with tab1:
        st.header("🎯 Configure Target Model")
        st.markdown("""
        This is the main model that will be tested for security vulnerabilities. 
        Choose carefully as this will be the target of all security tests.
        """)
        
        available_models = get_ollama_models()
        
        st.markdown('<div class="agent-box target" style="padding: 30px;">', unsafe_allow_html=True)
        st.subheader("Select Target Model")
        st.session_state.target_model = st.selectbox(
            "Choose the model to test",
            available_models,
            key="target_select",
            help="This is the model that will be tested for vulnerabilities"
        )
        
        with st.expander("Target Model Settings"):
            st.session_state.model_settings['target']['temperature'] = st.slider(
                "Temperature",
                0.0, 2.0,
                st.session_state.model_settings['target']['temperature'],
                key="target_temperature"
            )
            st.session_state.model_settings['target']['top_p'] = st.slider(
                "Top P",
                0.0, 1.0,
                st.session_state.model_settings['target']['top_p'],
                key="target_top_p"
            )
            st.session_state.model_settings['target']['max_tokens'] = st.number_input(
                "Max Tokens",
                1, 4096,
                st.session_state.model_settings['target']['max_tokens'],
                key="target_max_tokens"
            )
        
        with st.expander("View Target System Prompt"):
            st.code(AGENT_PROMPTS["target"], language="text")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Preview section
        st.subheader("Target Model Preview")
        test_prompt = st.text_input("Enter a test prompt to see how the target model responds")
        if st.button("Test Response"):
            with st.spinner("Getting response from target model..."):
                try:
                    preview_agent = Agent(
                        name="Target",
                        instructions=AGENT_PROMPTS["target"],
                        model=st.session_state.target_model
                    )
                    
                    logger.info(f"Preview test using model: {st.session_state.target_model}")
                    
                    test_response = client.run(
                        agent=preview_agent,
                        messages=[{"role": "user", "content": test_prompt}]
                    )
                    
                    if hasattr(test_response, 'messages') and test_response.messages:
                        response_content = test_response.messages[-1]["content"]
                    else:
                        response_content = str(test_response)
                        
                    st.code(response_content)
                except Exception as e:
                    logger.error(f"Preview test error with model {st.session_state.target_model}: {str(e)}")
                    st.error(f"Error testing model: {str(e)}")
    
    with tab2:
        st.header("Configure Testing Agents")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="agent-box red-team">', unsafe_allow_html=True)
            st.subheader("🔴 Red Team Model")
            st.markdown("This agent attempts to find vulnerabilities")
            st.session_state.red_team_model = st.selectbox(
                "Select Red Team model",
                available_models,
                key="red_team_select"
            )
            with st.expander("Red Team Settings"):
                st.session_state.model_settings['red_team']['temperature'] = st.slider(
                    "Temperature",
                    0.0, 2.0,
                    st.session_state.model_settings['red_team']['temperature'],
                    key="red_team_temperature"
                )
                st.session_state.model_settings['red_team']['top_p'] = st.slider(
                    "Top P",
                    0.0, 1.0,
                    st.session_state.model_settings['red_team']['top_p'],
                    key="red_team_top_p"
                )
            with st.expander("View Red Team System Prompt"):
                st.code(AGENT_PROMPTS["red_team"], language="text")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="agent-box blue-team">', unsafe_allow_html=True)
            st.subheader("🔵 Blue Team Model")
            st.markdown("This agent analyzes security implications")
            st.session_state.blue_team_model = st.selectbox(
                "Select Blue Team model",
                available_models,
                key="blue_team_select"
            )
            with st.expander("Blue Team Settings"):
                st.session_state.model_settings['blue_team']['temperature'] = st.slider(
                    "Temperature",
                    0.0, 2.0,
                    st.session_state.model_settings['blue_team']['temperature'],
                    key="blue_team_temperature"
                )
                st.session_state.model_settings['blue_team']['top_p'] = st.slider(
                    "Top P",
                    0.0, 1.0,
                    st.session_state.model_settings['blue_team']['top_p'],
                    key="blue_team_top_p"
                )
            with st.expander("View Blue Team System Prompt"):
                st.code(AGENT_PROMPTS["blue_team"], language="text")
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.header("Test Configuration")
        
        col1, col2 = st.columns([2,1])
        with col1:
            st.subheader("Add Custom Test Prompts")
            new_prompt = st.text_area("Enter a custom test prompt")
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("Add Prompt", use_container_width=True):
                if new_prompt:
                    st.session_state.custom_prompts.append(new_prompt)
                    st.success("Prompt added!")
        
        st.subheader("Load Prompts from File")
        uploaded_file = st.file_uploader("Upload CSV file with prompts", type="csv")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if 'prompt' in df.columns:
                    for prompt in df['prompt'].tolist():
                        if prompt not in st.session_state.custom_prompts:
                            st.session_state.custom_prompts.append(prompt)
                    st.success(f"Loaded {len(df)} prompts from file!")
                else:
                    st.error("CSV file must contain a 'prompt' column")
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
        
        if st.session_state.custom_prompts:
            st.subheader("Manage Test Prompts")
            for i, prompt in enumerate(st.session_state.custom_prompts):
                col1, col2, col3 = st.columns([1, 5, 1])
                with col1:
                    st.write(f"#{i+1}")
                with col2:
                    st.text_area("Prompt", prompt, key=f"prompt_{i}", height=100)
                with col3:
                    if st.button("🗑️", key=f"delete_{i}"):
                        st.session_state.custom_prompts.pop(i)
                        st.rerun()
            
            if st.button("Export Prompts to CSV"):
                try:
                    df = pd.DataFrame({"prompt": st.session_state.custom_prompts})
                    df.to_csv("exported_prompts.csv", index=False)
                    st.success("Prompts exported to exported_prompts.csv")
                except Exception as e:
                    st.error(f"Error exporting prompts: {str(e)}")
    
    with tab4:
        st.header("Download Additional Models")
        available_remote_models = [
            "llama2", "mistral", "codellama", "neural-chat",
            "starling-lm", "orca-mini", "vicuna", "zephyr"
        ]
        
        col1, col2 = st.columns([3, 1])
        with col1:
            model_to_download = st.selectbox(
                "Select model to download",
                available_remote_models,
                key="model_download_select"
            )
        with col2:
            if st.button("Download Model", use_container_width=True):
                with st.spinner(f"Downloading {model_to_download}..."):
                    if pull_ollama_model(model_to_download):
                        st.success(f"Successfully downloaded {model_to_download}")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"Failed to download {model_to_download}")
        
        st.subheader("Available Models")
        local_models = get_ollama_models()
        if local_models:
            st.write("Currently installed:", ", ".join(local_models))
            
            st.subheader("Model Details")
            model_data = []
            for model in local_models:
                try:
                    response = requests.get(f'http://localhost:11434/api/show?name={model}')
                    if response.status_code == 200:
                        model_info = response.json()
                        model_data.append({
                            "Model": model,
                            "Size": f"{model_info.get('size', 0) / (1024*1024*1024):.1f}GB",
                            "Modified": model_info.get('modified', 'Unknown')
                        })
                except Exception as e:
                    logger.error(f"Error getting model info: {str(e)}")
            
            if model_data:
                df = pd.DataFrame(model_data)
                st.dataframe(df, use_container_width=True)
        else:
            st.info("No models currently installed. Download some models to get started!")
    
    st.markdown("---")
    if st.button("Start Security Testing", use_container_width=True):
        if not st.session_state.custom_prompts:
            st.error("Please add at least one test prompt before starting")
        else:
            st.session_state.setup_complete = True
            st.rerun()

# Testing Dashboard
else:
    st.title("🛡️ PurPaaS LLM Dashboard")
    
    # Initialize security testing system
    security_system = SecurityTestingSystem()
    
    # Sidebar controls
    with st.sidebar:
        st.header("Testing Controls")
        if st.button("Reset Configuration"):
            st.session_state.setup_complete = False
            st.session_state.test_results = []
            st.session_state.live_chat_messages = []
            st.rerun()
        
        st.header("Current Configuration")
        st.markdown(f"**Target Model**: {st.session_state.target_model}")
        st.markdown(f"**Red Team**: {st.session_state.red_team_model}")
        st.markdown(f"**Blue Team**: {st.session_state.blue_team_model}")
        
        with st.expander("Model Settings"):
            st.markdown("**Target Model:**")
            st.write(f"Temperature: {st.session_state.model_settings['target']['temperature']}")
            st.write(f"Top P: {st.session_state.model_settings['target']['top_p']}")
            st.write(f"Max Tokens: {st.session_state.model_settings['target']['max_tokens']}")
            
            st.markdown("**Red Team Model:**")
            st.write(f"Temperature: {st.session_state.model_settings['red_team']['temperature']}")
            st.write(f"Top P: {st.session_state.model_settings['red_team']['top_p']}")
            
            st.markdown("**Blue Team Model:**")
            st.write(f"Temperature: {st.session_state.model_settings['blue_team']['temperature']}")
            st.write(f"Top P: {st.session_state.model_settings['blue_team']['top_p']}")
    
    # Main testing interface
    col1, col2 = st.columns([2,1])
    
    with col1:
        st.header("Test Results")
        test_tab, chat_tab = st.tabs(["Test Controls", "Live Chat"])
        
        with test_tab:
            if st.session_state.test_results:
                for result in st.session_state.test_results:
                    with st.expander(f"Test Result - {result['timestamp']}"):
                        st.markdown("**Original Prompt:**")
                        st.code(result['prompt'])
                        
                        res_tab1, res_tab2, res_tab3 = st.tabs(["🔴 Red Team", "🎯 Target", "🔵 Blue Team"])
                        
                        with res_tab1:
                            st.markdown("**Red Team Results:**")
                            for i, test in enumerate(result['red_team_results']):
                                st.markdown(f"**Variation {i+1}:**")
                                st.code(test['variation'])
                                st.markdown("**Response:**")
                                st.code(test['response'])
                        
                        with res_tab2:
                            st.markdown("**Target Output:**")
                            st.code(result['target_output'])
                        
                        with res_tab3:
                            st.markdown("**Blue Team Analysis:**")
                            st.code(result['blue_team_analysis'])
            else:
                st.info("No test results yet. Run some tests to see results here.")
                
        with chat_tab:
            st.subheader("Live Testing Chat")
            chat_placeholder = st.empty()
            
            st.session_state.chat_placeholder = chat_placeholder
            
            with chat_placeholder.container():
                if st.session_state.live_chat_messages:
                    for message in st.session_state.live_chat_messages:
                        with st.chat_message(message['role'], avatar='🔴' if message['role'] == 'user' else '🎯'):
                            st.write(message['content'])
                            st.caption(f"Time: {message['timestamp']}")
                else:
                    st.info("No chat messages yet. Run some tests to see the conversation.")
            
            if st.button("Clear Chat History"):
                st.session_state.live_chat_messages = []
                st.rerun()
    
    with col2:
        st.header("Run Tests")
        
        # Full test suite
        if st.button("Run Test Suite", use_container_width=True) and not st.session_state.test_in_progress:
            st.session_state.test_in_progress = True
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, prompt in enumerate(st.session_state.custom_prompts):
                status_text.text(f"Testing prompt {i+1}/{len(st.session_state.custom_prompts)}")
                progress_bar.progress((i+1)/len(st.session_state.custom_prompts))
                result = asyncio.run(run_test_with_chat_updates(prompt, security_system, client))
                if result:
                    st.session_state.test_results.append(result)
            
            st.session_state.test_in_progress = False
            status_text.text("Testing complete!")
            st.rerun()
        
        # Quick single test
        st.markdown("---")
        st.subheader("Quick Test")
        quick_prompt = st.text_area("Enter prompt to test")
        if st.button("Run Quick Test", use_container_width=True):
            if quick_prompt:
                with st.spinner("Running test..."):
                    result = asyncio.run(run_test_with_chat_updates(quick_prompt, security_system, client))
                    if result:
                        st.session_state.test_results.append(result)
                        st.success("Test complete!")
                        st.rerun()
            else:
                st.warning("Please enter a prompt")
        
        # Export results
        if st.session_state.test_results:
            st.markdown("---")
            st.header("Export Results")
            if st.button("Export to CSV"):
                try:
                    # Create a flattened version of results for CSV
                    flattened_results = []
                    for result in st.session_state.test_results:
                        flat_result = {
                            "timestamp": result["timestamp"],
                            "original_prompt": result["prompt"],
                            "target_output": result["target_output"],
                            "blue_team_analysis": result["blue_team_analysis"]
                        }
                        for i, red_team_result in enumerate(result["red_team_results"]):
                            flat_result[f"variation_{i+1}"] = red_team_result["variation"]
                            flat_result[f"response_{i+1}"] = red_team_result["response"]
                        flattened_results.append(flat_result)
                    
                    df = pd.DataFrame(flattened_results)
                    df.to_csv("security_test_results.csv", index=False)
                    st.success("Results exported to security_test_results.csv")
                except Exception as e:
                    st.error(f"Error exporting results: {str(e)}")

if __name__ == "__main__":
    logging.info("🚀 Starting PurPaaS LLM Application")