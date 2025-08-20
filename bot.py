import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("TOKEN")  # ✅ Puxa direto da variável de ambiente do Replit

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    if "shopee" not in message:
        return
    url = message.strip()
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else "Produto Shopee"
        img_tag = soup.find("img")
        image_url = img_tag['src'] if img_tag else None
        preco_original = "R$46,00"
        preco_promocional = "R$7,99"
        texto = f"""📦 {title}\n\n~~{preco_original}~~\n✅ {preco_promocional}\n\n🔗 {url}\n\n*Promoção sujeita à alteração*"""
        if image_url:
            await update.message.reply_photo(photo=image_url, caption=texto, parse_mode='Markdown')
        else:
            await update.message.reply_text(texto)
    except Exception as e:
        await update.message.reply_text("❌ Erro ao processar o link.")
        print(e)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 Bot rodando...")
app.run_polling()
