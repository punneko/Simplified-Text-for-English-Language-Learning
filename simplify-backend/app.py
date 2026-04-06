from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.result_routes import result_bp
from routes.history_routes import history_bp
from waitress import serve

app = Flask(__name__)
CORS(
    app,
    resources={r"/api/*": {"origins": "http://localhost:5173"}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization", "X-User-Id"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)



# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(result_bp, url_prefix="/api")
app.register_blueprint(history_bp, url_prefix="/api")

@app.route("/", methods=["GET"])
def home():
    return "<h2>Text Simplifier API is running!</h2>"

if __name__ == "__main__":
    serve(app, host="localhost", port=5000)
