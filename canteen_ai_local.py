import streamlit as st
from datetime import datetime
import random
from transformers import pipeline, set_seed
import warnings
warnings.filterwarnings('ignore')

# Настройка страницы
st.set_page_config(
    page_title="Canteen-X AI Чат",
    page_icon="🤖",
    layout="centered"
)

class ImprovedCanteenAI:
    def __init__(self):
        self.chatbot = None
        self.load_model()
        
        # Улучшенная база знаний
        self.canteen_info = {
            "меню": {
                "пицца": ["🍕 Маргарита - 350 руб", "🍕 Пепперони - 380 руб", "🍕 Гавайская - 370 руб"],
                "бургеры": ["🍔 Классик - 280 руб", "🍔 Чизбургер - 300 руб", "🍔 Вегетарианский - 260 руб"],
                "салаты": ["🥗 Цезарь - 220 руб", "🥗 Греческий - 200 руб", "🥗 Оливье - 180 руб"],
                "паста": ["🍝 Карбонара - 320 руб", "🍝 Болоньезе - 340 руб", "🍝 Альфредо - 310 руб"],
                "напитки": ["🥤 Кола - 100 руб", "🥤 Сок - 120 руб", "☕ Кофе - 150 руб", "🍵 Чай - 80 руб"]
            },
            "время": "🕒 Пн-Пт: 8:00-20:00, Сб-Вс: 9:00-18:00",
            "оплата": "💳 Карты (Visa/Mastercard), мобильные платежи, наличные",
            "доставка": "🚗 Бесплатно по кампусу, 100 руб за пределами",
            "тип заказа": ["📦 с собой", "🍽️ в зале"]
        }
    
    def load_model(self):
        """Загружаем улучшенную модель"""
        try:
            self.chatbot = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",  # Улучшенная модель
                max_length=200,
                temperature=0.8,  # Более креативные ответы
                do_sample=True,
                pad_token_id=50256
            )
            set_seed(42)  # Для более стабильных ответов
        except Exception as e:
            st.error(f"⚠️ Базовая версия AI: {e}")
            self.chatbot = None
    
    def get_ai_response(self, user_message):
        """Улучшенный AI с лучшим контекстом"""
        lower_message = user_message.lower()
        
        # Умные ответы на частые вопросы
        smart_responses = {
            'привет': ["Привет! 👋 Рад тебя видеть! Как я могу помочь с заказом?", 
                      "Здравствуй! 😊 Готов помочь выбрать вкусный обед!"],
            'меню': [self.get_menu_response()],
            'как дела': ["Отлично! 🎉 Готов помогать с заказами еды! А у тебя как настроение?",
                        "Прекрасно! Тем более когда могу помочь с выбором вкусной еды! 🍕"],
            'что посоветуешь': ["Рекомендую пиццу Пепперони! 🍕 Она очень популярна! Или может салат Цезарь? 🥗",
                               "Попробуй наш бургер Классик! 🍔 Все от него в восторге!"],
            'спасибо': ["Всегда пожалуйста! 😊 Приятного аппетита!",
                       "Рад был помочь! 🎩 Жду твоего следующего заказа!"],
            'пока': ["До встречи! 👋 Жду твоего возвращения!",
                    "Пока-пока! 🍕 Не забывай заходить за вкусной едой!"]
        }
        
        # Проверяем умные ответы
        for key, responses in smart_responses.items():
            if key in lower_message:
                return random.choice(responses)
        
        # Проверяем информацию о кафе
        if any(word in lower_message for word in ['меню', 'еда', 'блюд', 'кухн', 'заказ']):
            return self.get_menu_response()
        elif any(word in lower_message for word in ['время', 'работа', 'открыт', 'закрыт']):
            return f"🕒 {self.canteen_info['время']}"
        elif any(word in lower_message for word in ['оплат', 'карт', 'деньг', 'цена']):
            return f"💳 {self.canteen_info['оплата']}"
        elif any(word in lower_message for word in ['доставк', 'привез', 'забер']):
            return f"🚗 {self.canteen_info['доставка']}"
        
        # Используем AI для остальных вопросов
        if self.chatbot:
            try:
                # Улучшенный промпт с контекстом
                prompt = f"""Ты Григорий - дружелюбный и веселый помощник в столовой Canteen-X. 
Отвечай кратко, дружелюбно, используй эмодзи. Будь общительным!

Пользователь: {user_message}
Григорий:"""
                
                response = self.chatbot(
                    prompt,
                    max_new_tokens=100,
                    temperature=0.8,
                    do_sample=True
                )
                
                ai_text = response[0]['generated_text']
                clean_response = ai_text.split("Григорий:")[-1].strip()
                
                # Убедимся что ответ не пустой
                if clean_response and len(clean_response) > 5:
                    return clean_response
                else:
                    return "Расскажи, что тебя интересует? Может, меню или заказ? 😊"
                
            except Exception as e:
                return "Привет! 😊 Чем могу помочь с заказом еды?"
        
        # Запасной ответ
        return "Привет! Я Григорий 🤖 Помогу с заказом еды! Спроси о меню или времени работы! 🍕"
    
    def get_menu_response(self):
        """Красивое меню"""
        menu_text = "🍽️ **Наше вкусное меню:**\n\n"
        for category, items in self.canteen_info["меню"].items():
            menu_text += f"**{category.upper()}:**\n"
            for item in items:
                menu_text += f"  {item}\n"
            menu_text += "\n"
        menu_text += "Что тебе по душе? Могу помочь выбрать! 😋"
        return menu_text

def main():
    # Инициализация улучшенного AI
    if 'ai_bot' not in st.session_state:
        with st.spinner("🔄 Загружаем умного Григория..."):
            st.session_state.ai_bot = ImprovedCanteenAI()
    
    # Инициализация истории чата
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "bot", 
            "content": "Привет! Я Григорий 🤖\nТвой веселый помощник в Canteen-X! Готов помочь с заказом, рассказать о меню или просто поболтать! 😊",
            "time": datetime.now().strftime("%H:%M")
        })
    
    # Заголовок
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Canteen-X 🍕")
        st.subheader("Умный чат с Григорием")
        st.caption("🚀 Теперь с улучшенным AI!")
    with col2:
        st.markdown("<div style='text-align: center; font-size: 50px'>🤖</div>", unsafe_allow_html=True)
    
    # Статус
    if st.session_state.ai_bot.chatbot:
        st.success("✅ Умный AI активен! Григорий готов к общению!")
    else:
        st.warning("⚠️ Работает в базовом режиме")
    
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
    
    # Улучшенный ввод сообщения с поддержкой Enter
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input(
            "Введите сообщение:",
            placeholder="Напишите что-нибудь... (нажмите Enter для отправки)",
            label_visibility="collapsed"
        )
        submit_button = st.form_submit_button(label='Отправить ➤')
    
    # Обработка отправки по Enter или кнопке
    if submit_button and user_input.strip():
        # Добавляем сообщение пользователя
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "time": datetime.now().strftime("%H:%M")
        })
        
        # Получаем AI ответ
        with st.spinner("Григорий думает..."):
            ai_response = st.session_state.ai_bot.get_ai_response(user_input)
        
        st.session_state.messages.append({
            "role": "bot", 
            "content": ai_response,
            "time": datetime.now().strftime("%H:%M")
        })
        
        st.rerun()
    
    # Быстрые кнопки
    st.markdown("**Быстрые вопросы:**")
    cols = st.columns(3)
    quick_actions = [
        ("📋 Что в меню?", "Что в меню?"),
        ("🕒 До скольки работаете?", "До скольки работаете?"),
        ("💸 Как оплатить?", "Как оплатить заказ?"),
        ("🚗 Есть доставка?", "Есть доставка?"),
        ("😊 Как дела?", "Как дела?"),
        ("🍕 Что посоветуешь?", "Что посоветуешь?")
    ]
    
    for i, (btn_text, message) in enumerate(quick_actions):
        with cols[i % 3]:
            if st.button(btn_text, use_container_width=True, key=f"quick_{i}"):
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
        st.session_state.messages.append({
            "role": "bot",
            "content": "Чат очищен! Спрашивай что угодно! 😊",
            "time": datetime.now().strftime("%H:%M")
        })
        st.rerun()

if __name__ == "__main__":
    main()
