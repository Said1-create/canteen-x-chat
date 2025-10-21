import streamlit as st
from datetime import datetime
from transformers import pipeline
import torch
import re

# Настройка страницы
st.set_page_config(
    page_title="Canteen-X AI Чат",
    page_icon="🤖",
    layout="centered"
)

class UniversalAIBot:
    def __init__(self):
        self.chatbot = None
        self.conversation_history = []
        self.load_model()
        
        # Контекст Canteen-X для нейросети
        self.canteen_context = """
        Ты Григорий - AI помощник в приложении Canteen-X для заказа еды в столовых.
        
        Информация о Canteen-X:
        - Меню: пицца (350-380 руб), бургеры (280-300 руб), салаты (180-220 руб), паста (310-340 руб), напитки (80-150 руб)
        - Время работы: Пн-Пт 8:00-20:00, Сб-Вс 9:00-18:00
        - Оплата: карты, мобильные платежи, наличные
        - Доставка: бесплатно по кампусу, 100 руб за пределами
        - Типы заказа: "с собой" или "в зале"
        
        Твоя роль: помогать с заказами еды, отвечать на вопросы о меню, но также можешь общаться на любые тепы.
        Будь дружелюбным, используй эмодзи, поддерживай беседу.
        """
    
    def load_model(self):
        """Загружаем модель для свободного общения"""
        try:
            self.chatbot = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",  # Лучше для диалогов
                max_length=1024,  # Больше контекста
                temperature=0.7,  # Баланс креативности
                do_sample=True,
                pad_token_id=50256,
                torch_dtype=torch.float32
            )
        except Exception as e:
            st.error(f"⚠️ AI модель не загрузилась: {e}")
            self.chatbot = None
    
    def get_ai_response(self, user_message):
        """Универсальный AI для любого общения"""
        if not self.chatbot:
            return "🤖 Привет! Спроси о меню или просто поболтаем! 😊"
        
        try:
            # Собираем историю диалога
            history_text = ""
            for i, (user_msg, bot_msg) in enumerate(self.conversation_history[-4:]):  # Последние 4 реплики
                history_text += f"Пользователь: {user_msg}\nГригорий: {bot_msg}\n"
            
            # Создаем умный промпт с историей и контекстом
            prompt = f"""{self.canteen_context}

{history_text}
Пользователь: {user_message}
Григорий:"""
            
            # Генерируем ответ нейросетью
            response = self.chatbot(
                prompt,
                max_new_tokens=150,  # Достаточно для развернутого ответа
                temperature=0.7,
                do_sample=True,
                repetition_penalty=1.1  # Избегаем повторений
            )
            
            # Извлекаем чистый ответ
            full_text = response[0]['generated_text']
            ai_response = full_text.split("Григорий:")[-1].strip()
            
            # Очищаем ответ от лишнего
            ai_response = re.split(r'Пользователь:|Григорий:', ai_response)[0].strip()
            
            # Сохраняем в историю
            self.conversation_history.append((user_message, ai_response))
            
            # Ограничиваем размер истории
            if len(self.conversation_history) > 10:
                self.conversation_history.pop(0)
            
            return ai_response if ai_response else "Интересный вопрос! Расскажи больше? 😊"
            
        except Exception as e:
            return "Привет! 😊 Давай общаться! Спрашивай что угодно или заказывай еду! 🍕"

def main():
    # Инициализация универсального AI
    if 'ai_bot' not in st.session_state:
        with st.spinner("🔄 Загружаем универсальную нейросеть..."):
            st.session_state.ai_bot = UniversalAIBot()
    
    # Инициализация истории чата
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "bot", 
            "content": "Привет! Я Григорий 🤖\nУниверсальная нейросеть готова к общению! Можем:\n• Заказывать еду 🍕\n• Общаться на любые темы 💬\n• Шутить и поддерживать беседу 😄\nЧто хочешь сделать?",
            "time": datetime.now().strftime("%H:%M")
        })
    
    # Заголовок
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Canteen-X 🧠")
        st.subheader("Универсальная нейросеть")
        st.caption("🚀 Общается на любые темы + заказы еды!")
    with col2:
        st.markdown("<div style='text-align: center; font-size: 50px'>🤖</div>", unsafe_allow_html=True)
    
    # Статус
    if st.session_state.ai_bot.chatbot:
        st.success("✅ Универсальный AI активен! Общается на любые темы!")
    else:
        st.warning("⚠️ Базовый режим")
    
    # Область чата
    st.markdown("---")
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style='display: flex; justify-content: flex-end; margin-bottom: 15px;'>
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 16px; border-radius: 18px 18px 0 18px; margin: 8px 0; max-width: 80%;'>
                        {msg["content"]}
                        <div style='font-size: 0.8em; color: rgba(255,255,255,0.8); margin-top: 4px;'>{msg["time"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='display: flex; justify-content: flex-start; margin-bottom: 15px;'>
                    <div style='background: #f1f3f4; color: #333; padding: 12px 16px; border-radius: 18px 18px 18px 0; margin: 8px 0; max-width: 80%;'>
                        {msg["content"]}
                        <div style='font-size: 0.8em; color: #666; margin-top: 4px;'>{msg["time"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Ввод с поддержкой Enter
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input(
            "Напишите сообщение:",
            placeholder="Можете спросить о еде, поболтать, задать любой вопрос...",
            label_visibility="collapsed"
        )
        submit_button = st.form_submit_button(label='Отправить ➤')
    
    # Обработка сообщения
    if submit_button and user_input.strip():
        # Добавляем сообщение пользователя
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "time": datetime.now().strftime("%H:%M")
        })
        
        # Получаем ответ от универсального AI
        with st.spinner("Григорий думает..."):
            ai_response = st.session_state.ai_bot.get_ai_response(user_input)
        
        st.session_state.messages.append({
            "role": "bot", 
            "content": ai_response,
            "time": datetime.now().strftime("%H:%M")
        })
        
        st.rerun()
    
    # Быстрые темы для общения
    st.markdown("**Попробуйте спросить:**")
    cols = st.columns(2)
    topics = [
        ("🍕 Про еду", "Что вкусного посоветуешь?"),
        ("💬 Просто поболтать", "Как твои дела?"),
        ("😊 Про настроение", "Какое у тебя сегодня настроение?"),
        ("🎮 Про хобби", "Что ты любишь делать?"),
        ("🤔 Философское", "В чем смысл жизни?"),
        ("📚 Про учебу", "Как лучше учиться программированию?")
    ]
    
    for i, (btn_text, message) in enumerate(topics):
        with cols[i % 2]:
            if st.button(btn_text, use_container_width=True, key=f"topic_{i}"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": message,
                    "time": datetime.now().strftime("%H:%M")
                })
                
                with st.spinner("Григорий думает..."):
                    ai_response = st.session_state.ai_bot.get_ai_response(message)
                
                st.session_state.messages.append({
                    "role": "bot",
                    "content": ai_response,
                    "time": datetime.now().strftime("%H:%M")
                })
                
                st.rerun()
    
    # Кнопка очистки
    if st.button("🧹 Очистить историю", use_container_width=True):
        st.session_state.messages = []
        st.session_state.ai_bot.conversation_history = []
        st.session_state.messages.append({
            "role": "bot",
            "content": "Чат очищен! Я вся твоя! Спрашивай что угодно или заказывай еду! 🎉",
            "time": datetime.now().strftime("%H:%M")
        })
        st.rerun()

if __name__ == "__main__":
    main()
