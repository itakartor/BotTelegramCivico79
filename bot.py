import json
import gdown
import logging
import os
from telegram import Bot, Update, InputMediaDocument
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from datetime import datetime
from datetime import time
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN:str = os.environ.get('TOKEN')
PORT:int = int(os.environ.get('PORT', 5000))
logger = logging.getLogger(__name__)
class InfoUser():
    firstname:str
    lastname:str
    username:str
    def __str__(self) -> str:
        return f"{self.firstname} - {self.lastname} - {self.username} - {datetime.now()}"

civico_by_night:bool = False
# These are the main messages
normal_day_message:str = """Buongiorno, l'aula studio sarà disponibile dalle 15:30 del pomeriggio fino alle 19 della sera."""
night_message:str ="""
Ah no aspetta, ma l'aula studio è aperta pure la sera? 

Civico79: 
'Certo fino al 21 Febbraio sarà aperta, per tutti gli studenti lavoratori, 
le persone che non trovano un posto tranquillo dove studiare.
L'aula studio sarà a disposizione dalle 19 fino alle 23 con la possibilità di mangiare insieme.
"""

who_message:str = """ Ciao!
Siamo dei ragazzi di Livorno appartenenti alla realtà del Civico79,
spazio interamente dedicato a noi giovani universitari e lavoratori dai 19 ai 35 anni,
come aula studio e molto altro.Se siete curiosi vi aspettiamo in viale Risorgimento 77 Livorno"""
close_classroom:str = """Oggi l'aula studio riarrà chiusa, ma vi invitiamo a rimanere aggiornati sui nostri social anche attraverso il bot Telegram per i prossimi eventi."""
not_event:str = """Al momento non ci sono eventi in programmazione, in caso che si volesse collaborare per nuovi eventi per i giovani scriveteci pure sui vari social."""
FORMAT_JSON:str = '.json'
FORMAT_IMAGE:str = '.jpg'
FORMAT_SIMPLE_TEXT:str = '.txt'

url_messages:str = ''
NAME_MESSAGGES:str = 'messagges'
url_config_event:str = 'https://drive.google.com/file/d/1MvjWTx3STW7OpaJVz-RK2JGT0Nus5bMf/view?usp=sharing'
NAME_CONFIG:str = 'config'

#Flyer of last event
url_last_event:str = 'https://drive.google.com/file/d/13e2-vwaXl4AM4ZeYjJQuPZG0Imo2eK6V/view?usp=share_link'
NAME_FLYER:str = 'lastFlyer'
message_flyer:str = 'Prossimo evento dedicato al gioco e al Ponce, vi aspettiamo con dei ponce fumanti oppure delle semplici birre per chicchierare e giocare insieme.'

url_file_caption_drive:str = 'https://drive.google.com/file/d/1JhPxjdJIWIOX53TO2sXZA-4tLxlVUlcZ/view?usp=sharing'
NAME_CAPTION_FLYER:str = 'captionLastFlyer'
NAME_ACCESS_FILE:str ='nameAccessBot'
# it uses for to send the messages on the channel
# instead of the user id which I can get from the update object
idChannel:str = '@Civico79Livorno'
channelDebug:str = '@provePazze'

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# this function get the name of the people which uses the bot
def writeName(update: Update):
    #print(update.message.from_user)
    info = InfoUser()
    info.firstname = update.message.from_user.first_name
    info.lastname = update.message.from_user.last_name
    info.username = update.message.from_user.username
    with open(NAME_ACCESS_FILE + FORMAT_SIMPLE_TEXT,'a') as nameAccesFile:
        nameAccesFile.write(str(info))

# def daily_job(bot, update, job_queue):
#     """ Running on Mon, Tue, Wed, Thu, Fri = tuple(range(5)) """
#     bot.send_message(chat_id=update.effective_chat.id, text='Setting a daily notifications!')
#     #t = datetime.time(10, 00, 00, 000000)
#     t = datetime.time(0, 00, 15, 000000)
#     job_queue.run_daily(messageIoStudio, t, days=tuple(range(7)), context=update)
async def messageIoStudio(context: ContextTypes.DEFAULT_TYPE,pIdChannel:str=idChannel):
    await context.bot.send_message(chat_id=pIdChannel, text=close_classroom)
async def messageIoStudioUser(update: Update,context: ContextTypes.DEFAULT_TYPE):
    message:str = ''
    date = datetime.now()
    dayOfWeek = date.weekday()
    if(dayOfWeek >= 0 and dayOfWeek <= 4): # Monday, Tuesday, Wednesday, Thursday, Friday
        message += normal_day_message
    elif(dayOfWeek >=5 and dayOfWeek <= 7):
        message = close_classroom
    if(dayOfWeek <= 2 and civico_by_night): # Monday, Tuesday, Wednesday
        message += night_message
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao, ti diamo il benvenuto")
    writeName(update) # it is used for to get username and some information of interaction with user

async def instagram(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='https://www.instagram.com/civico79livorno')
async def facebook(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='https://www.facebook.com/civico79livorno')
async def youtube(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Il video dell\'ultimo evento: https://youtu.be/ISPGx5LUXMQ')
async def who(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=who_message)
async def event(update: Update,context: ContextTypes.DEFAULT_TYPE): #'https://drive.google.com/file/d/13e2-vwaXl4AM4ZeYjJQuPZG0Imo2eK6V/view?usp=share_link'
    if(url_last_event == ''):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=not_event)
    else:
        gdown.download(url_file_caption_drive, NAME_CAPTION_FLYER + FORMAT_SIMPLE_TEXT, quiet=False,fuzzy=True)
        caption:str = ''
        with open(NAME_CAPTION_FLYER+FORMAT_SIMPLE_TEXT,'r') as file:
            caption = file.read()
        gdown.download(url_last_event, NAME_FLYER + FORMAT_IMAGE, quiet=False,fuzzy=True)
        with open(NAME_FLYER + FORMAT_IMAGE,'rb') as media_1:
            await context.bot.send_photo(chat_id=update.effective_chat.id,photo=media_1, caption=caption)
async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=idChannel, text='One message every minute')
async def init(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=channelDebug,text="aggiornamento cofig civico79")
    gdown.download(url_config_event, NAME_CONFIG + FORMAT_JSON, quiet=False,fuzzy=True)
    with open(NAME_CONFIG + FORMAT_JSON,'r') as file:
        listOfGLobal = globals()
        data = json.load(file)
        listOfGLobal['url_last_event'] = data['url_flyer'] 
        listOfGLobal['url_file_caption_drive'] = data['url_caption']
        listOfGLobal['civico_by_night'] = data['civico_by_night']
        listOfGLobal['url_messages'] = data['url_messages']
    gdown.download(url_messages, NAME_MESSAGGES + FORMAT_JSON, quiet=False,fuzzy=True)
    with open(NAME_MESSAGGES + FORMAT_JSON,'r') as messages:
        data = json.load(messages)
        listOfGLobal['normal_day_message'] = data['normal_day']
        listOfGLobal['night_message'] = data['night']
        listOfGLobal['close_classroom'] = data['close_classroom']
        listOfGLobal['who_message'] = data['who']
        listOfGLobal['not_event'] = data['not_event']
 
def main():
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    ioStudio_handler = CommandHandler('iostudio', messageIoStudioUser)
    instagram_handler = CommandHandler('instagram', instagram)
    facebook_handler = CommandHandler('facebook', facebook)
    youtube_handler = CommandHandler('youtube', youtube)
    who_handler = CommandHandler('chiii', who)
    event_handler = CommandHandler('evento', event)
    # queue of the jobs
    job_queue = application.job_queue

    # the job starts to 11:00 + timezone, i have to use timezone
    if(civico_by_night):
        job_minute = job_queue.run_daily(messageIoStudio, time(hour=11,minute=00,second=00))
    
    job_minute_init = job_queue.run_repeating(init,interval=60*60*4)#for each 4 hours the bot gets the config

    application.add_handler(start_handler)
    application.add_handler(ioStudio_handler)
    application.add_handler(instagram_handler)
    application.add_handler(facebook_handler)
    application.add_handler(who_handler)
    application.add_handler(event_handler)
    application.add_handler(youtube_handler)
    
    # log all errors
    application.add_error_handler(error)

    # Start the Bot
    application.run_polling()
#
if __name__ == '__main__':
    main()