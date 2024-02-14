document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input[data-phrase]');
    let lastKeyPressTime = 0;
    let allTypingData = {};

    inputs.forEach(input => {
        let typingData = [];
        const phraseId = input.getAttribute('data-phrase');

        input.addEventListener('input', (event) => {
            const phraseId = input.getAttribute('data-phrase');
            const phraseDiv = document.getElementById(`phrase${phraseId}`);
            const letters = phraseDiv.querySelectorAll('.letter');
            const inputText = event.target.value;

            letters.forEach((letter, index) => {
                if (index < inputText.length && letter.textContent === inputText[index]) {
                    letter.style.color = 'red';
                } else {
                    letter.style.color = 'initial';
                }
            });
        });

        input.addEventListener('keydown', (event) => {
            const currentTime = new Date().getTime();
            const keyPressDuration = currentTime - lastKeyPressTime;
            lastKeyPressTime = currentTime;

            // Añadir datos de la tecla presionada al array
            typingData.push({
                key: event.key,
                timeSinceLastKey: keyPressDuration,
                timeStamp: currentTime
            });

            console.log(typingData); // Mostrar los datos en la consola
        });

        input.prepareData = function () {
            allTypingData[phraseId] = typingData; // Almacenar los datos de la frase en el objeto global
            if (phraseId === '2') {
                sendData();
            }
        };
    });

    function sendData() {
        fetch('/session')
            .then(response => response.json())
            .then(session => {
                let dataToSend = {"data": {[session.username]: allTypingData}};
                const jsonData = JSON.stringify(dataToSend);
                console.log(jsonData);
                fetch('/authorized', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: jsonData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Mostrar el mensaje
                    alert(data.message);
                    
                    // Redirigir si es necesario
                    if (data.redirect) {
                        window.location.href = data.redirectURL;
                    }
                })
                .catch(error => {
                    console.error('There has been a problem with your fetch operation:', error);
                });
            });
    }
    
});

