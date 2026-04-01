from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

import os
TOKEN = os.getenv("8062826954:AAGGnR-eNT804QjWlwl5XSRvsY23OH3dy1U")

data = {
    "Primer año": {
        "Anatomia": {
            "Moore": "moore.pdf",
            "Grays": "grays.pdf"
        },
        "Histologia": {
            "Ross": "ross.pdf",
            "Geneser": "geneser.pdf",
            "Fortoul": "fortoul.pdf"
        },
        "Bioquimica": {
            "McKee": "mckee.pdf",
            "Leninger": "leninger.pdf"
        },
        "Embriologia": {
            "Carlson": "carlson.pdf",
            "Arteaga": "arteaga.pdf"
        }
    },
    "Segundo año": {
        "Farmacologia": {
            "Goodman": "goodman.pdf",
            "Goodmancito": "goodmancito.pdf",
            "Golan": "golan.pdf",
            "Katzung": "katzung.pdf"
        },
        "Fisiologia": {
            "Guyton": "guyton.pdf",
            "Boron": "boron.pdf"
        },
        "Inmunologia": {
            "Abbas": "abbas.pdf",
            "Murphy": "murphy.pdf"
        },
        "Cirugia": {
            "Archundia": "archundia.pdf",
            "Schwartz": "schwartz.pdf"
        },
        "Micro y para": {
            "Murray": "murray.pdf",
            "Arenas": "arenas.pdf",
            "Romero": "romero.pdf"
        }
    }
}

def crear_botones(opciones, prefijo):
    botones = []
    for opcion in opciones:
        botones.append([InlineKeyboardButton(opcion, callback_data=f"{prefijo}|{opcion}")])
    return InlineKeyboardMarkup(botones)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = crear_botones(data.keys(), "year")
    await update.message.reply_text("Elige año:", reply_markup=teclado)

async def manejar_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    tipo, valor = query.data.split("|")

    if tipo == "year":
        teclado = crear_botones(data[valor].keys(), valor)
        await query.edit_message_text("Elige materia:", reply_markup=teclado)

    else:
        for year in data:
            if valor in data[year]:
                teclado = crear_botones(data[year][valor].keys(), valor)
                await query.edit_message_text("Elige libro:", reply_markup=teclado)
                return

            for materia in data[year]:
                if valor in data[year][materia]:
                    archivo = data[year][materia][valor]
                    await query.message.reply_document(open(archivo, "rb"))
                    return

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(manejar_click))

app.run_polling()