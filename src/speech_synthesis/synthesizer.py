"""
Speech Synthesizer
Converts recognized text to speech output
Note: OpenAI Whisper is primarily for speech recognition, so we use TTS alternatives
"""

import os
try:
    import pyttsx3
except ImportError:
    print("Warning: pyttsx3 not installed. Install with: pip install pyttsx3")
    pyttsx3 = None

try:
    from gtts import gTTS
    import pygame
except ImportError:
    print("Warning: gTTS or pygame not installed. Install with: pip install gtts pygame")
    gTTS = None
    pygame = None


class SpeechSynthesizer:
    """
    Text-to-Speech synthesizer using multiple backends
    """
    
    def __init__(self, engine='pyttsx3', rate=150, volume=1.0):
        """
        Initialize speech synthesizer
        
        Args:
            engine: TTS engine to use ('pyttsx3' or 'gtts')
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        self.engine_type = engine
        self.rate = rate
        self.volume = volume
        self.engine = None
        
        if engine == 'pyttsx3' and pyttsx3 is not None:
            self._init_pyttsx3()
        elif engine == 'gtts' and gTTS is not None:
            self._init_gtts()
        else:
            print(f"Warning: {engine} not available, no TTS will be used")
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 engine"""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            if voices:
                # Set a default voice (first available)
                self.engine.setProperty('voice', voices[0].id)
            
            print("pyttsx3 TTS engine initialized successfully")
        except Exception as e:
            print(f"Error initializing pyttsx3: {e}")
            self.engine = None
    
    def _init_gtts(self):
        """Initialize gTTS (requires internet connection)"""
        try:
            if pygame is not None:
                pygame.mixer.init()
            print("gTTS engine initialized (requires internet)")
            self.engine = 'gtts'
        except Exception as e:
            print(f"Error initializing gTTS: {e}")
            self.engine = None
    
    def speak(self, text):
        """
        Convert text to speech and play it
        
        Args:
            text: Text string to convert to speech
        """
        if not text or text.strip() == "":
            return
        
        if self.engine_type == 'pyttsx3' and self.engine is not None:
            self._speak_pyttsx3(text)
        elif self.engine_type == 'gtts' and self.engine is not None:
            self._speak_gtts(text)
        else:
            print(f"Speech output: {text}")
    
    def _speak_pyttsx3(self, text):
        """Speak using pyttsx3"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error speaking with pyttsx3: {e}")
    
    def _speak_gtts(self, text):
        """Speak using gTTS"""
        try:
            # Create temporary audio file
            temp_file = "/tmp/speech_output.mp3"
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_file)
            
            # Play the audio file
            if pygame is not None:
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                # Clean up
                pygame.mixer.music.unload()
            
            # Remove temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        except Exception as e:
            print(f"Error speaking with gTTS: {e}")
    
    def speak_async(self, text):
        """
        Speak text asynchronously (non-blocking)
        
        Args:
            text: Text to speak
        """
        import threading
        
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.daemon = True
        thread.start()
    
    def set_rate(self, rate):
        """
        Set speech rate
        
        Args:
            rate: Speech rate in words per minute
        """
        self.rate = rate
        if self.engine_type == 'pyttsx3' and self.engine is not None:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume):
        """
        Set volume level
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        if self.engine_type == 'pyttsx3' and self.engine is not None:
            self.engine.setProperty('volume', self.volume)
    
    def set_voice(self, voice_id=None):
        """
        Set voice for speech synthesis
        
        Args:
            voice_id: Voice identifier (if None, uses default)
        """
        if self.engine_type == 'pyttsx3' and self.engine is not None:
            voices = self.engine.getProperty('voices')
            if voices:
                if voice_id is not None and voice_id < len(voices):
                    self.engine.setProperty('voice', voices[voice_id].id)
                else:
                    self.engine.setProperty('voice', voices[0].id)
    
    def list_voices(self):
        """
        List available voices
        
        Returns:
            voices: List of available voice names
        """
        if self.engine_type == 'pyttsx3' and self.engine is not None:
            voices = self.engine.getProperty('voices')
            return [(i, v.name) for i, v in enumerate(voices)]
        return []
    
    def stop(self):
        """Stop current speech"""
        if self.engine_type == 'pyttsx3' and self.engine is not None:
            try:
                self.engine.stop()
            except:
                pass
        elif self.engine_type == 'gtts' and pygame is not None:
            try:
                pygame.mixer.music.stop()
            except:
                pass
    
    def cleanup(self):
        """Clean up resources"""
        self.stop()
        if self.engine_type == 'gtts' and pygame is not None:
            try:
                pygame.mixer.quit()
            except:
                pass
