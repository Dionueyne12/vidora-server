from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

# pasta temporária
DOWNLOAD_DIR = "/tmp"

@app.route("/")
def home():
    return "Servidor Vidora online 🚀"


@app.route("/baixar")
def baixar():
    url = request.args.get("url")

    if not url:
        return jsonify({"erro": "❌ URL não fornecida"}), 400

    try:
        filename = str(uuid.uuid4())

        caminho_saida = os.path.join(DOWNLOAD_DIR, f"{filename}.%(ext)s")

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": caminho_saida,

            # 🔥 COOKIES (ESSENCIAL PRO YOUTUBE)
            "cookiefile": os.path.join(os.getcwd(), "cookies.txt"),

            # evitar bloqueio
            "http_headers": {
                "User-Agent": "Mozilla/5.0"
            },

            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # verifica se baixou mesmo
        if not os.path.exists(file_path):
            return jsonify({
                "erro": "❌ Falha ao localizar o arquivo baixado"
            }), 500

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        erro_str = str(e)

        # 🎯 tratamento inteligente de erros
        if "Sign in to confirm" in erro_str or "cookies" in erro_str:
            return jsonify({
                "erro": "⚠️ YouTube bloqueou (cookies inválidos ou expirados)",
                "detalhe": erro_str
            }), 403

        elif "Video unavailable" in erro_str:
            return jsonify({
                "erro": "❌ Vídeo indisponível"
            }), 404

        elif "Private video" in erro_str:
            return jsonify({
                "erro": "🔒 Vídeo privado"
            }), 403

        elif "age" in erro_str.lower():
            return jsonify({
                "erro": "🔞 Vídeo com restrição de idade"
            }), 403

        else:
            return jsonify({
                "erro": "❌ Erro ao baixar vídeo",
                "detalhe": erro_str
            }), 500


# 🔥 necessário pro Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
