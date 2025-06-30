# main.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import re

from config import FORCE_CHANNEL, ADMIN_ID
from keep_alive import keep_alive
from downloader import youtube, instagram, tiktok, pinterest

BOT_TOKEN = "7705956184:AAGzgWtufVUiQhod1UxYGdEqBTl5kzy7TOQ"

bot = Client(
    "TrapDownloaderBot",
    bot_token=BOT_TOKEN,
    api_id=10896344,
    api_hash="b642b4217b34b1f6ef8b8f4e6c5f0c89"
)

# ------------------------- ابزارها -------------------------

def check_membership(user_id):
    try:
        member = bot.get_chat_member(FORCE_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def get_platform(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "instagram.com" in url:
        return "instagram"
    elif "tiktok.com" in url:
        return "tiktok"
    elif "pinterest.com" in url:
        return "pinterest"
    else:
        return "unknown"

# ------------------------- دکمه عضویت -------------------------

def join_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{FORCE_CHANNEL.strip('@')}")],
        [InlineKeyboardButton("✅ عضویت زدم، بیا", callback_data="refresh")]
    ])

# ------------------------- فرمان /start -------------------------

@bot.on_message(filters.command("start"))
def start(client, message: Message):
    user_id = message.from_user.id
    if not check_membership(user_id):
        message.reply("برای استفاده از ربات اول باید عضو کانال بشی ⬇️", reply_markup=join_button())
        return
    message.reply(
        "🎬 سلام! لینک هر پست یا ویدیو از YouTube، Instagram، TikTok، Pinterest رو بفرست تا برات دانلود کنم.\n\n🔗 فقط کافیه لینک رو بفرستی."
    )

# ------------------------- هندل پیام‌ها -------------------------

@bot.on_message(filters.private & filters.text)
def downloader(client, message: Message):
    user_id = message.from_user.id
    text = message.text.strip()

    if not check_membership(user_id):
        message.reply("🔒 برای استفاده از ربات باید اول عضو کانال بشی:", reply_markup=join_button())
        return

    url_regex = r"https?://[^\s]+"
    match = re.search(url_regex, text)
    if not match:
        message.reply("❌ لطفاً یک لینک معتبر ارسال کن.")
        return

    url = match.group()
    platform = get_platform(url)

    message.reply("⏳ در حال پردازش لینک...")

    try:
        if platform == "youtube":
            result = youtube.download_youtube(url)
        elif platform == "instagram":
            result = instagram.download_instagram(url)
        elif platform == "tiktok":
            result = tiktok.download_tiktok(url)
        elif platform == "pinterest":
            result = pinterest.download_pinterest(url)
        else:
            message.reply("❌ پلتفرم این لینک پشتیبانی نمی‌شود.")
            return

        if "error" in result:
            message.reply(f"❌ خطا: {result['error']}")
        else:
            message.reply(f"✅ عنوان: {result.get('title', 'بدون عنوان')}\n📥 لینک دانلود:\n{result.get('url')}")
    except Exception as e:
        message.reply(f"⚠️ مشکلی پیش اومد: {str(e)}")

# ------------------------- هندل عضویت مجدد -------------------------

@bot.on_callback_query(filters.regex("refresh"))
def refresh_join(c, callback_query):
    user_id = callback_query.from_user.id
    if check_membership(user_id):
        callback_query.message.edit_text("✅ عضویت تأیید شد. حالا لینک ارسال کن.")
    else:
        callback_query.answer("❌ هنوز عضو نشدی!", show_alert=True)

# ------------------------- اجرای ربات -------------------------

keep_alive()
print("🤖 Bot is running...")
bot.run()
