from flask import Flask, request, jsonify
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
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '/tmp/%(title)s.%(ext)s',

            'cookiefile': 'cookies.txt',

            'http_headers': {
                'User-Agent': 'Mozilla/5.0'
            },

            'quiet': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        return jsonify({
            "status": "ok",
            "titulo": info.get("title"),
            "arquivo": info.get("title") + ".mp4"
        })

    except Exception as e:
        erro = str(e)

        if "Sign in to confirm" in erro:
            return jsonify({
                "erro": "⚠️ YouTube bloqueou (cookies)"
            })

        return jsonify({
            "erro": "❌ erro geral",
            "detalhe": erro
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
