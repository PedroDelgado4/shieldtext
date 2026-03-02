// Archivo: src/App.jsx
import { useState } from 'react';
import axios from 'axios';
import './App.css';
import FloatingProfileButton from './components/FloatingProfileButton';

function App() {
  const [message, setMessage] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setResult(null);

    try {
        // Usamos una variable de entorno para la URL. Si no existe (local), usa localhost.
        const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';
        
        // Hacemos la petición a nuestra API en Flask
        const response = await axios.post(`${apiUrl}/predict`, {
          message: message
        });
        setResult(response.data);
    } catch (error) {
        console.error("Error al contactar la API:", error);
        setResult({ error: "No se pudo conectar con el servidor del modelo." });
    } finally {
        setLoading(false);
    }
  };

  return (
    // Usamos un Fragmento (<>) para devolver múltiples elementos
    <>
      <FloatingProfileButton />
      <div className="App">
        <h1>🕵️‍♂️ Spam Detector</h1>
        <p>Write a message (English only) and the system will tell you if it's safe or spam.</p>
        
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Congratulations! You've won a free trip..."
        />
        
        <button onClick={handleAnalyze} disabled={loading || !message.trim()}>
          {loading ? 'Analyzing...' : 'Analyze Message'}
        </button>

        {loading && <div className="spinner"></div>}

        {result && !result.error && (
          <div className={`result ${result.prediction === 1 ? 'spam' : 'safe'}`}>
            <p>Result: {result.label}</p>
            <p>Confidence (Spam): {(result.spam_probability * 100).toFixed(2)}%</p>
          </div>
        )}

        {result && result.error && (
          <div className="result spam">
            <p>{result.error}</p>
          </div>
        )}
      </div>
    </>
  );
}

export default App;
