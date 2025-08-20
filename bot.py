from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
from bs4 import BeautifulSoup

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    if "shopee" not in message:
        return

    url = message.strip()

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Obter título da aba
        title = soup.title.string.strip()

        # Tenta pegar uma imagem
        image_tag = soup.find('img')
        image_url = image_tag['src'] if image_tag else None

        # Preços fixos simulados (você pode adaptar com scraping real se quiser)
        preco_original = "R$46,00"
        preco_promocional = "R$7,99"

        # Texto final
        texto = f"""📦 {title}

~~{preco_original}~~  
✅ {preco_promocional}

🔗 {url}

*Promoção sujeita à alteração*
"""

        if image_url:
            await update.message.reply_photo(photo=image_url, caption=texto, parse_mode='Markdown')
        else:
            await update.message.reply_text(texto)

    except Exception as e:
        await update.message.reply_text("❌ Erro ao processar o link.")
        print(f"Erro: {e}")

# COLE SEU TOKEN AQUI
TOKEN = "SEU_TOKEN_AQUI"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot rodando...")
app.run_polling()
