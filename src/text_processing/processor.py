"""
Text Processor using Llama 2
Processes lip movement patterns and generates coherent text
"""

import numpy as np
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    import torch
except ImportError:
    print("Warning: transformers not installed. Install with: pip install transformers torch")
    AutoTokenizer = None
    AutoModelForCausalLM = None
    pipeline = None


class TextProcessor:
    """
    Text processing and generation using Llama 2 model
    """
    
    def __init__(self, model_name="meta-llama/Llama-2-7b-chat-hf", use_local=False):
        """
        Initialize the text processor
        
        Args:
            model_name: HuggingFace model name or local path
            use_local: Whether to use a local model path
        """
        self.model_name = model_name
        self.use_local = use_local
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Movement to phoneme mapping (simplified for demonstration)
        self.movement_patterns = {
            'small': ['i', 'e'],
            'medium': ['a', 'o'],
            'large': ['ah', 'oo'],
            'rapid': ['t', 'k', 'p']
        }
        
        self.text_buffer = []
        self.context_window = 10  # Keep last 10 recognized elements
        
    def load_model(self):
        """
        Load the Llama 2 model
        Note: Requires authentication token for Llama 2 from HuggingFace
        """
        if AutoTokenizer is None or AutoModelForCausalLM is None:
            raise ImportError("transformers library is required")
        
        try:
            print(f"Loading Llama 2 model: {self.model_name}")
            print("Note: This requires HuggingFace authentication for Llama 2 models")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
            print(f"Model loaded successfully on {self.device}")
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Using fallback mode without Llama 2")
            return False
    
    def analyze_movement_pattern(self, movement_history):
        """
        Analyze lip movement pattern to extract features
        
        Args:
            movement_history: List of movement magnitudes
            
        Returns:
            pattern_type: String describing the pattern
        """
        if len(movement_history) == 0:
            return 'none'
        
        avg_magnitude = np.mean(movement_history)
        std_magnitude = np.std(movement_history)
        
        # Classify movement pattern
        if avg_magnitude < 3.0:
            return 'small'
        elif avg_magnitude < 7.0:
            return 'medium'
        elif std_magnitude > 2.0:
            return 'rapid'
        else:
            return 'large'
    
    def pattern_to_phoneme(self, pattern_type):
        """
        Convert movement pattern to phoneme
        
        Args:
            pattern_type: Type of movement pattern
            
        Returns:
            phoneme: Corresponding phoneme
        """
        phonemes = self.movement_patterns.get(pattern_type, [''])
        return phonemes[0] if phonemes else ''
    
    def process_movement(self, movement_history):
        """
        Process lip movement history and generate text
        
        Args:
            movement_history: List of recent movement magnitudes
            
        Returns:
            recognized_text: Generated or recognized text
        """
        pattern_type = self.analyze_movement_pattern(movement_history)
        phoneme = self.pattern_to_phoneme(pattern_type)
        
        if phoneme:
            self.text_buffer.append(phoneme)
            
            # Keep buffer limited
            if len(self.text_buffer) > self.context_window:
                self.text_buffer.pop(0)
        
        # Combine phonemes into text
        recognized_text = ''.join(self.text_buffer)
        return recognized_text
    
    def generate_text(self, prompt, max_length=50):
        """
        Generate text using Llama 2 model
        
        Args:
            prompt: Input prompt for generation
            max_length: Maximum length of generated text
            
        Returns:
            generated_text: Model-generated text
        """
        if self.model is None or self.tokenizer is None:
            # Fallback: return prompt with simple completion
            return prompt + " [Model not loaded - using fallback]"
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return generated_text
            
        except Exception as e:
            print(f"Error generating text: {e}")
            return prompt
    
    def complete_sentence(self, partial_text):
        """
        Complete a partial sentence using Llama 2
        
        Args:
            partial_text: Partial text to complete
            
        Returns:
            completed_text: Completed sentence
        """
        if not partial_text:
            return ""
        
        prompt = f"Complete this sentence naturally: {partial_text}"
        completed = self.generate_text(prompt, max_length=100)
        
        # Extract only the completion part
        if ":" in completed:
            completed = completed.split(":", 1)[1].strip()
        
        return completed
    
    def predict_next_word(self, context):
        """
        Predict the next word based on context
        
        Args:
            context: Current text context
            
        Returns:
            predicted_word: Next predicted word
        """
        if self.model is None:
            return ""
        
        try:
            inputs = self.tokenizer(context, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=5,
                    num_return_sequences=1,
                    temperature=0.5,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            predicted = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract only new tokens
            new_text = predicted[len(context):].strip()
            return new_text.split()[0] if new_text else ""
            
        except Exception as e:
            print(f"Error predicting next word: {e}")
            return ""
    
    def reset_buffer(self):
        """Clear the text buffer"""
        self.text_buffer = []
    
    def get_current_text(self):
        """Get current buffered text"""
        return ''.join(self.text_buffer)
