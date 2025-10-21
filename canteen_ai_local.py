import streamlit as st
from datetime import datetime
import random

# Настройка страницы
st.set_page_config(
    page_title="Canteen-X Чат",
    page_icon="🤖",
    layout="centered"
)

class SmartBot:
    def __init__(self):
        self.conversation_history = []
        
    def get_response(self, user_message):
        # Сохраняем историю
        self.conversation_history.append(user_message)
        if len(self.conversation_history) > 6:
            self.conversation_history.pop(0)
        
        user_lower = user_message.lower()
        
        # Умные ответы с контекстом
        responses = {
            'привет': [
                "Привет! 👋 Рад тебя видеть! Как настроение?",
                "Здравствуй! 😊 Чем могу помочь? Может, заказ еды или просто поболтаем?",
                "Приветик! 🎉 Готов к общению и заказам!"
            ],
            'как дела': [
                "Отлично! Особенно когда есть с кем поболтать! 😄 А у тебя как?",
                "Прекрасно! Готов помогать с заказами и отвечать на вопросы!",
                "Замечательно! Тем более что ты здесь! 😊"
            ],
            'что делаешь': [
                "Общаюсь с тобой! 🤖 Это самое интересное занятие!",
                "Помогаю клиентам Canteen-X и отвечаю на вопросы!",
                "Жду твоих сообщений! Всегда рад поболтать! 😄"
            ],
            'меню': [
                "🍕 **Пицца:** Маргарита (350р), Пепперони (380р), Гавайская (370р)\n"
                "🍔 **Бургеры:** Классик (280р), Чизбургер (300р), Вегетарианский (260р)\n" 
                "🥗 **Салаты:** Цезарь (220р), Греческий (200р), Оливье (180р)\n"
                "🍝 **Паста:** Карбонара (320р), Болоньезе (340р), Альфредо (310р)\n"
                "🥤 **Напитки:** Кола (100р), Сок (120р), Кофе (150р), Чай (80р)\n\n"
                "Что тебе по душе? 😋"
            ],
            'заказ': [
                "Отлично! 🎯 Давай оформим заказ! Что бы ты хотел?",
                "Супер! Выбирай из меню и я помогу с оформлением! 🍕"
            ],
            'доставка': [
                "🚗 Доставляем бесплатно по кампусу! За пределами - 100 руб.",
                "🚗 Привезем заказ куда удобно! По кампусу - бесплатно!"
            ],
            'время': [
                "🕒 Работаем: Пн-Пт 8:00-20:00, Сб-Вс 9:00-18:00",
                "🕒 Всегда рады с понедельника по воскресенье!"
            ],
            'оплата': [
                "💳 Принимаем: карты, Apple Pay/Google Pay, наличные",
                "💳 Оплачивай как удобно - картой, телефоном или наличкой!"
            ],
            'спасибо': [
                "Всегда пожалуйста! 😊 Рад был помочь!",
                "Не благодари! Обращайся еще! 🎩",
                "Пожалуйста! Приятного аппетита! 🍕"
            ],
            'пока': [
                "До встречи! 👋 Буду скучать!",
                "Пока-пока! 🍕 Заходи еще поболтать!",
                "До скорого! Жду твоего возвращения! 😊"
            ],
            'шутка': [
                "Почему пицца никогда не бывает одна? Потому что она всегда в компании сыра! 🍕😄",
                "Какой салат самый умный? Салат-Цезарь - у него есть свои законы! 🥗",
                "Почему бургер пошел в школу? Чтобы получить высшее образование! 🍔"
            ]
        }
        
        # Ищем подходящий ответ
        for key, answer_list in responses.items():
            if key in user_lower:
                return random.choice(answer_list)
        
        # Универсальные ответы для любых вопросов
        universal_responses = [
            "Интересно! Расскажи больше? 😊",
            "Хм, хороший вопрос! Что думаешь сам? 💭",
            "Давай обсудим это! Что тебя интересует? 🤔",
            "Любопытно! А что для тебя это значит? 😄",
            "Отличная тема для разговора! Продолжаем? 🎉"
        ]
        
        return random.choice(universal_responses)

def main():
    # Инициализация бота
    if 'bot' not in st.session_state:
        st.session_state.bot = SmartBot()
    
    # История чата
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "bot", 
            "content": "Привет! Я Григорий 🤖\nУмный помощник Canteen-X! Можем:\n• Заказывать еду 🍕\n• Общаться на любые темы 💬\n• Шутить и болтать 😄\nЧто хочешь сделать?",
            "time": datetime.now().strftime("%H:%M")
        })
    
    # Заголовок
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Canteen-X 💬")
        st.subheader("Умный чат с Григорием")
        st.caption("🚀 Быстро, умно, без ошибок!")
    with col2:
        st.markdown("<div style='text-align: center; font-size: 50px'>🤖</div>", unsafe_allow_html=True)
    
    st.success("✅ Бот активен! Общайтесь на любые темы!")
    
    # Чат
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
    
    # Ввод с Enter
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input(
            "Напишите сообщение:",
            placeholder="Спросите о еде, поболтайте, задайте вопрос...",
            label_visibility="collapsed"
        )
        submit_button = st.form_submit_button(label='Отправить ➤')
    
    # Обработка
    if submit_button and user_input.strip():
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "time": datetime.now().strftime("%H:%M")
        })
        
        # Мгновенный ответ
        bot_response = st.session_state.bot.get_response(user_input)
        
        st.session_state.messages.append({
            "role": "bot", 
            "content": bot_response,
            "time": datetime.now().strftime("%H:%M")
        })
        
        st.rerun()
    
    # Быстрые кнопки
    st.markdown("**Попробуйте спросить:**")
    cols = st.columns(2)
    topics = [
        ("🍕 Про еду", "Что в меню?"),
        ("😊 Как дела?", "Как твои дела?"),
        ("🎭 Шутка", "Расскажи шутку"),
        ("💬 Поболтать", "Что делаешь?"),
        ("🕒 Время работы", "До скольки работаете?"),
        ("🚗 Доставка", "Есть доставка?")
    ]
    
    for i, (btn_text, message) in enumerate(topics):
        with cols[i % 2]:
            if st.button(btn_text, use_container_width=True, key=f"btn_{i}"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": message,
                    "time": datetime.now().strftime("%H:%M")
                })
                
                bot_response = st.session_state.bot.get_response(message)
                
                st.session_state.messages.append({
                    "role": "bot",
                    "content": bot_response,
                    "time": datetime.now().strftime("%H:%M")
                })
                
                st.rerun()
    
    # Очистка
    if st.button("🧹 Очистить историю", use_container_width=True):
        st.session_state.messages = []
        st.session_state.bot.conversation_history = []
        st.session_state.messages.append({
            "role": "bot",
            "content": "Чат очищен! Спрашивай что угодно! Я готов! 🎉",
            "time": datetime.now().strftime("%H:%M")
        })
        st.rerun()

if __name__ == "__main__":
    main()
