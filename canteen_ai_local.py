import streamlit as st
from datetime import datetime
import random
from transformers import pipeline
import warnings

warnings.filterwarnings('ignore')

# Настройка страницы
st.set_page_config(
    page_title="Canteen-X Local AI",
    page_icon="🤖",
    layout="centered"
)


class LocalCanteenAI:
    def __init__(self):
        self.chatbot = None
        self.load_model()

        # База знаний о Canteen-X
        self.canteen_info = {
            "меню": {
                "пицца": ["Маргарита - 350 руб", "Пепперони - 380 руб", "Гавайская - 370 руб"],
                "бургеры": ["Классик - 280 руб", "Чизбургер - 300 руб", "Вегетарианский - 260 руб"],
                "салаты": ["Цезарь - 220 руб", "Греческий - 200 руб", "Оливье - 180 руб"],
                "паста": ["Карбонара - 320 руб", "Болоньезе - 340 руб", "Альфредо - 310 руб"],
                "напитки": ["Кола - 100 руб", "Сок - 120 руб", "Кофе - 150 руб", "Чай - 80 руб"]
            },
            "время": "Пн-Пт: 8:00-20:00, Сб-Вс: 9:00-18:00",
            "оплата": "Карты (Visa/Mastercard), мобильные платежи, наличные",
            "доставка": "Бесплатно по кампусу, 100 руб за пределами",
            "тип заказа": ["с собой", "в зале"]
        }

    def load_model(self):
        """Загружаем легкую модель для чата"""
        try:
            # Используем легкую модель для быстрой работы
            self.chatbot = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-small",
                tokenizer="microsoft/DialoGPT-small",
                torch_dtype='auto'
            )
            st.success("✅ AI модель загружена!")
        except Exception as e:
            st.error(f"❌ Ошибка загрузки модели: {e}")
            self.chatbot = None

    def get_ai_response(self, user_message):
        """Получаем ответ от AI с контекстом Canteen-X"""

        # Сначала проверяем ключевые слова для точных ответов
        lower_message = user_message.lower()

        # Ответы на конкретные вопросы о Canteen-X
        if any(word in lower_message for word in ['меню', 'еда', 'блюд', 'кухн']):
            return self.get_menu_response()

        elif any(word in lower_message for word in ['время', 'работа', 'открыт']):
            return f"🕒 {self.canteen_info['время']}"

        elif any(word in lower_message for word in ['оплат', 'карт', 'деньг']):
            return f"💳 {self.canteen_info['оплата']}"

        elif any(word in lower_message for word in ['доставк', 'привез']):
            return f"🚗 {self.canteen_info['доставка']}"

        elif any(word in lower_message for word in ['заказ', 'заказыв']):
            return "🎯 Отлично! Для заказа:\n1. Выберите блюдо из меню\n2. Укажите тип заказа: 'с собой' или 'в зале'\n3. Подтвердите заказ"

        elif any(word in lower_message for word in ['с собой', 'навынос']):
            return "📦 Заказ 'с собой' будет аккуратно упакован. Что бы вы хотели?"

        elif any(word in lower_message for word in ['в зале', 'на месте']):
            return "🍽️ Заказ 'в зале' - столик будет ждать вас. Какое блюдо?"

        # Если нет ключевых слов, используем AI
        elif self.chatbot:
            try:
                # Добавляем контекст о роли бота
                prompt = f"Ты Григорий - помощник в столовой Canteen-X. Отвечай кратко и полезно. Вопрос: {user_message}"

                response = self.chatbot(
                    prompt,
                    max_length=150,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=50256
                )

                ai_text = response[0]['generated_text']
                # Убираем промпт из ответа
                clean_response = ai_text.replace(prompt, "").strip()
                return clean_response if clean_response else "Расскажите, чем могу помочь с заказом еды?"

            except Exception as e:
                return f"🤖 Спросите о нашем меню, времени работы или как сделать заказ!"

        else:
            return "Привет! Я Григорий 🤖 Помогу с заказом еды в Canteen-X. Спросите о меню или времени работы!"

    def get_menu_response(self):
        """Генерируем красивый ответ с меню"""
        menu_text = "🍽️ **Наше меню:**\n\n"
        for category, items in self.canteen_info["меню"].items():
            menu_text += f"**{category.title()}:**\n"
            for item in items:
                menu_text += f"• {item}\n"
            menu_text += "\n"
        menu_text += "Что вас интересует?"
        return menu_text


def main():
    # Инициализация AI
    if 'ai_bot' not in st.session_state:
        with st.spinner("🔄 Загружаем AI модель... Это может занять минуту"):
            st.session_state.ai_bot = LocalCanteenAI()

    # Инициализация истории чата
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "bot",
            "content": "Привет! Я Григорий 🤖\nВаш локальный AI-помощник в Canteen-X. Спросите меня о меню, заказе или времени работы!",
            "time": datetime.now().strftime("%H:%M")
        })

    # Заголовок
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Canteen-X 🍕")
        st.subheader("Локальный AI Чат с Григорием")
        st.caption("🚀 Работает полностью оффлайн!")

    with col2:
        st.markdown("<div style='text-align: center; font-size: 50px'>🧠</div>", unsafe_allow_html=True)

    # Индикатор статуса AI
    if st.session_state.ai_bot.chatbot:
        st.success("✅ AI активен и готов к общению!")
    else:
        st.warning("⚠️ AI в базовом режиме (только ключевые слова)")

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

    # Ввод сообщения
    col1, col2 = st.columns([4, 1])

    with col1:
        user_input = st.text_input(
            "Введите ваш вопрос:",
            placeholder="Спросите о меню, заказе, времени работы...",
            label_visibility="collapsed"
        )

    with col2:
        send_clicked = st.button("Отправить", use_container_width=True)

    # Быстрые кнопки
    st.markdown("**Быстрые вопросы:**")
    quick_questions = [
        "Что в меню?",
        "До скольки работаете?",
        "Как оплатить заказ?",
        "Есть доставка?",
        "Хочу заказать еду"
    ]

    cols = st.columns(len(quick_questions))
    for i, question in enumerate(quick_questions):
        with cols[i]:
            if st.button(question, key=f"btn_{i}", use_container_width=True):
                user_input = question
                send_clicked = True

    # Обработка отправки сообщения
    if user_input and send_clicked:
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

    # Кнопка очистки чата
    if st.button("🧹 Очистить историю чата"):
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "bot",
            "content": "Чат очищен! Чем могу помочь?",
            "time": datetime.now().strftime("%H:%M")
        })
        st.rerun()

    # Информация о системе
    st.markdown("---")
    with st.expander("ℹ️ О системе"):
        st.write("""
        **Технологии:**
        - 🤖 Локальный AI: DialoGPT-small
        - 🚀 Библиотека: Transformers от Hugging Face
        - 💾 Работает полностью оффлайн
        - ⚡ Быстрые ответы на русском языке

        **Что умеет Григорий:**
        - Помогать с заказами еды
        - Рассказывать о меню и ценах
        - Отвечать о времени работы и оплате
        - Объяснять про доставку
        - Отвечать на общие вопросы
        """)


if __name__ == "__main__":
    main()