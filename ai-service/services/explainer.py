import os
import openai
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class AIExplainer:
    def __init__(self):
        # Initialize OpenAI API (you'll need to set your API key)
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        if not openai.api_key:
            print("Warning: OpenAI API key not set. Using fallback explanations.")
    
    def explain(self, text: str, context: Optional[str] = "") -> str:
        """Generate an explanation for the selected text"""
        if not text:
            return "Please select text to explain."
        
        try:
            if openai.api_key:
                # Use OpenAI to generate an explanation
                prompt = f"Explain the following text in simple terms:\n\n{text}\n\nContext: {context}"
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful educational assistant that explains complex concepts in simple terms."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                
                return response.choices[0].message.content
            else:
                # Fallback explanation if API key is not available
                return self._generate_fallback_explanation(text)
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return f"Sorry, I couldn't generate an explanation for this text. Error: {str(e)}"
    
    def _generate_fallback_explanation(self, text: str) -> str:
        """Generate a simple fallback explanation when API is unavailable"""
        # This is a very basic fallback
        return f"This would provide an AI-generated explanation for: '{text[:100]}...'"
