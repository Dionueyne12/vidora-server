from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor rodando 🚀"

@app.route("/baixar")
def baixar():
    url = request.args.get("url")

    if not url:
        return jsonify({"erro": "URL não enviada"})

    try:
        nome = str(uuid.uuid4())
        caminho = f"/tmp/{nome}.mp4"

        ydl_opts = {
            'format': 'best',
            'outtmpl': caminho,
            'quiet': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not os.path.exists(caminho):
            return jsonify({"erro": "Falha ao baixar vídeo"})

        return send_file(caminho, as_attachment=True)

    except Exception as e:
        return jsonify({"erro": str(e)})
