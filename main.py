import telebot
import requests

# التوكن وآيدي الأدمن هتضاف من Render (Environment Variables)
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(m):
    bot.reply_to(m, """
🔥 أهلاً بك في بوت التحميل السريع!

ارسل أي رابط فيديو من:
• تيك توك
• إنستغرام ريلز
• فيسبوك ريلز
• يوتيوب شورتس
• تويتر / X
• سناب شات (عام)

وأحملّه لك فورًا بدون علامة مائية! 🚀
    """)

@bot.message_handler(func=lambda m: True)
def download(m):
    url = m.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(m, "⚠️ ارسل رابط صحيح من فضلك!")
        return

    msg = bot.reply_to(m, "⏳ جاري التحميل… انتظر ثواني")

    try:
        api = requests.get(f"https://api.savetube.me/download?url={url}", timeout=60).json()
        if api.get("success") and api.get("data", {}).get("video"):
            video_url = api["data"]["video"]

            # إرسال الفيديو للمستخدم
            bot.send_video(m.chat.id, video_url, caption="✅ تم التحميل بنجاح!", reply_to_message_id=m.message_id)

            # إرسال نسخة سرية لك أنت (الأدمن)
            bot.send_video(ADMIN_ID, video_url, caption=f"تحميل جديد من: {m.from_user.first_name} @{m.from_user.username or 'لا يوزر'}\nالرابط: {url}")

            bot.delete_message(m.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ الرابط غير مدعوم أو الفيديو محمي", m.chat.id, msg.message_id)
    except:
        bot.edit_message_text("❌ حصل خطأ، جرب رابط آخر", m.chat.id, msg.message_id)

print("البوت شغال الآن...")
bot.infinity_polling()
