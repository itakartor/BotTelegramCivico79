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

# These are the main messages
NORMAL_DAY_MESSAGE:str = """Buongiorno, 
l'aula studio sarà disponibile dalle 15:30 del pomeriggio fino alle 19 della sera.
"""
NIGHT_MESSAGE:str ="""
Ah no aspetta, ma l'aula studio è aperta pure la sera? 

Civico79: 
'Certo fino al 21 Febbraio sarà aperta, per tutti gli studenti lavoratori, 
le persone che non trovano un posto tranquillo dove studiare.
L'aula studio sarà a disposizione dalle 19 fino alle 23 con la possibilità di mangiare insieme.
"""
REST_MESSAGE:str = """ Buon weekend a tutti, oggi l'aula studio non sarà a disposizione. Però vi aspettiamo nei prossimi giorni per prendere un aperitivo insieme.\n"""

WHO_MESSAGE:str = """ Ciao!
Siamo dei ragazzi di Livorno appartenenti alla realtà del Civico79,
spazio interamente dedicato a noi giovani universitari e lavoratori dai 19 ai 35 anni,
come aula studio e molto altro.Se siete curiosi vi aspettiamo in viale Risorgimento 77 Livorno"""
CLOSE_CLASSROOM = """Oggi l'aula studio riarrà chiusa, ma vi invitiamo a rimanere aggiornati sui nostri social anche attraverso il bot Telegram per i prossimi eventi."""
#Flyer of last event
URL_LAST_EVENT = 'https://drive.google.com/file/d/13e2-vwaXl4AM4ZeYjJQuPZG0Imo2eK6V/view?usp=share_link'
NAME_FLYER = 'lastFlyer'
FORMAT_IMAGE = '.jpg'
MESSAGE_FLYER = 'Prossimo evento dedicato al gioco e al Ponce, vi aspettiamo con dei ponce fumanti oppure delle semplici birre per chicchierare e giocare insieme.'

# it uses for to send the messages on the channel
# instead of the user id which I can get from the update object
idChannel:str = '@Civico79Livorno'

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
    with open('nameAccessBot.txt','w') as nameAccesFile:
        nameAccesFile.write(str(info))

# def daily_job(bot, update, job_queue):
#     """ Running on Mon, Tue, Wed, Thu, Fri = tuple(range(5)) """
#     bot.send_message(chat_id=update.effective_chat.id, text='Setting a daily notifications!')
#     #t = datetime.time(10, 00, 00, 000000)
#     t = datetime.time(0, 00, 15, 000000)
#     job_queue.run_daily(messageIoStudio, t, days=tuple(range(7)), context=update)
async def messageIoStudio(context: ContextTypes.DEFAULT_TYPE,pIdChannel:str=idChannel):
    await context.bot.send_message(chat_id=pIdChannel, text=CLOSE_CLASSROOM)
async def messageIoStudio(context: ContextTypes.DEFAULT_TYPE,pIdChannel:str=idChannel):
    message:str = ''
    date = datetime.now()
    dayOfWeek = date.weekday()
    if(dayOfWeek >= 0 and dayOfWeek <= 4): # Monday, Tuesday, Wednesday, Thursday, Friday
        message += NORMAL_DAY_MESSAGE
    else: # Saturday, Sunday   
       message += REST_MESSAGE
    if(dayOfWeek <= 2): # Monday, Tuesday, Wednesday
        message += NIGHT_MESSAGE
    await context.bot.send_message(chat_id=pIdChannel, text=message)
    
async def messageIoStudioUser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await messageIoStudio(context,update.effective_chat.id)

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
    await context.bot.send_message(chat_id=update.effective_chat.id, text=WHO_MESSAGE)
async def event(update: Update,context: ContextTypes.DEFAULT_TYPE): #'https://drive.google.com/file/d/13e2-vwaXl4AM4ZeYjJQuPZG0Imo2eK6V/view?usp=share_link'
    gdown.download(URL_LAST_EVENT, NAME_FLYER + FORMAT_IMAGE, quiet=False,fuzzy=True)
    media_1 = open(NAME_FLYER + FORMAT_IMAGE,'rb')
    await context.bot.send_photo(chat_id=update.effective_chat.id,photo=media_1, caption=MESSAGE_FLYER)

async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=idChannel, text='One message every minute')

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

    # the job starts to 11:00
    job_minute = job_queue.run_daily(messageIoStudio, time(hour=11,minute=00,second=00))
    

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