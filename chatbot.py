
import random
import re
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from iagenerativa import generar_respuestas

app = FastAPI(title="Chatbot básico - Shena", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: List[Dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str



"""def responder(mensaje: str) -> str:
    ruta_datos = Path(__file__).with_name("datos.txt")

    try:
        with open(ruta_datos, "r", encoding="utf-8") as archivo:
            datos = archivo.read().splitlines()
        print("Datos leídos")
    except FileNotFoundError:
        datos = []
        print("No se encontró el archivo datos.txt")

    modelo = {}

    for frase in datos:
        palabras = re.findall(r"\w+", frase.lower())

        for i in range(len(palabras) - 1):
            actual = palabras[i]
            siguiente = palabras[i + 1]

            if actual not in modelo:
                modelo[actual] = []

            modelo[actual].append(siguiente)

    print("\nModelo construido")

    for palabra, siguientes in modelo.items():
        print(palabra, "->", siguientes)

    texto = mensaje.strip().lower()

    if not texto:
        return "Por favor escribe un mensaje. No puedo responder a mensajes vacíos."

    if len(texto) < 2:
        return "¿Podrías escribir un mensaje más largo? Tu mensaje es muy corto."

    if any(saludo in texto for saludo in ("hola", "buenas", "hey")):
        return "¡Hola! Soy Shena, tu asistente virtual SENA. ¿En qué puedo ayudarte?"

    if "nombre" in texto:
        return "Soy Shena, un chatbot básico hecho con Python."

    if any(palabra in texto for palabra in ("adiós", "chao", "hasta luego")):
        return "¡Hasta luego! Que tengas un buen día."

    if "ayuda" in texto:
        return "Puedo responder preguntas sobre programas, inscripciones, contacto, requisitos y contratos de aprendizaje. ¿Qué necesitas?"

    if any(palabra in texto for palabra in ("oferta", "carreras", "cursos", "que hay", "qué hay", "programas", "estudiar")):
        return (
            "Las ofertas disponibles para estudiar son:\n"
            "Tecnólogo ADSO\n"
            "Multimedia\n"
            "Animación 3D\n"
            "Desarrollo de medios visuales\n"
            "Consulta la oferta vigente en https://betowa.sena.edu.co/"
        )

    if any(palabra in texto for palabra in ("inscripciones", "fechas", "fecha", "inicio")):
        return (
            "Consulta las fechas de inscripción y las convocatorias vigentes "
            "en https://betowa.sena.edu.co/"
        )

    if any(palabra in texto for palabra in ("contacto", "telefono", "teléfono", "datos", "correo")):
        return (
            "Información de contacto registrada:\n"
            "Nombre: Claudia Marcela Estupiñán Gómez\n"
            "Rol: Coordinadora grupo de Administración Administrativa\n"
            "Correo: cmestupinan@sena.edu.co\n"
            "Centro: Centro para la Industria de la Comunicación Gráfica\n"
            "Regional: Regional Distrito Capital\n"
            "Dirección: Calle 15 No. 31-42, Bogotá D.C., Colombia"
        )

    if "contrato" in texto:
        return (
            "Aquí puedes consultar información sobre el contrato de aprendizaje:\n"
            "https://comunicaciongraficasena.blogspot.com/p/contrato-de-aprendizaje.html"
        )

    if any(palabra in texto for palabra in ("requisitos", "papel", "documentos", "diploma")):
        return (
            "Los requisitos dependen del programa y la convocatoria. "
            "Consulta la información vigente en:\n"
            "https://betowa.sena.edu.co/"
        )

    palabras_usuario = re.findall(r"\w+", texto)

    palabras_vacias = {
        "que", "qué", "como", "cómo", "es", "el", "la", "los", "las",
        "un", "una", "del", "en", "y", "a", "me", "puedes", "dime",
        "sobre", "por", "favor", "de", "se", "mi", "tu"
    }

    candidatas = [
        palabra for palabra in palabras_usuario
        if palabra in modelo and palabra not in palabras_vacias
    ]

    if not candidatas:
        return (
            "No encuentro una palabra conocida en tu consulta.\n"
            "Prueba con aprendiz, estudiante, Python, Flask, React o MySQL."
        )

    actual = candidatas[-1]
    frase_generada = [actual]

    for _ in range(7):
        if actual not in modelo or not modelo[actual]:
            break

        siguiente = random.choice(modelo[actual])
        frase_generada.append(siguiente)
        actual = siguiente

    # devolver las respuesta

    respuesta = " ".join(frase_generada)

    print("\n=== RESPUESTA GENERADA ===")
    print(respuesta)

    return "Segun los patrones de mis datos: " + respuesta
"""


@app.get("/", response_class=HTMLResponse)
def pagina() -> str:
    return HTML


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
   respuesta = await generar_respuestas(request.message)

   return ChatResponse(reply=respuesta)


HTML = r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CeniChat - Asistente CENIGRAF</title>
  <!-- Enlace al archivo CSS externo -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="/static/styles.css">
</head>
<body>

  <div class="app-container">
  <!-- Barra lateral con iconos profesionales -->
  <div class="sidebar">
    <div class="sidebar-icon active" title="Chat"><i class="fa-solid fa-comment-dots"></i></div>
    <div class="sidebar-icon" title="Programas"><i class="fa-solid fa-graduation-cap"></i></div>
    <div class="sidebar-icon" title="Requisitos"><i class="fa-solid fa-file-lines"></i></div>
    <div class="sidebar-icon" title="Ubicación"><i class="fa-solid fa-location-dot"></i></div>
    <div class="sidebar-footer">
      <div class="sidebar-icon" title="Configuración"><i class="fa-solid fa-gear"></i></div>
    </div>
  </div>

    <!-- Área principal de chat -->
    <div class="chat-area">
      <div class="chat-header">
        <div class="header-info">
          <h1>🤖 CeniChat</h1>
          <p>Asistente de información - Oferta educativa CENIGRAF</p>
        </div>
        <div class="header-actions">
          <div class="nav-links">
            <span>🏠 Inicio</span>
            <span>ℹ️ Sobre CENIGRAF</span>
            <span>🎓 Programas</span>
          </div>
          <!-- Botón para limpiar chat -->
          <button class="btn-clear" id="btnClear" onclick="clearChat()">
            🗑️ Limpiar chat
          </button>
        </div>
      </div>

      <div class="chat-body-wrapper">
        <!-- Panel de Preguntas Frecuentes -->
        <div class="faq-sidebar">
          <h3>❓ Preguntas frecuentes</h3>
          <button class="faq-btn" onclick="sendPreset('¿Qué programas ofrece CENIGRAF?')">🎓 ¿Qué programas ofrece CENIGRAF?</button>
          <button class="faq-btn" onclick="sendPreset('¿Cuáles son los requisitos de inscripción?')">📋 ¿Cuáles son los requisitos de inscripción?</button>
          <button class="faq-btn" onclick="sendPreset('¿Cómo es el proceso de matrícula?')">💳 ¿Cómo es el proceso de matrícula?</button>
          <button class="faq-btn" onclick="sendPreset('¿Dónde se encuentra CENIGRAF?')">📍 ¿Dónde se encuentra CENIGRAF?</button>
          <button class="faq-btn" onclick="sendPreset('¿Cuáles son los horarios?')">⏱️ ¿Cuáles son los horarios?</button>
        </div>

        <div style="flex: 1; display: flex; flex-direction: column;">
          <div id="chat" aria-live="polite">
            <div class="message bot">
              ¡Hola! 👋 Soy CeniChat, tu asistente virtual. Puedo ayudarte con información sobre nuestros programas, requisitos, matrícula y más. Selecciona una pregunta frecuente o escribe tu consulta.
              <div class="message-time" id="init-time"></div>
            </div>
            <!-- Indicador de respuesta -->
            <div class="typing-indicator" id="typingIndicator">
              💬 El chatbot está escribiendo...
            </div>
          </div>

          <div class="chat-input-container">
            <form id="form">
              <button type="button" class="btn-attach" title="Adjuntar archivo">📎</button>
              <input id="message" autocomplete="off" placeholder="Escribe tu mensaje..." required maxlength="2000">
              <button type="submit" class="btn-send" title="Enviar">➤</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const chat = document.querySelector('#chat');
    const form = document.querySelector('#form');
    const input = document.querySelector('#message');
    const typingIndicator = document.querySelector('#typingIndicator');

    document.getElementById('init-time').textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    function getCurrentTime() {
      return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function addMessage(sender, text) {
      const div = document.createElement('div');
      div.className = `message ${sender}`;
      
      const timeSpan = document.createElement('div');
      timeSpan.className = 'message-time';
      timeSpan.textContent = getCurrentTime();

      div.textContent = text;
      div.appendChild(timeSpan);
      
      chat.insertBefore(div, typingIndicator);
      chat.scrollTop = chat.scrollHeight;
    }

    function showTyping(show) {
      typingIndicator.style.display = show ? 'block' : 'none';
      chat.scrollTop = chat.scrollHeight;
    }

    async function sendPreset(questionText) {
      input.value = questionText;
      form.dispatchEvent(new Event('submit'));
    }

    function clearChat() {
      const messages = chat.querySelectorAll('.message');
      messages.forEach(msg => msg.remove());
      
      const welcomeDiv = document.createElement('div');
      welcomeDiv.className = 'message bot';
      welcomeDiv.innerHTML = `¡Hola! 👋 Soy CeniChat, tu asistente virtual. Puedo ayudarte con información sobre nuestros programas, requisitos, matrícula y más. Selecciona una pregunta frecuente o escribe tu consulta.<div class="message-time">${getCurrentTime()}</div>`;
      chat.insertBefore(welcomeDiv, typingIndicator);
    }

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const message = input.value.trim();
      if (!message) return;

      addMessage('user', message);
      input.value = '';
      showTyping(true);

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });

        if (!response.ok) throw new Error('No se pudo obtener una respuesta.');

        const data = await response.json();
        showTyping(false);
        addMessage('bot', data.reply);
      } catch (error) {
        showTyping(false);
        addMessage('bot', `Error: ${error.message}`);
      }
    });
  </script>
</body>
</html>
"""