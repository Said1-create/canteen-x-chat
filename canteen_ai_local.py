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

# Инициализация состояния темы ДО всех функций
if 'dark_theme' not in st.session_state:
    st.session_state.dark_theme = False

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
            'меню': "📋 **Внимание!** Функция просмотра меню временно недоступна. Мы работаем над обновлением ассортимента!",
            'заказ': "🛒 **Внимание!** Система заказов находится в разработке. Скоро вы сможете оформлять заказы онлайн!",
            'доставка': "🚚 **Внимание!** Информация о доставке временно недоступна. Мы обновляем зоны доставки!",
            'время': "⏰ **Внимание!** Информация о времени работы временно недоступна. Ведутся технические работы!",
            'оплата': "💳 **Внимание!** Информация о способах оплаты обновляется. Скоро будут доступны новые варианты!",
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
                return "🛒 **Внимание!** Система заказов находится в разработке. Скоро вы сможете оформлять заказы онлайн!"
        
        # Ищем подходящий ответ
        for key, answer_list in responses.items():
            if key in user_lower:
                if isinstance(answer_list, list):
                    return random.choice(answer_list)
                else:
                    return answer_list
        
        # Ответы на вопросы о еде
        food_keywords = {
            'пицц': "🍕 Пицца у нас свежая, готовится 15 минут! Но меню временно обновляется!",
            'бургер': "🍔 Бургеры сочные с домашней булочкой! Ассортимент скоро будет доступен!",
            'салат': "🥗 Салаты свежие, заправляем перед подачей! Обновляем рецепты!",
            'паст': "🍝 Паста с домашним соусом! Скоро вернемся с новыми вариантами!",
            'напитк': "🥤 Напитки охлажденные! Ассортимент временно ограничен!"
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

def setup_theme():
    """Настраивает тему приложения"""
    
    # CSS для темной темы
    if st.session_state.dark_theme:
        st.markdown("""
        <style>
        /* Основной фон */
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        
        /* Заголовки */
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
        
        /* Текст */
        p, div, span {
            color: white !important;
        }
        
        /* Уведомления */
        .stSuccess {
            background-color: #1A472A !important;
            color: white !important;
            border: 1px solid #2E8B57 !important;
        }
        
        .stInfo {
            background-color: #1E3A5F !important;
            color: white !important;
            border: 1px solid #3B82F6 !important;
        }
        
        /* Кнопки */
        .stButton button {
            background-color: #374151 !important;
            color: white !important;
            border: 1px solid #4B5563 !important;
        }
        
        .stButton button:hover {
            background-color: #4B5563 !important;
            border-color: #6B7280 !important;
        }
        
        /* Поле ввода - ИСПРАВЛЕНО */
        .stTextInput input {
            background-color: #1F2937 !important;
            color: white !important;
            border: 1px solid #374151 !important;
        }
        
        .stTextInput input::placeholder {
            color: #9CA3AF !important;
        }
        
        .stTextInput input:focus {
            border-color: #60A5FA !important;
        }
        
        /* Кнопка отправки - ИСПРАВЛЕНО */
        .stFormSubmitButton button {
            background-color: #2563EB !important;
            color: white !important;
            border: 1px solid #3B82F6 !important;
        }
        
        .stFormSubmitButton button:hover {
            background-color: #1D4ED8 !important;
            border-color: #2563EB !important;
        }
        
        /* Сообщения пользователя */
        .user-message-dark {
            background: linear-gradient(135deg, #4A5568 0%, #2D3748 100%) !important;
            color: white !important;
            border: 1px solid #4A5568 !important;
        }
        
        /* Сообщения бота */
        .bot-message-dark {
            background: #374151 !important;
            color: white !important;
            border: 1px solid #4B5563 !important;
        }
        
        /* Время сообщений */
        .message-time-dark {
            color: #9CA3AF !important;
        }
        
        /* Подписи */
        .stCaption {
            color: #CCCCCC !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Светлая тема (сбрасываем стили)
        st.markdown("""
        <style>
        .stApp {
            background-color: white;
        }
        .stFormSubmitButton button {
            background-color: #1E40AF !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)

def create_theme_toggle():
    """Создает кнопку переключения темы и справки"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col4:
        # Кнопка справки
        if st.button("❓", key="help_toggle", help="Информация о приложении"):
            st.session_state.show_help = True
            
    with col5:
        # Кнопка переключения темы
        theme_icon = "🌙" if not st.session_state.dark_theme else "☀️"
        if st.button(theme_icon, key="theme_toggle", help="Переключить тему"):
            st.session_state.dark_theme = not st.session_state.dark_theme
            st.rerun()

def show_help_modal():
    """Показывает модальное окно с информацией о приложении"""
    if st.session_state.get('show_help', False):
        st.markdown("""
        <style>
        .help-modal {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 10000;
            border: 2px solid #3B82F6;
            max-width: 400px;
            width: 90%;
        }
        .help-modal.dark {
            background: #1F2937;
            color: white;
        }
        .help-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: 9999;
        }
        .close-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: #6B7280;
        }
        </style>
        """, unsafe_allow_html=True)
        
        modal_class = "help-modal dark" if st.session_state.dark_theme else "help-modal"
        
        st.markdown(f"""
        <div class="help-overlay" onclick="document.getElementById('help-modal').style.display='none'">
            <div class="{modal_class}" id="help-modal">
                <button class="close-btn" onclick="this.parentElement.parentElement.style.display='none'">×</button>
                <h3>🤖 О чат-боте</h3>
                <p><strong>Версия:</strong> Alpha 1.0</strong></p>
                <p>Это тестовая версия чат-бота Canteen-X. Некоторые функции могут быть временно недоступны или работать некорректно.</p>
                <p><strong>Следите за обновлениями:</strong></p>
                <p>📢 Наш Telegram: <em><a href="https://t.me/CanteenX1" target="_blank">Перейти в канал</a></em></p>
                <small>Приносим извинения за временные неудобства! 🛠️</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Сбрасываем флаг показа помощи после отображения
        if st.button("Закрыть", key="close_help"):
            st.session_state.show_help = False
            st.rerun()

def main():
    # Инициализация состояния помощи
    if 'show_help' not in st.session_state:
        st.session_state.show_help = False
    
    # Создаем переключатель темы и справки
    create_theme_toggle()
    
    # Показываем модальное окно помощи если нужно
    show_help_modal()
    
    # Применяем выбранную тему
    setup_theme()
    
    # Инициализация бота
    if 'bot' not in st.session_state:
        st.session_state.bot = SmartBot()
    
    # История чата
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "bot", 
            "content": "Привет! Я Григорий 🤖\nУмный помощник Canteen-X! Можем:\n• Общаться на любые темы 💬\n• Шутить и болтать 😄\n• Рассказать о текущем статусе сервиса 🛠️\n\n⚠️ <strong>Внимание:</strong> Некоторые функции временно недоступны - мы работаем над улучшением сервиса!",
            "time": datetime.now().strftime("%H:%M")
        })
    
    # Заголовок
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Canteen-X 💬")
        st.subheader("Умный чат с Григорием")
        st.caption("🚀 Альфа-версия • Некоторые функции временно недоступны")
    with col2:
        st.markdown("<div style='text-align: center; font-size: 50px'>🤖</div>", unsafe_allow_html=True)
    
    st.success("✅ Бот активен! Общайтесь на любые темы!")
    
    # Чат
    st.markdown("---")
    
    # Контейнер чата
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            is_dark = st.session_state.dark_theme
            
            if msg["role"] == "user":
                message_class = "user-message-dark" if is_dark else ""
                st.markdown(f"""
                <div style='display: flex; justify-content: flex-end; margin: 10px 0;'>
                    <div class='{message_class}' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 16px; border-radius: 18px 18px 0 18px; max-width: 70%; word-wrap: break-word;'>
                        {msg["content"]}
                        <div style='font-size: 0.7em; color: rgba(255,255,255,0.8); margin-top: 5px; text-align: right;'>{msg["time"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                message_class = "bot-message-dark" if is_dark else ""
                time_class = "message-time-dark" if is_dark else ""
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

if __name__ == "__main__":
    main()
