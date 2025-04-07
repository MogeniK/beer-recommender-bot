import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from model import load_model, predict_beer

model = load_model('beer_model.h5')

IBU, ABV, SRM, TEMP, PRICE, FRUIT, MALT, LIGHT, SMOKE, CARB = range(10)

async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Привіт! Я допоможу тобі обрати пиво за твоїми вподобаннями.\n"
        "Відповідай на кілька запитань, щоб я міг зробити рекомендацію.\n\n"
        "Спочатку, наскільки гірке пиво ти віддаєш перевагу? (0-100 IBU)"
    )
    return IBU

async def ibu(update: Update, context: CallbackContext) -> int:
    context.user_data['ibu'] = float(update.message.text)
    await update.message.reply_text(
        "Яка міцність пива тобі подобається? (у відсотках ABV)"
    )
    return ABV

# Similar code for other conversation states...

def main() -> None:
    application = Application.builder().token(os.getenv("TELEGRAM_API_TOKEN")).build()
    
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            IBU: [MessageHandler(filters.TEXT & ~filters.COMMAND, ibu)],
            ABV: [MessageHandler(filters.TEXT & ~filters.COMMAND, abv)],
            SRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, srm)],
            # Add other states...
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conversation_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
    