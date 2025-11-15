from flask import Flask, render_template,request,send_file
import os
import Image_create

app = Flask(__name__)
PROCESSED_FOLDER = 'processed'
TEST = 0
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs("TEST", exist_ok=True)

# ★ まずは全許可で動作確認（開発用）:
# CORS(
#     app,
#     resources={r"/upload": {"origins": "*"}},  # 動的に絞る前の確認用
#     supports_credentials=False,                 # Cookie使うなら True にし、origins は * ではなく限定必須
#     methods=["GET", "POST", "OPTIONS"],
#     allow_headers=["Content-Type", "Authorization"],
#     expose_headers=[],
#     max_age=86400
# )

@app.route('/')
def index():
    return render_template('editor.html')

@app.route('/crop')
def crop_page():
    return render_template('crop.html')

@app.route('/send')
def send_page():
    return render_template('send.html')

@app.route('/input')
def input_page():
    return render_template('input.html')

@app.route("/upload", methods=["POST"])
def upload():
    print("\033[32m" + "UPLOAD_SUCSSES")
    raw_areas = request.form.getlist("SnippingArea[]")
    CreateImg = Image_create.createSerialImage(request,raw_areas)
    serialimage = CreateImg.cserialImage()
    processed_path = os.path.join(PROCESSED_FOLDER, "prossed.png")
    serialimage.save(processed_path)
    
    print("\033[0m")
    return send_file(processed_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)