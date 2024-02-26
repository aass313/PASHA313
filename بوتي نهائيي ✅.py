from telebot import TeleBot, types
bot = TeleBot('6741898409:AAHKsjoOGcV1c-8yDeQWgrBIWJRSlc6SrWc')
group_id = -1002081735927
admin_id = 647776789  
admins = []  
pending_posts = {}
approved_users = set()
from telegram import InputMediaPhoto
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id in approved_users:
        user_name = message.from_user.first_name
        user_username = message.from_user.username if message.from_user.username else ""
        user_id = message.from_user.id
        welcome_image_url = "https://i.postimg.cc/BvwzKWD3/16791cec34ca5eb738e1db6799e8d0fd.jpg"
        welcome_message_template = f"""
        مرحبا بك [{user_name}](https://telegram.me/{user_username}) في بوت صور الصيد 🖤
        
ارسل صور صيدك ليتم نشرها في قناة صور الصيد 🔥

قناة صور الصيد : ✨ [اضغط هنا](https://telegram.me/OBA_R) ✨
"""

        # إرسال الرسالة الترحيبية مع الصورة مباشرة
        bot.send_photo(message.chat.id, welcome_image_url, caption=welcome_message_template, parse_mode='Markdown')      
    else:        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("موافقة", callback_data="approve"))
        bot.send_message(user_id, """مرحبا بك في بوت صور الصيد 🛸

⚠️ عليك ان تقرأ قبل الموافقة  ⚠️

1- ارسل ك صوره واحدة وليس مجموعة صور 🔹

2- لا ترسل GIF او فيديو او ملصقات 🔸

3- لا ترسل اي شيئ غير صور الصيد ♦️

🚸 في حال مخالفة ما ذكر سيتم حظرك من البوت والقنوات 🚸""", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data == "approve")
def approve_user(call):
    user_id = call.from_user.id
    approved_users.add(user_id)
    bot.send_message(user_id, "𒁂 تم تأكيد موافقتك على الشروط 𒁂")
    bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    user_id = message.from_user.id
    if user_id in approved_users:
        photo_id = message.photo[-1].file_id
        caption = message.caption if message.caption else ''
        pending_posts[user_id] = {'photo_id': photo_id, 'caption': caption}
        bot.send_message(user_id, "☚ تم استلام صور صيدك شكرا لك ☛")
        send_post_for_approval(message)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("موافقة", callback_data="approve"))
        bot.send_message(user_id, """مرحبا بك في بوت صور الصيد 🛸

⚠️ عليك ان تقرأ قبل الموافقة  ⚠️

1- ارسل ك صوره واحدة وليس مجموعة صور 🔹

2- لا ترسل GIF او فيديو او ملصقات 🔸

3- لا ترسل اي شيئ غير صور الصيد ♦️

🚸 في حال مخالفة ما ذكر سيتم حظرك من البوت والقنوات 🚸""", reply_markup=markup)
def send_post_for_approval(message):
    user_id = message.from_user.id
    photo_data = pending_posts[user_id]
    photo_id = photo_data['photo_id']
    caption = photo_data['caption']
    username = bot.get_chat(user_id).username
    markup = types.InlineKeyboardMarkup()
    approve_button = types.InlineKeyboardButton("موافقة", callback_data=f"approve_{user_id}")
    reject_button = types.InlineKeyboardButton("رفض", callback_data=f"reject_{user_id}")
    markup.row(approve_button, reject_button)
    bot.send_photo(group_id, photo_id, caption=f" {caption}\n\n⚜️ لقد تم إرسال صورة الصيد من @{username} ⚜️", reply_markup=markup)    
@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def approve_post(call):
    user_id = int(call.data.split('_')[1])
    photo_data = pending_posts.pop(user_id, None)
    if photo_data:
        photo_id = photo_data['photo_id']
        admin_username = bot.get_chat(admin_id).username
        approving_admin_username = bot.get_chat(call.from_user.id).username
        RAM = f"\n\nتمت الموافقة عليه بواسطة @{approving_admin_username}"
        caption = f"{photo_data['caption']}"        
        username = bot.get_chat(user_id).username  
        bot.send_photo('-1001630983368', photo_id, caption=f" {caption}\n\n⚜️ لقد تم إرسال صورة الصيد من @{username} ⚜️")             
        bot.send_photo(group_id, photo_id, caption=RAM)   
        bot.send_message(user_id, "تمت الموافقة على صور صيدك وتم نشرها")
    else:
        bot.send_message(group_id, "لا يوجد صور صيد معلقة لهذا المستخدم")
    bot.edit_message_reply_markup(group_id, call.message.message_id)
@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_"))
def reject_post(call):
    user_id = int(call.data.split('_')[1])
    pending_posts.pop(user_id, None)
    bot.send_message(user_id, "تم رفض صور صيدك")
    bot.edit_message_reply_markup(group_id, call.message.message_id)
bot.polling()