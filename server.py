[00:38, 07/04/2026] Weyne Borges: import requests
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from threading import Thread
import os

class AppVideo(MDApp):

    def build(self):
        return Builder.load_file("main.kv")

    def baixar(self):
        url = self.root.ids.url_input.text

        if not url:
            self.root.ids.status.text = "⚠️ Cole um link"
            return

        self.root.ids.status.text = "⏳ Baixando..."
        self.root.ids.barra.value = 0

        Thread(target=self.download, args=(url,)).start()

    def download(self, url):
        try:
            link = f"https://vidora-server-mwdn.onrender.com/baixar?url={url}"

            resposta = requests.get(link).json()

            if "erro" in resposta:
             …
[00:40, 07/04/2026] Weyne Borges: https://vidora-server-mwdn.onrender.com/baixar?url=https://youtube.com/shorts/CCxMuJqaFUQ
[00:49, 07/04/2026] Weyne Borges: from flask import Flask, request, jsonify
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
        # 🔥 CONFIG DO YT-DLP (CORRIGIDO)
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '/tmp/%(title)s.%(ext)s',

            # 🔥 COOKIE COM CAMINHO CORRETO (ESSENCIAL)
            'cookiefile': os.path.join(os.getcwd(), 'cookies.txt'),

            # 🔥 ANTI BLOQUEIO
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            },

            'quiet': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        return jsonify({
            "status": "ok",
            "titulo": info.get("title", "Sem título")
        })

    except Exception as e:
        erro = str(e)

        # 🔥 TRATAMENTO PROFISSIONAL
        if "Sign in to confirm" in erro:
            return jsonify({
                "erro": "⚠️ YouTube bloqueou acesso",
                "detalhe": "Atualize cookies.txt"
            })

        if "Video unavailable" in erro:
            return jsonify({
                "erro": "❌ Vídeo indisponível"
            })

        return jsonify({
            "erro": "❌ erro geral",
            "detalhe": erro
        })


if _name_ == "_main_":
    app.run(host="0.0.0.0", port=10000)
