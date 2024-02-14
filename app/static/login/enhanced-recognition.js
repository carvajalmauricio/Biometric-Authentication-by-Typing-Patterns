window.onload = function() {
    // Inicializa la primera frase visible y las demás ocultas
    var phrases = document.querySelectorAll('.phrase');
    for (var i = 1; i < phrases.length; i++) {
      phrases[i].classList.add('hidden');
    }
  
    // Función para manejar el evento click del botón "Listo"
    var handleButtonClick = function(event) {
      var currentPhraseIndex = parseInt(this.dataset.phrase);
      var currentPhrase = document.getElementById('phrase' + currentPhraseIndex);
      var nextPhrase = document.getElementById('phrase' + (currentPhraseIndex + 1));
  
      // Oculta la frase actual
      currentPhrase.classList.add('hidden');
  
      // Si hay una siguiente frase, la muestra
      if (nextPhrase) {
        nextPhrase.classList.remove('hidden');
      }
    };
  
    // Agregar el evento click a cada botón
    var buttons = document.querySelectorAll('button');
    buttons.forEach(function(button) {
      button.onclick = handleButtonClick;
    });
  };
  
