from datetime import datetime
import telebot
from telebot import types
bot = telebot.TeleBot('')
class PESEL:
    def __init__(self, number):
        self.number = number
        self.year = None
        self.month = None
        self.day = None
    def validate(self):
        if self.number.isdigit() and len(self.number) == 11 and (1 <= int(self.number[2:4]) <=12 or 21 <= int(self.number[2:4]) <= 32):
            if int(self.number[2:4]) <= 12:
                self.month = int(self.number[2:4])
                self.year = 1900 + int(self.number[0:2])
                self.day = int(self.number[4:6])
            else:
                self.month = int(self.number[2:4]) - 20
                self.year = 2000 + int(self.number[0:2])
                self.day = int(self.number[4:6])
            try:
                datetime(self.year, self.month, self.day)
            except ValueError:
                print('You wrote date wrong')
                return False 
            weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
            checksum = sum(int(d)*w for d, w in zip(self.number[:10], weights))
            check_digit = (10 - (checksum % 10)) % 10
            if check_digit != int(self.number[10]):
                print(f'PESEL {self.number} has invalid control digit')
                return False

            return True
        else:
            print('You wrote something wrong')
            return False 
    def get_birth_date(self):
        if self.year is None:
            return False
        return datetime(self.year, self.month, self.day)
    def get_gender(self):
            return 'Female' if int(self.number[9]) % 2 == 0 else 'Male'
    def __str__(self):
        return f'PESEL: {self.number}'
    
class PeselList():
    def __init__(self):
        self.pesels = []
    def add_pesel(self, pesel_number):
        p = PESEL(pesel_number)
        if p.validate():
            for i in self.pesels:
                if i.number == pesel_number:
                    print('You wrote this pesel before')
                    return False
            self.pesels.append(p)
            return True
    def sort_by_date(self):
        return sorted(self.pesels, key=lambda p: p.get_birth_date())
    
    def sort_by_gender(self):
        return sorted(self.pesels, key=lambda p: 0 if p.get_gender() == 'Female' else 1)
    
    def sort_by_gender_and_date(self):
        return sorted(
            self.pesels,
            key=lambda p: (
                0 if p.get_gender() == 'Female' else 1,
                p.get_birth_date()
            )
        )
    def load_from_file(self, filename):
        self.pesels.clear()
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                number = line.strip()
                if number:
                    p = PESEL(number)
                    if p.validate():
                        self.pesels.append(p)
        
    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for p in self.pesels:
                f.write(p.number + '\n')

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Write your number pesel:')
    bot.register_next_step_handler(msg, process_answer)

pesel_list = PeselList()

def main_button():
    btn1 = types.InlineKeyboardButton('show sort by date', callback_data='by_date')
    btn2 = types.InlineKeyboardButton('show sort by gender', callback_data='by_gender')
    btn3 = types.InlineKeyboardButton('show sort by date and gender', callback_data='by_date_and_gender')
    btn4 = types.InlineKeyboardButton('show all pesel', callback_data='show_all')
    btn5 = types.InlineKeyboardButton('add another pesel', callback_data='add_pesel')
    return btn1, btn2, btn3, btn4, btn5

  
def process_answer(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(*main_button())
    pesel = PESEL(message.text)
    if pesel.validate():
        bot.send_message(message.chat.id, '✅ PESEL valid', reply_markup=markup)
        if not pesel_list.add_pesel(message.text):
            bot.send_message(message.chat.id, 'But you wrote this pesel before')
    else:
        msg = bot.send_message(message.chat.id, '❌ Invalid PESEL, try again:')
        bot.register_next_step_handler(msg, process_answer)

@bot.callback_query_handler(func=lambda call: call.data == 'add_pesel')
def callback(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    bot.delete_message(chat_id, call.message.message_id)
    msg = bot.send_message(chat_id, 'Write your number pesel')
    bot.register_next_step_handler(msg, process_answer)
    
@bot.callback_query_handler(func=lambda call: call.data == 'by_date')
def callback(call):
    markup = types.InlineKeyboardMarkup()
    for btn in main_button():
        markup.add(btn)
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "\n".join(f"{i+1}.) {p.number}" for i, p in enumerate(pesel_list.sort_by_date())), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'by_gender')
def callback(call):
    markup = types.InlineKeyboardMarkup()
    for btn in main_button():
        markup.add(btn)
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "\n".join(f"{i+1}.) {p.number}" for i, p in enumerate(pesel_list.sort_by_gender())), reply_markup=markup)
   
@bot.callback_query_handler(func=lambda call: call.data == 'by_date_and_gender')
def callback(call):
    markup = types.InlineKeyboardMarkup()
    for btn in main_button():
        markup.add(btn)
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "\n".join(f"{i+1}.) {p.number}" for i, p in enumerate(pesel_list.sort_by_gender_and_date())), reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: call.data == 'show_all')
def callback(call):
    markup = types.InlineKeyboardMarkup()
    for btn in main_button():
        markup.add(btn)
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "\n".join(p.number for p in pesel_list.pesels), reply_markup=markup)

 


bot.polling()