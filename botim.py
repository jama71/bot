import telebot
import g4f
import deepai

# 1. API kalitlarini o‘rnatish
deepai.api_key = "3f23f872-c41a-4273-9ae0-cd20a5eeb64a"  # DeepAI API kalitingizni qo‘ying

# 2. Telegram bot tokeni
TOKEN = "7638833930:AAHpV_HwcDvG65S7lwLVGBl3uo0nk_MuqE8"
bot = telebot.TeleBot(TOKEN)

# 3. GPT-4 orqali muloqot (g4f)
def ask_gpt4(prompt):
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": prompt}]
        )
        return response
    except Exception as e:
        print(e)
        return "❌ AI bilan bog‘lanishda xatolik yuz berdi."

@bot.message_handler(func=lambda message: not message.text.startswith("/"))
def chat_with_ai(message):
    reply = ask_gpt4(message.text)
    bot.send_message(message.chat.id, reply)

# 4. Rasm generatsiyasi (DeepAI text2img)
@bot.message_handler(commands=['image'])
def generate_image(message):
    prompt = message.text.replace("/image", "").strip()
    if not prompt:
        bot.send_message(message.chat.id, "❌ Iltimos, rasm yaratish uchun so‘rov yuboring!")
        return
    try:
        response = deepai.call("text2img", {"text": prompt})
        image_url = response.get("output_url")

        if image_url:
            bot.send_photo(message.chat.id, image_url)
        else:
            bot.send_message(message.chat.id, "❌ Rasm yaratilishda xatolik yuz berdi.")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "❌ Rasm generatsiyasida xatolik yuz berdi.")

# 5. Botni ishga tushirish
print("🤖 Bot ishga tushdi...")
bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
