"""
Gemini AI Service
Handles all AI vision and chat operations
"""

import google.generativeai as genai
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiAnalyzer:
    """
    AI analyzer using Google Gemini Vision API
    """
    
    def __init__(self):
        """Initialize Gemini with API key"""
        # Get API key from environment variable
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set!")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # ✅ LIST ALL AVAILABLE MODELS
        print("\n" + "="*60)
        print("📋 CHECKING AVAILABLE GEMINI MODELS:")
        print("="*60)
        
        available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    model_name = m.name
                    print(f"✅ Found: {model_name}")
                    available_models.append(model_name)
        except Exception as e:
            print(f"❌ Error listing models: {e}")
        
        print("="*60)
        
        # ✅ TRY MODELS IN ORDER OF PREFERENCE
        models_to_try = [
    'gemini-2.5-pro',
    'models/gemini-2.5-pro',
    'gemini-flash-latest',
    'models/gemini-flash-latest',
    'gemini-pro-latest',
    'models/gemini-pro-latest'
]
        
        model_initialized = False
        
        print("\n🔄 Attempting to initialize model...")
        for model_name in models_to_try:
            try:
                print(f"   Trying: {model_name}... ", end="")
                self.model = genai.GenerativeModel(model_name)
                # Test the model works
                test_response = self.model.generate_content("Hi")
                print(f"✅ SUCCESS!")
                print(f"\n🎯 Using model: {model_name}\n")
                model_initialized = True
                break
            except Exception as e:
                print(f"❌ Failed: {str(e)[:50]}")
                continue
        
        if not model_initialized:
            # Last resort - use first available model
            if available_models:
                first_model = available_models[0]
                # Remove 'models/' prefix if present for trying
                clean_name = first_model.replace('models/', '')
                print(f"\n🔄 Trying first available: {clean_name}")
                try:
                    self.model = genai.GenerativeModel(clean_name)
                    print(f"✅ Initialized with: {clean_name}\n")
                except:
                    # Try with models/ prefix
                    self.model = genai.GenerativeModel(first_model)
                    print(f"✅ Initialized with: {first_model}\n")
            else:
                raise ValueError("❌ No compatible models found! Check your API key.")
        
        print("✅ Gemini AI initialized successfully\n")
    
    def _get_mime_type(self, file_path: str) -> str:
        """Get MIME type from file extension"""
        extension = Path(file_path).suffix.lower()
        
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.webp': 'image/webp',
            '.gif': 'image/gif'
        }
        
        return mime_types.get(extension, 'image/jpeg')
    
    def analyze_kibble_label(self, image_path: str) -> Optional[Dict[str, Any]]:
        """
        Analyze kibble nutrition label and extract data
        
        Args:
            image_path: Path to the label image
            
        Returns:
            dict: Extracted nutrition data or None if failed
        """
        try:
            # Read image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Prepare image for Gemini
            image_parts = [{
                "mime_type": self._get_mime_type(image_path),
                "data": image_data
            }]
            
            # Create prompt
            prompt = """
Analyze this pet food nutrition label. Find the GUARANTEED ANALYSIS section.

Extract ONLY these specific values:
1. CRUDE PROTEIN (MINIMUM) % - Look for "Crude Protein (min)"
2. CRUDE FAT (MINIMUM) % - Look for "Crude Fat (min)"
3. CRUDE FIBER (MAXIMUM) % - Look for "Crude Fiber (max)"
4. MOISTURE (MAXIMUM) % - Look for "Moisture (max)"
5. ASH % - Look for "Ash (max)" (if present, otherwise use 0)

CRITICAL - DO NOT CONFUSE:
- Moisture is NOT protein
- Ash is NOT fat
- NFE is NOT fiber

Only extract values from the GUARANTEED ANALYSIS table.
Ignore other sections like feeding guidelines or calorie content.

Return ONLY a valid JSON object with these exact fields (no markdown, no explanations):

{
    "brand_name": "exact brand name from label",
    "product_line": "product line/variant if visible",
    "protein_pct": numeric_value_from_crude_protein_minimum,
    "fat_pct": numeric_value_from_crude_fat_minimum,
    "fiber_pct": numeric_value_from_crude_fiber_maximum,
    "moisture_pct": numeric_value_from_moisture_maximum,
    "ash_pct": numeric_value_from_ash_or_0,
    "price_per_kg": 0
}

RULES:
- All percentage values must be numbers (not strings)
- Only extract from "Crude Protein (min)", "Crude Fat (min)", "Crude Fiber (max)"
- If ash is not visible, use 0
- If any value is unclear, use 0
- Return ONLY the JSON object, no other text
- Do NOT wrap in markdown code blocks

Example label reading:
If label shows:
  Crude Protein (min) ... 30%
  Crude Fat (min) ....... 15%
  Crude Fiber (max) ..... 3%
  Moisture (max) ........ 10%
  
Return:
{
    "protein_pct": 30,
    "fat_pct": 15,
    "fiber_pct": 3,
    "moisture_pct": 10,
    ...
}
"""
            
            # Generate content
            response = self.model.generate_content([prompt, image_parts[0]])
            
            # Parse response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()
            
            # Parse JSON
            result = json.loads(response_text)
            
            # Validate required fields
            required_fields = ['brand_name', 'protein_pct', 'fat_pct', 'fiber_pct', 'moisture_pct']
            
            for field in required_fields:
                if field not in result:
                    print(f"Missing required field: {field}")
                    return None
            
            # Convert percentages to float
            for key in ['protein_pct', 'fat_pct', 'fiber_pct', 'moisture_pct', 'ash_pct', 'price_per_kg']:
                if key in result:
                    try:
                        result[key] = float(result[key])
                    except (ValueError, TypeError):
                        result[key] = 0.0
            
            print(f"✅ Successfully analyzed label: {result['brand_name']}")
            return result
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Response was: {response_text}")
            return None
            
        except Exception as e:
            print(f"❌ Error analyzing label: {e}")
            return None
    
    def analyze_image_with_prompt(self, image_path: str, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Analyze image with custom prompt
        
        Args:
            image_path: Path to image file
            prompt: Custom prompt for analysis
            
        Returns:
            dict: Parsed JSON response from Gemini
        """
        try:
            # Read image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Prepare image for Gemini
            image_parts = [{
                "mime_type": self._get_mime_type(image_path),
                "data": image_data
            }]
            
            # Generate content with custom prompt
            response = self.model.generate_content([prompt, image_parts[0]])
            
            # Parse JSON response
            response_text = response.text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()
            
            # Parse JSON
            result = json.loads(response_text)
            
            print(f"✅ Successfully analyzed image with custom prompt")
            return result
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Response text: {response_text}")
            return None
            
        except Exception as e:
            print(f"❌ Error analyzing image: {e}")
            return None
    
    def chat(self, prompt: str) -> str:
        """
        Chat with Gemini AI
        
        Args:
            prompt: User's question or prompt
            
        Returns:
            str: AI response
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"❌ Chat error: {e}")
            return "Sorry, I encountered an error. Please try again."
    
    def analyze_cat_photo(self, image_path: str) -> Optional[Dict[str, Any]]:
        """
        Analyze cat photo for body condition
        
        Args:
            image_path: Path to cat photo
            
        Returns:
            dict: Analysis results
        """
        prompt = """
        Analyze this cat photo and provide a body condition assessment.
        
        Return ONLY a valid JSON object with these exact fields:
        
        {
            "bcs": 5,
            "weight_assessment": "Ideal",
            "health_notes": "Overall appearance is healthy. Coat looks shiny and well-maintained.",
            "recommended_food": "High protein, moderate fat, low carbohydrate",
            "feeding_suggestions": "Maintain current feeding schedule. Ensure fresh water is always available."
        }
        
        Body Condition Score (BCS) scale:
        - 1-3: Underweight
        - 4-5: Ideal
        - 6-7: Overweight
        - 8-9: Obese
        
        Weight assessment options: "Underweight", "Ideal", "Overweight", "Obese"
        
        Return ONLY the JSON object, no markdown blocks or explanations.
        """
        
        return self.analyze_image_with_prompt(image_path, prompt)


# Test function
if __name__ == "__main__":
    try:
        analyzer = GeminiAnalyzer()
        print("Gemini service is working correctly!")
    except Exception as e:
        print(f"Error: {e}")