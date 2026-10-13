import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 1. Masukkan TOKEN bot kamu dari BotFather (di dalam tanda kutip)
TOKEN = '8697395026:AAEiuoiUkVdhOA_rXNpxoodavU-qa8XGOj8'

# 2. Masukkan ID Channel dan Grup (harus berupa angka, contoh: -1001234567890)
CHANNEL_ID = - 4330324143
GROUP_ID = - 3975403288    

# 3. Masukkan Link T.me Channel dan Grup preview kamu
CHANNEL_LINK = "https://t.me/asupansukasukaa" 
GROUP_LINK = "https://t.me/sukasukagalerii"       

bot = telebot.TeleBot(TOKEN)

# Fungsi untuk mengecek apakah user sudah gabung
def check_membership(user_id):
    try:
        member_channel = bot.get_chat_member(CHANNEL_ID, user_id)
        member_group = bot.get_chat_member(GROUP_ID, user_id)
        
        status_ok = ['creator', 'administrator', 'member']
        
        is_in_channel = member_channel.status in status_ok
        is_in_group = member_group.status in status_ok
        
        return is_in_channel and is_in_group
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

# Handler /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if check_membership(user_id):
        bot.send_message(
            message.chat.id, 
            f"Halo **{message.from_user.first_name}**! Selamat datang di **@asupansukasukabot**! 🔥\n\nAkses kamu sudah terbuka.",
            parse_mode="Markdown"
        )
    else:
        markup = InlineKeyboardMarkup()
        btn_channel = InlineKeyboardButton("📢 Gabung Channel", url=CHANNEL_LINK)
        btn_group = InlineKeyboardButton("💬 Gabung Grup", url=GROUP_LINK)
        btn_verify = InlineKeyboardButton("✅ Cek Verifikasi", callback_data="verify_join")
        
        markup.add(btn_channel)
        markup.add(btn_group)
        markup.add(btn_verify)
        
        bot.send_message(
            message.chat.id, 
            "⚠️ **Akses Terkunci!**\n\nUntuk menggunakan **@asupansukasukabot**, kamu **wajib** bergabung ke Channel dan Grup kami terlebih dahulu:",
            reply_markup=markup,
            parse_mode="Markdown"
        )

# Handler Tombol Cek Verifikasi
@bot.callback_query_handler(func=lambda call: call.data == "verify_join")
def verify_callback(call):
    user_id = call.from_user.id
    
    if check_membership(user_id):
        bot.answer_callback_query(call.id, "Terima kasih! Kamu sudah terverifikasi. 🎉", show_alert=True)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Selamat datang **{call.from_user.first_name}** di **@asupansukasukabot**! Akses kamu aktif.",
            parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(
            call.id, 
            "❌ Kamu belum bergabung di Channel/Grup! Silakan gabung dulu.", 
            show_alert=True
        )

print("Bot @asupansukasukabot berjalan...")
bot.infinity_polling()