from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import subprocess

app = Flask(__name__)

# 🔥 Atualiza yt-dlp ao iniciar
subprocess.run(["pip", "install", "-U", "yt-dlp"])

@app.route("/")
def home():
    return "Vidora servidor online 🚀"

@app.route("/baixar")
def baixar():
    url = request.args.get("url")

    if not url:
        return jsonify({"erro": "URL inválida"}), 400

    caminho = "video.mp4"

    try:
        ydl_opts = {
            'outtmpl': caminho,
            'format': 'best'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(caminho, as_attachment=True)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
