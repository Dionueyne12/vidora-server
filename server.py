from flask import Flask, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

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
            'format': 'bestvideo+bestaudio/best',
            'cookiefile': 'cookies.txt',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0'
            },
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(caminho, as_attachment=True)

    except Exception as e:
        erro_msg = str(e)

        if "unavailable" in erro_msg:
            mensagem = "❌ Este vídeo não está disponível."
        elif "Sign in to confirm" in erro_msg:
            mensagem = "⚠️ YouTube bloqueou o acesso (precisa de cookies válidos)."
        elif "private" in erro_msg:
            mensagem = "🔒 Este vídeo é privado."
        elif "age" in erro_msg:
            mensagem = "🔞 Vídeo com restrição de idade."
        else:
            mensagem = "❌ Erro ao baixar o vídeo."

        return jsonify({
            "erro": mensagem,
            "detalhe": erro_msg
        }), 500


# 🔥 IMPORTANTE PARA O RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
