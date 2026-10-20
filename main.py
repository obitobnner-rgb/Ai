from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
import requests
import threading

# Yahan apni API Key zaroor dalein
API_KEY = "aapki_openrouter_api_key_yahan_dalein" 
MODEL = "cognitivecomputations/dolphin-mixtral-8x7b"

class ObitoAI(App):
    def build(self):
        self.title = "Obito AI"
        # Theme - Dark Sci-Fi Blue Background
        Window.clearcolor = (0.05, 0.08, 0.12, 1) 
        
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        self.last_response = ""
        
        # --- Top Bar (Title & Tools) ---
        top_bar = BoxLayout(size_hint=(1, 0.1), spacing=10)
        title_label = Label(text="[b][color=00FFFF]OBITO AI[/color][/b]", markup=True, font_size='22sp', size_hint=(0.5, 1))
        
        clear_btn = Button(text="Clear Chat", size_hint=(0.25, 1), background_color=(0.9, 0.2, 0.2, 1), bold=True)
        clear_btn.bind(on_press=self.clear_chat)
        
        copy_btn = Button(text="Copy Last", size_hint=(0.25, 1), background_color=(0.2, 0.6, 0.8, 1), bold=True)
        copy_btn.bind(on_press=self.copy_last)
        
        top_bar.add_widget(title_label)
        top_bar.add_widget(clear_btn)
        top_bar.add_widget(copy_btn)
        self.layout.add_widget(top_bar)
        
        # --- Chat History Area ---
        self.scroll = ScrollView(size_hint=(1, 0.75))
        self.chat_history = Label(
            size_hint_y=None, 
            text="[color=00FF00]Obito AI System Initialized... Ready![/color]\n\n", 
            halign="left", 
            valign="top", 
            markup=True,
            font_size='16sp'
        )
        self.chat_history.bind(
            width=lambda *x: self.chat_history.setter('text_size')(self.chat_history, (self.chat_history.width, None)), 
            texture_size=lambda *x: self.chat_history.setter('height')(self.chat_history, self.chat_history.texture_size[1])
        )
        self.scroll.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll)
        
        # --- Input Area ---
        input_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        self.user_input = TextInput(
            hint_text="Ask Obito AI anything...", 
            multiline=False, 
            background_color=(0.15, 0.18, 0.22, 1), 
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 1, 1, 1),
            font_size='16sp',
            padding=(10, 15)
        )
        self.send_btn = Button(
            text="SEND", 
            size_hint=(0.3, 1), 
            background_color=(0.1, 0.8, 0.4, 1), 
            bold=True,
            font_size='16sp'
        )
        self.send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(self.send_btn)
        self.layout.add_widget(input_layout)
        
        return self.layout
        
    def clear_chat(self, instance):
        self.chat_history.text = "[color=00FF00]Chat memory cleared. Ready.[/color]\n\n"
        
    def copy_last(self, instance):
        if self.last_response:
            Clipboard.copy(self.last_response)
            self.update_ui("[color=FFFF00]System: Last response copied to clipboard![/color]\n\n")

    def send_message(self, instance):
        user_text = self.user_input.text.strip()
        if not user_text: return
        
        # User ki formatting (Cyan color)
        self.update_ui(f"[color=00FFFF]You:[/color] {user_text}\n\n")
        self.user_input.text = ""
        self.send_btn.text = "Wait..."
        self.send_btn.disabled = True
        
        threading.Thread(target=self.fetch_response, args=(user_text,)).start()

    def fetch_response(self, user_text):
        headers = {"Authorization": f"Bearer {API_KEY}"}
        data = {"model": MODEL, "messages": [{"role": "user", "content": user_text}]}
        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data).json()
            ai_reply = res['choices'][0]['message']['content']
            self.last_response = ai_reply
            # AI ki formatting (Orange color)
            formatted_reply = f"[color=FFA500]Obito AI:[/color] {ai_reply}\n\n"
            # Kivy mein thread update safe karne ke liye Clock use kiya hai
            Clock.schedule_once(lambda dt: self.update_ui(formatted_reply, enable_btn=True))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_ui("[color=FF0000]Error: Connection failed![/color]\n\n", enable_btn=True))

    def update_ui(self, text, enable_btn=False):
        self.chat_history.text += text
        self.scroll.scroll_y = 0 # Auto-scroll to bottom
        if enable_btn:
            self.send_btn.text = "SEND"
            self.send_btn.disabled = False

if __name__ == '__main__':
    ObitoAI().run()
    
