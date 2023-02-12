import logging
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from datetime import datetime
from datetime import time
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
class InfoUser():
    firstname:str
    lastname:str
    username:str
    def __str__(self) -> str:
        return f"{self.firstname} - {self.lastname} - {self.username} - {datetime.now()}"

# These are the main messages
normalDayMessage:str = """Buongiorno, \n
                        l'aula studio sarà disponibile dalle 16 del pomeriggio \n fino alle 19 della sera.\n
                        """
nightMessage:str = """ Ah no aspetta, ma l'aula studio è aperta pure la sera? \n
                        Civico79: 'Certo, per tutti gli studenti lavoratori,\n 
                        le persone che non trovano un posto tranquillo dove studiare e stare insieme.\n
                        Oppure per quelli che preferiscono al luce della luna a quella del sole.\n
                        L'aula studio sarà a disposizione dalle 19 fino alle 23 con la possibilità di mangiare insieme.\n' """
restMessage:str = """ Buon weekend a tutti, oggi l'aula studio non sarà a disposizione. \nPerò vi aspettiamo nei prossimi giorni per prendere un aperitivo insieme.\n"""

whoMessage:str = """ Ciao! \nSiamo dei ragazzi di Livorno appartenenti alla realtà del Civico79,\n spazio interamente dedicato a noi giovani universitari e lavoratori dai 19 ai 35 anni,\n come aula studio e molto altro.\n"""

# it uses for to send the messages on the channel
# instead of the user id which I can get from the update object
idChannel:str = '@Civico79Livorno'

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
    message:str = ''
    date = datetime.now()
    dayOfWeek = date.weekday()
    if(dayOfWeek >= 0 and dayOfWeek <= 4): # Monday, Tuesday, Wednesday, Thursday, Friday
        message += normalDayMessage
    elif(dayOfWeek <= 2): # Monday, Tuesday, Wednesday
        message += nightMessage
    else: # Saturday, Sunday   
       message += restMessage
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
async def who(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=whoMessage)

async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=idChannel, text='One message every minute')


if __name__ == '__main__':
    token:str = input('insert a new token \n')
    application = ApplicationBuilder().token(token).build()
    start_handler = CommandHandler('start', start)
    ioStudio_handler = CommandHandler('iostudio', messageIoStudioUser)
    instagram_handler = CommandHandler('instagram', instagram)
    facebook_handler = CommandHandler('facebook', facebook)
    who_handler = CommandHandler('chiii', who)
    
    # queue of the jobs
    job_queue = application.job_queue

    # the job starts to 11:00
    job_minute = job_queue.run_daily(messageIoStudio, time(hour=11,minute=00,second=00))


    application.add_handler(start_handler)
    application.add_handler(ioStudio_handler)
    application.add_handler(instagram_handler)
    application.add_handler(facebook_handler)
    application.add_handler(who_handler)
    application.run_polling()