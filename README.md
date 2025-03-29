# Autenticación Biométrica por Patrones de Tecleo

![Versión](https://img.shields.io/badge/versión-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Flask](https://img.shields.io/badge/Flask-3.0.1-lightblue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.0-orange)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4.0-yellow)

Un sistema avanzado de autenticación biométrica que utiliza patrones de tecleo únicos para verificar la identidad del usuario, complementando o reemplazando los métodos tradicionales de contraseña.

## 📋 Descripción

Este proyecto implementa un sistema de autenticación biométrica basado en patrones de tecleo, utilizando aprendizaje automático para identificar a los usuarios por la forma única en que escriben. A diferencia de las contraseñas tradicionales, este método:

- Mitiga ataques por diccionario y fuerza bruta
- Reduce el problema del olvido o descuido de contraseñas
- Añade una capa adicional de seguridad basada en características biométricas
- Se adapta al comportamiento del usuario con el tiempo

El sistema analiza múltiples características del patrón de escritura como:
- Tiempo entre pulsaciones de teclas
- Uso de teclas especiales (Shift, CapsLock)
- Patrones de velocidad al escribir
- Consistencia al escribir frases específicas
- Distancia de Levenshtein entre la frase objetivo y la escrita

## 🔧 Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: scikit-learn, TensorFlow, RandomForestClassifier
- **Email**: SendGrid
- **Almacenamiento**: Archivos JSON

## 🚀 Instalación

### Prerrequisitos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno

### Pasos de instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/Biometric-Authentication-by-Typing-Patterns.git
   cd Biometric-Authentication-by-Typing-Patterns
   ```

2. Crear y activar un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   # En macOS/Linux
   source venv/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar las variables de entorno para SendGrid (opcional para emails):
   ```bash
   # En Windows
   set SENDGRID_API_KEY=tu_api_key
   # En macOS/Linux
   export SENDGRID_API_KEY=tu_api_key
   ```

5. Ejecutar la aplicación:
   ```bash
   python -m app
   ```

## 💻 Uso

1. Acceder a la aplicación a través de http://localhost:5000/
2. Registrarse como nuevo usuario o iniciar sesión
3. Durante la fase de registro, se le pedirá que escriba varias frases para capturar su patrón de tecleo
4. Para iniciar sesión, además de su nombre de usuario, deberá escribir frases de verificación
5. El sistema validará su identidad analizando su patrón de tecleo

## 🌟 Características Principales

- **Registro de usuarios**: Captura del perfil biométrico inicial
- **Autenticación biométrica**: Verificación de patrones de tecleo
- **Análisis de comportamiento**: Métricas avanzadas para identificación
- **Seguridad adicional**: Verificación de dispositivo y navegador
- **Alertas de seguridad**: Notificación por email cuando se detectan anomalías

## 🔍 Cómo Funciona

1. **Recolección de datos**: Durante el registro y el inicio de sesión, el sistema captura métricas como el tiempo entre pulsaciones, uso de teclas especiales, etc.
2. **Preprocesamiento**: Los datos se transforman en vectores de características
3. **Modelado**: Se utiliza RandomForestClassifier para crear un modelo predictivo
4. **Verificación**: Durante el inicio de sesión, el patrón actual se compara con el modelo del usuario

## 🧪 Evaluación del Modelo

El sistema utiliza validación cruzada para optimizar los hiperparámetros del modelo y garantizar una alta precisión en la identificación de usuarios. El modelo final es evaluado con datos de prueba separados.

## 🛡️ Consideraciones de Seguridad

- El sistema almacena patrones biométricos, no contraseñas tradicionales
- Se implementa verificación de IP y navegador para añadir seguridad
- Las sesiones tienen un tiempo de vida limitado
- Se utilizan técnicas para prevenir ataques de repetición

## 📚 Estructura del Proyecto

```
/
├── app/                    # Aplicación principal
│   ├── static/             # Archivos estáticos (JS, CSS)
│   │   ├── login/          # Scripts de reconocimiento
│   │   ├── phrases/        # Frases para verificación
│   │   └── users/          # Datos de usuarios
│   ├── templates/          # Plantillas HTML
│   ├── __init__.py         # Inicialización de la aplicación
│   ├── fitting_model.py    # Entrenamiento del modelo
│   ├── login.py            # Rutas de inicio de sesión
│   ├── model_preprocessing.py  # Preprocesamiento para el modelo
│   ├── privileges.py       # Control de acceso
│   ├── send_message.py     # Envío de alertas por email
│   └── verificate_user.py  # Verificación de usuarios
├── best_model.pkl          # Modelo de ML entrenado
├── data.json               # Datos de patrones de tecleo
├── data_with_features.json # Datos procesados con características
├── phrases.json            # Frases de verificación
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
```

## 🔄 Flujo de Autenticación

1. El usuario ingresa su nombre de usuario
2. El sistema verifica la IP y el navegador
3. Si son desconocidos, se activa una verificación adicional
4. Se presentan frases aleatorias para que el usuario las escriba
5. El sistema captura el patrón de escritura y lo compara con el modelo
6. Si coincide, el acceso es concedido; de lo contrario, se solicita verificación adicional

## 📝 Licencia

Este proyecto está licenciado bajo [tu licencia] - ver el archivo LICENSE para más detalles.

## 🔮 Mejoras Futuras

- Integración con sistemas de autenticación de dos factores
- Mejora del algoritmo mediante redes neuronales profundas
- Análisis de comportamiento continuo durante las sesiones
- Soporte para múltiples idiomas y disposiciones de teclado
- Adaptación a dispositivos móviles y pantallas táctiles

## 📞 Contacto

Para preguntas o sugerencias, contacta a [tu correo o información de contacto].

---

**Nota**: Este sistema está diseñado como una capa adicional de seguridad y no debe ser el único método de autenticación en sistemas críticos.
