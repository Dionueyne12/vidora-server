[00:12, 07/04/2026] Weyne Borges: from kivymd.app import MDApp
from kivy.lang import Builder
import webbrowser

API_URL = "https://vidora-server-mwdn.onrender.com/baixar?url="

KV = '''
MDScreen:

    MDBoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 20

        MDLabel:
            text: "🔥 VIDORA PRO 🔥"
            halign: "center"
            font_style: "H4"

        MDTextField:
            id: link
            hint_text: "Cole o link do vídeo"
            mode: "rectangle"

        MDRaisedButton:
            text: "🚀 BAIXAR VÍDEO"
            pos_hint: {"center_x": 0.5}
            on_release: app.baixar()

        MDLabel:
            id: status
            text: "Aguardando..."
            halign: "center"
'''

class VidoraApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def baixar(self):
        link = self.root.ids.link.text

        if not link:
            self.root.ids.status.text = "⚠️ Cole um link primeiro"
            return

        self.root.ids.status.text = "⏳ Iniciando download..."

        try:
            url = API_URL + link
            webbrowser.open(url)
            self.root.ids.status.text = "✅ Download iniciado!"

        except Exception as e:
            self.root.ids.status.text = f"❌ Erro: {str(e)}"


VidoraApp().run()
[00:15, 07/04/2026] Weyne Borges: "detalhe":"ERRO: [youtube] IGx9LbBko_o: Faça login para confirmar que você\u2019 não é um bot. Use --cookies-from-browser ou --cookies para autenticação. Consulte https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp para saber como passar cookies manualmente. Veja também https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies para dicas sobre como exportar cookies do YouTube de forma eficaz","erro":"\u26a0\ufe0f YouTube bloqueou o acesso (precisa de cookies v\u00e1lidos)."}
[00:20, 07/04/2026] Weyne Borges: https://vidora-server-mwdn.onrender.com
[00:21, 07/04/2026] Weyne Borges: https://vidora-server-mwdn.onrender.com
[00:23, 07/04/2026] Weyne Borges: https://github.com/Dionueyne12/vidora-server
[00:28, 07/04/2026] Weyne Borges: from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(_name_)

@app.route("/")
def home():
    return "🔥 Vidora server online"

@app.route("/baixar")
def baixar():
    url = request.args.get("url")

    if not url:
        return jsonify({"erro": "URL não enviada"})

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',

            # 🔥 COOKIES (ESSENCIAL PRO YOUTUBE)
            'cookiefile': 'cookies.txt',

            # 🔥 HEADERS (anti bloqueio)
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            },

            # 🔥 IGNORA ERROS PARCIAIS
            'ignoreerrors': True,

            # 🔥 SILENCIOSO
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        return jsonify({
            "status": "ok",
            "titulo": info.get("title", "Sem título")
        })

    except Exception as e:
        erro_msg = str(e)

        # 🔥 TRATAMENTO PROFISSIONAL DE ERRO
        if "Sign in to confirm" in erro_msg:
            return jsonify({
                "erro": "⚠️ YouTube bloqueou acesso",
                "detalhe": "Atualize cookies.txt"
            })

        if "Video unavailable" in erro_msg:
            return jsonify({
                "erro": "❌ Vídeo indisponível"
            })

        return jsonify({
            "erro": "Erro desconhecido",
            "detalhe": erro_msg
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
