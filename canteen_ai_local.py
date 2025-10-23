import streamlit as st
from datetime import datetime
import random
import time

# Настройка страницы
st.set_page_config(
    page_title="Canteen-X Чат",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

class SmartBot:
    def __init__(self):
        self.conversation_history = []
        
    def get_response(self, user_message):
        # Сохраняем историю
        self.conversation_history.append({"role": "user", "content": user_message})
        if len(self.conversation_history) > 10:
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
                "**🍕 ПИЦЦА**\n"
                "• Маргарита - 350₽\n" 
                "• Пепперони - 380₽\n"
                "• Гавайская - 370₽\n\n"
                
                "**🍔 БУРГЕРЫ**\n"
                "• Классик - 280₽\n"
                "• Чизбургер - 300₽\n" 
                "• Вегетарианский - 260₽\n\n"
                
                "**🥗 САЛАТЫ**\n"
                "• Цезарь - 220₽\n"
                "• Греческий - 200₽\n"
                "• Оливье - 180₽\n\n"
                
                "**🍝 ПАСТА**\n"
                "• Карбонара - 320₽\n"
                "• Болоньезе - 340₽\n"
                "• Альфредо - 310₽\n\n"
                
                "**🥤 НАПИТКИ**\n"
                "• Кола - 100₽\n"
                "• Сок - 120₽\n"
                "• Кофе - 150₽\n"
                "• Чай - 80₽\n\n"
                "Что тебе по душе? 😋"
            ],
            'заказ': [
                "Отлично! 🎯 Давай оформим заказ! Что бы ты хотел? Просто напиши названия блюд через запятую.",
                "Супер! Выбирай из меню и я помогу с оформлением! 🍕 Напиши что хочешь заказать.",
                "Готов принять заказ! ✍️ Перечисли блюда которые хочешь, и я всё оформлю!"
            ],
            'доставка': [
                "🚗 Доставляем бесплатно по кампусу! За пределами - 100 руб.",
                "🚗 Привезем заказ куда удобно! По кампусу - бесплатно!",
                "🚗 Доставка: бесплатно в кампусе, 100₽ за его пределами!"
            ],
            'время': [
                "🕒 Работаем: Пн-Пт 8:00-20:00, Сб-Вс 9:00-18:00",
                "🕒 Всегда рады с понедельника по воскресенье! Пн-Пт до 20:00, выходные до 18:00",
                "🕒 График: Пн-Пт 8:00-20:00, Сб-Вс 9:00-18:00"
            ],
            'оплата': [
                "💳 Принимаем: карты, Apple Pay/Google Pay, наличные",
                "💳 Оплачивай как удобно - картой, телефоном или наличкой!",
                "💳 Методы оплаты: карты, мобильные платежи, наличные"
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
        
        # Обработка заказа еды
        if any(word in user_lower for word in ['хочу', 'закажи', 'заказать', 'мне бы']):
            if any(food in user_lower for food in ['пицц', 'бургер', 'салат', 'паст', 'напитк']):
                return "Отлично! 🎯 Принял ваш заказ! Ожидайте подтверждения в течение 5 минут. Хотите что-то еще?"
        
        # Ищем подходящий ответ
        for key, answer_list in responses.items():
            if key in user_lower:
                return random.choice(answer_list)
        
        # Ответы на вопросы о еде
        food_keywords = {
            'пицц': "Пицца у нас свежая, готовится 15 минут! 🍕 Рекомендую Пепперони - самый популярный!",
            'бургер': "Бургеры сочные с домашней булочкой! 🍔 Чизбургер просто объедение!",
            'салат': "Салаты свежие, заправляем перед подачей! 🥗 Цезарь - бестселлер!",
            'паст': "Паста с домашним соусом! 🍝 Карбонара - кремовая и нежная!",
            'напитк': "Напитки охлажденные! 🥤 Кофе свежеобжаренный!"
        }
        
        for keyword, response in food_keywords.items():
            if keyword in user_lower:
                return response
        
        # Универсальные ответы для любых вопросов
        universal_responses = [
            "Интересно! Расскажи больше? 😊",
            "Хм, хороший вопрос! Что думаешь сам? 💭",
            "Давай обсудим это! Что тебя интересует? 🤔",
            "Любопытно! А что для тебя это значит? 😄",
            "Отличная тема для разговора! Продолжаем? 🎉",
            "Я пока учусь понимать такие вопросы! Может, спросишь о еде или меню? 🍕"
        ]
        
        return random.choice(universal_responses)

# ===== КОД ДЛЯ ПЕРЕКЛЮЧАТЕЛЯ ТЕМЫ =====
def setup_theme_toggle():
    """Добавляет переключатель темы в правый верхний угол"""
    
    # CSS для темной темы и переключателя
    st.markdown("""
    <style>
    /* Стили для переключателя темы */
    .theme-toggle {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 9999;
    }
    
    .theme-toggle button {
        background: rgba(255,255,255,0.9);
        border: 1px solid #e5e7eb;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .theme-toggle button:hover {
        background: rgba(255,255,255,1);
        transform: scale(1.1);
    }
    
    /* Темная тема */
    .dark-theme {
        background-color: #0E1117;
        color: white;
    }
    
    .dark-theme .stApp {
        background-color: #0E1117;
    }
    
    .dark-theme .stMarkdown {
        color: white !important;
    }
    
    .dark-theme .stTitle {
        color: white !important;
    }
    
    .dark-theme .stSubheader {
        color: white !important;
    }
    
    .dark-theme .stCaption {
        color: #CCCCCC !important;
    }
    
    .dark-theme .stSuccess {
        background-color: #1A472A !important;
        color: white !important;
        border: 1px solid #2E8B57 !important;
    }
    
    .dark-theme .stInfo {
        background-color: #1E3A5F !important;
        color: white !important;
        border: 1px solid #3B82F6 !important;
    }
    
    .dark-theme .stButton button {
        background-color: #374151 !important;
        color: white !important;
        border: 1px solid #4B5563 !important;
    }
    
    .dark-theme .stButton button:hover {
        background-color: #4B5563 !important;
        border-color: #6B7280 !important;
    }
    
    .dark-theme .stTextInput input {
        background-color: #1F2937 !important;
        color: white !important;
        border: 1px solid #374151 !important;
    }
    
    .dark-theme .stTextInput input:focus {
        border-color: #60A5FA !important;
    }
    
    /* Стили для сообщений чата в темной теме */
    .dark-theme .user-message {
        background: linear-gradient(135deg, #4A5568 0%, #2D3748 100%) !important;
        color: white !important;
        border: 1px solid #4A5568 !important;
    }
    
    .dark-theme .bot-message {
        background: #374151 !important;
        color: white !important;
        border: 1px solid #4B5563 !important;
    }
    
    .dark-theme .bot-message-time {
        color: #9CA3AF !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Переключатель темы
    with st.container():
        st.markdown('<div class="theme-toggle">', unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col5:
            # Инициализация состояния темы
            if 'dark_theme' not in st.session_state:
                st.session_state.dark_theme = False
            
            # Кнопка переключения темы
            theme_icon = "🌙" if not st.session_state.dark_theme else "☀️"
            
            if st.button(f"{theme_icon}", key="theme_toggle", help="Переключить тему"):
                st.session_state.dark_theme = not st.session_state.dark_theme
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Применение выбранной темы
    if st.session_state.dark_theme:
        st.markdown('<div class="dark-theme">', unsafe_allow_html=True)
        return True
    return False

def apply_chat_styles(is_dark_theme):
    """Обновляет стили сообщений в зависимости от темы"""
    if is_dark_theme:
        # Обновляем стили для темной темы
        st.markdown("""
        <style>
        /* Переопределяем стили сообщений для темной темы */
        div[data-testid="stMarkdownContainer"] {
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)

def main():
    # Настройка темы
    is_dark_theme = setup_theme_toggle()
    
    # Инициализация бота
    if 'bot' not in st.session_state:
        st.session_state.bot = SmartBot()
    
    # Применение стилей чата
    apply_chat_styles(is_dark_theme)
    
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
    
    # Контейнер чата
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            message_class = "user-message" if is_dark_theme and msg["role"] == "user" else ""
            message_class = "bot-message" if is_dark_theme and msg["role"] == "bot" else message_class
            time_class = "bot-message-time" if is_dark_theme and msg["role"] == "bot" else ""
            
            if msg["role"] == "user":
                st.markdown(f"""
                <div style='display: flex; justify-content: flex-end; margin: 10px 0;'>
                    <div class='{message_class}' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 16px; border-radius: 18px 18px 0 18px; max-width: 70%; word-wrap: break-word;'>
                        {msg["content"]}
                        <div style='font-size: 0.7em; color: rgba(255,255,255,0.8); margin-top: 5px; text-align: right;'>{msg["time"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='display: flex; justify-content: flex-start; margin: 10px 0;'>
                    <div class='{message_class}' style='background: #f0f2f6; color: #1f2937; padding: 12px 16px; border-radius: 18px 18px 18px 0; max-width: 70%; word-wrap: break-word; border: 1px solid #e5e7eb;'>
                        {msg["content"].replace('\n', '<br>')}
                        <div class='{time_class}' style='font-size: 0.7em; color: #6b7280; margin-top: 5px;'>{msg["time"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Ввод сообщения
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input(
            "Напишите сообщение:",
            placeholder="Спросите о еде, поболтайте, задайте вопрос...",
            label_visibility="collapsed",
            key="user_input"
        )
        col1, col2 = st.columns([3, 1])
        with col2:
            submit_button = st.form_submit_button(label='Отправить ➤', use_container_width=True)
    
    # Обработка отправки сообщения
    if submit_button and user_input.strip():
        # Добавляем сообщение пользователя
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "time": datetime.now().strftime("%H:%M")
        })
        
        # Получаем ответ бота
        bot_response = st.session_state.bot.get_response(user_input)
        
        # Добавляем ответ бота
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
        ("🍕 Меню", "меню"),
        ("😊 Как дела?", "как дела"),
        ("🎭 Шутка", "шутка"),
        ("💬 Поболтать", "что делаешь"),
        ("🕒 Время работы", "время работы"),
        ("🚗 Доставка", "доставка"),
        ("💳 Оплата", "оплата"),
        ("📦 Заказать", "хочу заказать пиццу")
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
    
    # Статус и управление
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧹 Очистить историю", use_container_width=True):
            st.session_state.messages = []
            st.session_state.bot.conversation_history = []
            st.session_state.messages.append({
                "role": "bot",
                "content": "Чат очищен! Спрашивай что угодно! Я готов! 🎉",
                "time": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    with col2:
        st.info(f"💬 Сообщений: {len(st.session_state.messages)}")
    
    # Закрываем div темной темы если она активна
    if is_dark_theme:
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
