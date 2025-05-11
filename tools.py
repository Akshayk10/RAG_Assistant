import requests
import math
import re

def calculator_tool(query):
    """Safe calculation with proper error handling"""
    try:
        # Extract math expression (remove "calculate" and non-math characters)
        expression = re.sub(r'[^\d+\-*/(). ]', '', 
                          query.lower().replace("calculate", "").strip())
        
        # Security check - only allow basic math operations
        if not re.fullmatch(r'^[\d+\-*/(). ]+$', expression):
            return "Error: Only numbers and +-*/.() allowed"
            
        # Evaluate safely
        result = eval(expression, {'__builtins__': None}, {
            'abs': abs,
            'round': round,
            'sqrt': math.sqrt,
            'log': math.log,
            'log10': math.log10
        })
        
        # Format display
        return {
            "result": result,
            "expression": expression,
            "formatted": f"**Calculation:** {expression} = **{result}**"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "formatted": f"❌ Calculation failed: {str(e)}"
        }

def dictionary_tool(query):
    """Real dictionary API integration"""
    try:
        # Extract word (handle "define x", "what is x", etc.)
        word = re.sub(r'define|what is|meaning of|\?', '', 
                     query.lower()).strip()
        
        # Free Dictionary API
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        data = response.json()
        
        if isinstance(data, list):
            meanings = data[0]['meanings'][0]
            definition = meanings['definitions'][0]['definition']
            example = meanings['definitions'][0].get('example', 'No example available')
            part_of_speech = meanings['partOfSpeech']
            
            return {
                "word": word,
                "definition": definition,
                "example": example,
                "partOfSpeech": part_of_speech,
                "formatted": (
                    f"**{word.capitalize()}** ({part_of_speech})\n\n"
                    f"**Definition:** {definition}\n\n"
                    f"**Example:** _{example}_"
                )
            }
        return {
            "error": "No definition found",
            "formatted": f"Couldn't find definition for '{word}'"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "formatted": f"Dictionary service unavailable: {str(e)}"
        }
