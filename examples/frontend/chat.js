// Selecciona los elementos del DOM
const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const usernameDialog = document.getElementById('db-dialog');
const usernameInput = document.getElementById('db-input');
const confirmUsernameButton = document.getElementById('db-username');
const chatContainer = document.getElementById('chat-container');

let username = '';

// Función para agregar mensajes al chat
function addMessageToChat(message, className) {
    const p = document.createElement('p');
    p.className = className;
    p.textContent = message;
    messagesDiv.appendChild(p);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll al final del chat
}

// Función para mostrar el cuadro de diálogo del nombre de usuario
function showUsernameDialog() {
    usernameDialog.style.display = 'flex';
}

// Función para ocultar el cuadro de diálogo y mostrar el chat
function hideUsernameDialog() {
    usernameDialog.style.display = 'none';
    chatContainer.style.display = 'block';
}

// Evento de clic en el botón "Confirmar" para el nombre de usuario
confirmUsernameButton.addEventListener('click', () => {
    const enteredUsername = usernameInput.value.trim();

    if (enteredUsername) {
        const initdb = enteredUsername; // Guardamos el nombre de usuario
        const requestBody = {
            Item: initdb
        }
        fetch('http://127.0.0.1:8080/init_item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        }).then((response) => {
            if (!response.ok) {  // Verifica si la respuesta no fue exitosa (status >= 400)
                return response.json().then(err => {
                    throw new Error(`Error ${response.status}: ${err.detail || 'Error desconocido'}`);
                });
            }
            return response.json();
        })  // convertir a json
            .then((json) => {
                hideUsernameDialog()
                localStorage.setItem('db', initdb)
                addMessageToChat(`Conexion establesida a la base de datos: ${json.payload}`, 'api-response');
            })    //imprimir los datos en la consola
            .catch((err) => {
                console.log('Solicitud fallida', err)
                alert('Error en la conexios revisa que el url este bien')
            }); // Capturar errores

    }
});

// Evento de clic en el botón "Enviar"
sendButton.addEventListener('click', async () => {
    const message = messageInput.value;

    if (message.trim() === '') {
        return; // Si el mensaje está vacío, no hacemos nada
    }

    // Agregar el mensaje del usuario al chat
    addMessageToChat(`${username}: ${message}`, 'user-message');

    // Limpiar el input después de enviar el mensaje
    messageInput.value = '';

    // Crear el cuerpo de la solicitud
    const requestBody = {
        Item: localStorage.getItem('db'),
        q: message
    };

    try {
        // Enviar el mensaje al endpoint '/inference' usando fetch
        const response = await fetch('http://127.0.0.1:8080/inference', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        // Verificar si la respuesta es exitosa
        if (response.ok) {
            const jsonResponse = await response.json();
            const apiResponse = jsonResponse.res; // Suponiendo que el backend devuelve una respuesta en el campo "response"
            const sql_query_generated = jsonResponse.sql_query_generated
            // Agregar la respuesta de la API al chat
            addMessageToChat(`Respuesta: ${JSON.stringify(apiResponse)}`, 'api-response');
            addMessageToChat(`Consulta SQL generada: ${sql_query_generated}`, 'api-response');

        } else {
            addMessageToChat('Error al conectarse con la API', 'api-response');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('Error al enviar el mensaje', 'api-response');
    }
});

// Mostrar el cuadro de diálogo del nombre de usuario al cargar la página
showUsernameDialog();
