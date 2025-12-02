import google.generativeai as genai
import os
from typing import Optional, List

class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        api_key = api_key or os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_summary(self, text: str, max_length: int = 500) -> str:
        """Generate summary of study material"""
        try:
            prompt = f"Please provide a concise summary (max {max_length} words) of the following text:\n\n{text}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def generate_quiz(self, material_text: str, num_questions: int = 5) -> List[dict]:
        """Generate quiz questions from material"""
        try:
            prompt = f"Generate exactly {num_questions} multiple choice quiz questions from the following material. Return as JSON array with keys: question, options (list of 4), correct_answer (0-3):\n\n{material_text}"
            response = self.model.generate_content(prompt)
            return self._parse_quiz_response(response.text)
        except Exception as e:
            return []
    
    def generate_flashcards(self, material_text: str, num_cards: int = 10) -> List[dict]:
        """Generate flashcard pairs from material"""
        try:
            prompt = f"Generate {num_cards} key concept flashcards from this material. Return as JSON array with keys: front, back:\n\n{material_text}"
            response = self.model.generate_content(prompt)
            return self._parse_flashcard_response(response.text)
        except Exception as e:
            return []
    
    def generate_study_plan(self, material_text: str, study_days: int = 7) -> str:
        """Generate personalized study plan"""
        try:
            prompt = f"Create a {study_days}-day study plan for this material with daily goals:\n\n{material_text}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating study plan: {str(e)}"
    
    def explain_concept(self, concept: str, context: str = "") -> str:
        """Explain a specific concept"""
        try:
            prompt = f"Explain the following concept in simple terms: {concept}"
            if context:
                prompt += f"\nContext: {context}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error explaining concept: {str(e)}"
    
    def _parse_quiz_response(self, response: str) -> List[dict]:
        import json
        try:
            import re
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return []
    
    def _parse_flashcard_response(self, response: str) -> List[dict]:
        import json
        try:
            import re
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return []
