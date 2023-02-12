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


normalDayMessage:str = """Buongiorno, \n
                        l'aula studio sarà disponibile dalle 16 del pomeriggio \n fino alle 19 della sera.\n
                        """
nightMessage:str = """ Ah no aspetta, ma l'aula studio è aperta pure la sera? \n
                        Civico79: 'Certo, per tutti gli studenti lavoratori,\n 
                        le persone che non trovano un posto tranquillo dove studiare e stare insieme.\n
                        Oppure per quelli che preferiscono al luce della luna a quella del sole.\n
                        L'aula studio sarà a disposizione dalle 19 fino alle 23 con la possibilità di mangiare insieme.\n' """
restMessage:str = """ Buon weekend a tutti, oggi l'aula studio non sarà a disposizione. Però vi aspettiamo per prendere un aperitivo insieme.\n"""
idChannel:str = '@Civico79Livorno'
def writeName(update: Update):
    #print(update.message.from_user)
    info = InfoUser()
    info.firstname = update.message.from_user.first_name
    info.lastname = update.message.from_user.last_name
    info.username = update.message.from_user.username
    with open('nameAccessBot.txt','w') as nameAccesFile:
        nameAccesFile.write(str(info))

def daily_job(bot, update, job_queue):
    """ Running on Mon, Tue, Wed, Thu, Fri = tuple(range(5)) """
    bot.send_message(chat_id=update.effective_chat.id, text='Setting a daily notifications!')
    #t = datetime.time(10, 00, 00, 000000)
    t = datetime.time(0, 00, 15, 000000)
    job_queue.run_daily(messageIoStudio, t, days=tuple(range(7)), context=update)

async def messageIoStudio(update: Update, context: ContextTypes.DEFAULT_TYPE,pIdChannel:str=''):
    message:str = ''
    date = datetime.now()
    dayOfWeek = date.weekday()
    if(dayOfWeek >= 0 and dayOfWeek <= 4): # Monday, Tuesday, Wednesday, Thursday, Friday
        message += normalDayMessage
    elif(dayOfWeek <= 2): # Monday, Tuesday, Wednesday
        message += nightMessage
    else: # Saturday, Sunday   
       message += restMessage
    if(pIdChannel == ''):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        await context.bot.send_message(chat_id=idChannel, text=message)
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao, ti diamo il benvenuto")
    writeName(update) # it is used for to get username and some information of interaction with user

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=idChannel, text='One message every minute')

async def messageOnChannel(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id='@Civico79Livorno', text='One message every minute')


if __name__ == '__main__':
    token:str = input('insert a new token \n')
    application = ApplicationBuilder().token(token).build()
    caps_handler = CommandHandler('caps', caps)
    start_handler = CommandHandler('start', start)
    ioStudio_handler = CommandHandler('ioStudio', messageIoStudio)
    #channel_handler = CommandHandler('channel', messageOnChannel)
    job_queue = application.job_queue

    job_minute = job_queue.run_daily(messageIoStudio, time(hour=15,minute=20,second=00))


    #application.add_handler(CommandHandler('notify', daily_job, pass_job_queue=True))
    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(ioStudio_handler)
    #application.add_handler(channel_handler)
    application.run_polling()