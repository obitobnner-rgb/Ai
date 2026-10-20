import flet as ft
import requests

# Yahan apni OpenRouter API key aur Uncensored Model ka naam dalein
API_KEY = "aapki_openrouter_api_key_yahan_dalein" 
MODEL = "cognitivecomputations/dolphin-mixtral-8x7b" 

def main(page: ft.Page):
    page.title = "My Uncensored AI"
    page.theme_mode = "dark"
    
    chat_history = ft.Column(scroll="always", expand=True)
    user_input = ft.TextField(hint_text="Ask anything...", expand=True)

    def send_message(e):
        user_text = user_input.value
        chat_history.controls.append(ft.Text(f"You: {user_text}", color="white"))
        user_input.value = ""
        page.update()

        # Uncensored AI ko message bhejna
        headers = {"Authorization": f"Bearer {API_KEY}"}
        data = {
            "model": MODEL,
            "messages": [{"role": "user", "content": user_text}]
        }
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data).json()
        ai_reply = response['choices'][0]['message']['content']
        
        chat_history.controls.append(ft.Text(f"My AI: {ai_reply}", color="blue"))
        page.update()

    send_btn = ft.ElevatedButton("Send", on_click=send_message)
    page.add(chat_history, ft.Row([user_input, send_btn]))

ft.app(target=main)
