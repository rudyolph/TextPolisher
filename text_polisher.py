import os
import time
import threading
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
import keyboard
import pyperclip
from google import genai
from dotenv import load_dotenv



# Global state
_cached_client = None
_cached_api_key = None
_tray_icon = None

# Colors
COLOR_NORMAL = (100, 200, 255) # Light Blue
COLOR_THINKING = (255, 165, 0)  # Orange
COLOR_ERROR = (255, 0, 0)       # Red
# load_dotenv() is now called inside process_text for dynamic reloading

SYSTEM_PROMPT = """You are a message rewriter. Rewrite the user's message to sound professional and friendly. Preserve the original meaning and intent. Keep it natural, not robotic or overly formal. Keep the same approximate length.
Return ONLY the rewritten message with no commentary, preamble, or quotes.

IMPORTANT STYLE RULES — the output must read like a real human typed it:
- Never use em dashes (—) or en dashes (–). Use commas, periods, ellipses, or separate sentences instead.
- Never use semicolons unless it was in the original text.
- Never use bullet points or numbered lists unless it was in the original text.
- Avoid overly polished transitions like 'however', 'furthermore', 'additionally', 'moreover'.
- Avoid filler phrases like 'I wanted to reach out', 'I hope this finds you well', 'please don't hesitate to'.
- Use simple, everyday words. Prefer 'use' over 'utilize', 'help' over 'assist', 'start' over 'initiate', 'get' over 'obtain'.
- Keep contractions (I'm, don't, can't, won't) — they sound more natural.
- Write like a normal person sending an email or text message, not like a corporate email template.

INLINE DIRECTIVES:

The user's text may contain directives inside curly braces like {ai: some instruction}. When you see these, follow the instruction and replace the directive with the generated content, blending it naturally into the surrounding text. Remove the curly braces from the output. If there are no curly-brace directives, just polish the text normally."""

def process_text():
    global _cached_client, _cached_api_key, _tray_icon
    
    print("\n--- Processing Polish Request ---")
    
    # Change icon to 'Thinking' color
    if _tray_icon:
        _tray_icon.icon = create_image(COLOR_THINKING)

    try:
        # 1. Wait for user to release hotkey
        while keyboard.is_pressed('ctrl') or keyboard.is_pressed('alt') or keyboard.is_pressed('p'):
            time.sleep(0.01)
        
        # 2. Capture Text (Ctrl+C)
        original_clipboard = pyperclip.paste()
        dummy_str = "___POLISHER_EMPTY___"
        pyperclip.copy(dummy_str)
        
        keyboard.send('ctrl+c')
        time.sleep(0.2) 
        
        current_clipboard = pyperclip.paste()
        
        source_text = None
        if current_clipboard != dummy_str and current_clipboard.strip():
            source_text = current_clipboard
            print("Captured selected text.")
        elif original_clipboard.strip():
            source_text = original_clipboard
            print("Using text from clipboard.")
            
        if not source_text:
            print("ERROR: No text found. Aborting.")
            if _tray_icon:
                _tray_icon.icon = create_image(COLOR_ERROR)
                _tray_icon.notify("Make sure you have text selected or in your clipboard.", title="No Text Found")
                threading.Timer(3.0, lambda: setattr(_tray_icon, 'icon', create_image(COLOR_NORMAL))).start()
            pyperclip.copy(original_clipboard)
            return

        # 3. Environment & Client Prep
        load_dotenv(override=True)
        api_key = os.getenv("GEMINI_API_KEY")
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        
        if not _cached_client or _cached_api_key != api_key:
            _cached_api_key = api_key
            _cached_client = genai.Client(api_key=api_key)
            print("Initialized fresh API client.")

        # 4. Gemini API Call
        print(f"Calling Gemini API ({model_name})...")
        response = _cached_client.models.generate_content(
            model=model_name,
            contents=source_text,
            config=genai.types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
        )
        
        polished_text = response.text
        if not polished_text:
            print("ERROR: Received empty response from Gemini API.")
            if _tray_icon:
                _tray_icon.icon = create_image(COLOR_ERROR)
                _tray_icon.notify("Received an empty response from the AI.", title="Polish Failed")
                threading.Timer(3.0, lambda: setattr(_tray_icon, 'icon', create_image(COLOR_NORMAL))).start()
            pyperclip.copy(original_clipboard)
            return
            
        # 5. Paste & Restore
        pyperclip.copy(polished_text)
        keyboard.send('ctrl+v')
        time.sleep(0.3) 
        
        pyperclip.copy(original_clipboard)
        print("SUCCESS: Text polished and pasted.")
        
    except Exception as e:
        error_msg = str(e)
        print(f"AN ERROR OCCURRED: {error_msg}")
        if _tray_icon:
            _tray_icon.icon = create_image(COLOR_ERROR)
            # Simplify error message for the notification
            clean_msg = error_msg.split('{')[0] if '{' in error_msg else error_msg
            _tray_icon.notify(clean_msg, title="TextPolisher Error")
            threading.Timer(3.0, lambda: setattr(_tray_icon, 'icon', create_image(COLOR_NORMAL))).start()
        try:
            pyperclip.copy(original_clipboard)
        except:
            pass
    finally:
        # Restore icon to 'Normal' color
        if _tray_icon:
            _tray_icon.icon = create_image(COLOR_NORMAL)

def on_activate():
    threading.Thread(target=process_text, daemon=True).start()

def create_image(color=COLOR_NORMAL):
    # Create a basic 'P' icon for the tray
    image = Image.new('RGB', (64, 64), color=(30, 30, 30))
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill=color)
    return image

def quit_action(icon, item):
    print("Exiting...")
    icon.stop()
    os._exit(0)

def setup_tray():
    global _tray_icon
    # Setup global hotkey
    try:
        keyboard.add_hotkey('ctrl+alt+p', on_activate)
        print("Hotkey registered: ctrl+alt+p")
    except ImportError as e:
        print(f"Failed to register hotkey. Make sure you run as Administrator. Error: {e}")
        return

    # Setup tray icon
    menu = pystray.Menu(item('Quit', quit_action))
    _tray_icon = pystray.Icon("TextPolisher", create_image(), "TextPolisher", menu)
    
    print("Starting TextPolisher System Tray...")
    _tray_icon.run()

if __name__ == '__main__':
    setup_tray()
