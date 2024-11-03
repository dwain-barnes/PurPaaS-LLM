import asyncio
from datetime import datetime
import logging
import test_generator
import agent_prompts
from swarm import Agent

logger = logging.getLogger(__name__)

class SecurityTestingSystem:
    def __init__(self):
        self.test_generator = test_generator.SecurityTestGenerator()
        
    async def test_prompt(self, prompt, red_team_model, target_model, blue_team_model, client):
        """Run security test with specified models"""
        try:
            # Initialize conversation history
            conversation = []
            
            # Store original prompt in conversation
            conversation.append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now().strftime("%H:%M")
            })

            # Generate variations
            variations = self.test_generator.generate_prompt_variations(prompt)
            test_results = []
            
            # Red Team Phase
            logger.info("🔴 Starting Red Team testing phase...")
            for variation in variations[:5]:  # Limit to 5 variations for demonstration
                logger.info(f"Using red team model: {red_team_model}")
                
                # Add variation to conversation
                conversation.append({
                    "role": "user",
                    "content": f"[Red Team Variation] {variation}",
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
                red_agent = Agent(
                    name="Red Team",
                    instructions=agent_prompts.AGENT_PROMPTS["red_team"],
                    model=red_team_model
                )
                
                red_result = client.run(
                    agent=red_agent,
                    messages=[{"role": "user", "content": variation}]
                )
                
                if hasattr(red_result, 'messages') and red_result.messages:
                    response_content = red_result.messages[-1]["content"]
                else:
                    response_content = str(red_result)
                    
                # Add red team response to conversation
                conversation.append({
                    "role": "assistant",
                    "content": f"[Red Team Response] {response_content}",
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
                test_results.append({
                    "variation": variation,
                    "response": response_content
                })
            
            # Target Phase
            logger.info(f"🎯 Testing target model: {target_model}")
            target_agent = Agent(
                name="Target",
                instructions=agent_prompts.AGENT_PROMPTS["target"],
                model=target_model
            )
            
            # Add target test to conversation
            conversation.append({
                "role": "user",
                "content": "[Target Test] Original prompt being tested on target model",
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            target_result = client.run(
                agent=target_agent,
                messages=[{"role": "user", "content": prompt}]
            )
            
            if hasattr(target_result, 'messages') and target_result.messages:
                target_response = target_result.messages[-1]["content"]
            else:
                target_response = str(target_result)
            
            # Add target response to conversation
            conversation.append({
                "role": "assistant",
                "content": target_response,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            # Blue Team Analysis
            logger.info(f"🔵 Starting Blue Team analysis with model: {blue_team_model}")
            analysis_prompt = f"""Analyze these test results:
            Original Prompt: {prompt}
            Test Results: {test_results}
            Target Response: {target_response}
            """
            
            # Add blue team analysis request to conversation
            conversation.append({
                "role": "user",
                "content": "[Blue Team] Requesting security analysis",
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            blue_agent = Agent(
                name="Blue Team",
                instructions=agent_prompts.AGENT_PROMPTS["blue_team"],
                model=blue_team_model
            )
            
            blue_result = client.run(
                agent=blue_agent,
                messages=[{"role": "user", "content": analysis_prompt}]
            )
            
            if hasattr(blue_result, 'messages') and blue_result.messages:
                blue_response = blue_result.messages[-1]["content"]
            else:
                blue_response = str(blue_result)
            
            # Add blue team analysis to conversation
            conversation.append({
                "role": "assistant",
                "content": f"[Blue Team Analysis] {blue_response}",
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            return {
                "prompt": prompt,
                "red_team_results": test_results,
                "target_output": target_response,
                "blue_team_analysis": blue_response,
                "timestamp": datetime.now().isoformat(),
                "models_used": {
                    "red_team": red_team_model,
                    "target": target_model,
                    "blue_team": blue_team_model
                },
                "conversation": conversation
            }
            
        except Exception as e:
            logger.error(f"Error in test_prompt: {str(e)}")
            logger.error(f"Failed model details - Target: {target_model}, Red Team: {red_team_model}, Blue Team: {blue_team_model}")
            raise