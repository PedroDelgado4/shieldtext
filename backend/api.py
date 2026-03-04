from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import string
import os

# Inicializar la aplicación Flask
app = Flask(__name__)
origins_list = [
        "http://localhost:5173", # Vite por defecto
        "https://shieldtext.vercel.app"
]

# Configuración extendida de CORS para manejar preflights
CORS(app, resources={r"/*": {
        "origins": origins_list,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
}})

# --- Middleware para forzar cabeceras CORS (Ciberseguridad/Robustez) ---
@app.after_request
def add_cors_headers(response):
    """Inyecta las cabeceras necesarias en cada respuesta del servidor."""
    origin = request.headers.get('Origin')
    if origin in origins_list:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# --- Cargar el modelo y la función de limpieza ---
# Esto se hace solo una vez cuando el servidor arranca

def cargar_modelo():
    """Carga el modelo desde el archivo .joblib."""
    # Definimos la ruta absoluta primero para que esté disponible en todo el bloque
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_modelo = os.path.join(base_dir, 'spam_detector.joblib')
    try:
        print(f"--- Intentando cargar modelo desde: {ruta_modelo} ---")
        modelo = joblib.load(ruta_modelo)
        print("✅ ¡Modelo cargado exitosamente!")
        return modelo
    except FileNotFoundError:
        print(f"❌ ERROR CRÍTICO: No se encontró el archivo del modelo en {ruta_modelo}")
        return None

def limpiar_texto(texto):
    """Limpia el texto de puntuación."""
    if isinstance(texto, str):
        return texto.translate(str.maketrans('', '', string.punctuation))
    return texto

# Cargamos el modelo al iniciar la app
modelo = cargar_modelo()

# --- Definir la ruta de la API ---
@app.route('/predict', methods=['POST', 'OPTIONS'])
@app.route('/predict/', methods=['POST', 'OPTIONS'])
def predict():
    """
    Ruta que recibe un texto y devuelve la predicción del modelo.
    """
    
    # Manejo manual de peticiones OPTIONS para evitar error 415
    if request.method == 'OPTIONS':
        return '', 200

    if modelo is None:
        return jsonify({'error': 'Modelo no encontrado, verifica que spam_detector.joblib exista.'}), 500

    # Obtener los datos JSON de la petición
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Petición inválida. Asegúrate de enviar un JSON con la clave "message".'}), 400

    mensaje = data['message']

    # Limpiar y predecir
    mensaje_limpio = limpiar_texto(mensaje)
    prediccion = modelo.predict([mensaje_limpio])[0]
    probabilidades = modelo.predict_proba([mensaje_limpio])[0]

    # Preparar la respuesta
    resultado = {
        'prediction': int(prediccion), # 0 para Ham, 1 para Spam
        'label': 'Spam' if int(prediccion) == 1 else 'Seguro (Ham)',
        'spam_probability': float(probabilidades[1])
    }

    return jsonify(resultado)

# --- Iniciar el servidor ---

if __name__ == '__main__':
    # En producción, el puerto lo define la variable de entorno PORT
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Iniciando servidor Flask en el puerto {port}...")
    # Usamos el puerto 5000 por convención para APIs
    app.run(host='0.0.0.0', port=port, debug=False)