const voice = window.speechSynthesis

const TextToSpeech = {

  play(textToPlay){
    // funcion que se asocia al botón de play en el evento onClick
    if (voice.speaking) {
      voice.resume()
      return
    }
    
    const utterance = new SpeechSynthesisUtterance(textToPlay)
    utterance.voice = voice.getVoices()[4] // index 4 es la voz por defecto para español
    voice.speak(utterance)
    
  },

  pause(){
    // funcion que se asocia al botón de pause en el evento onClick
    voice.pause()
  },

  stop(){
    // funcion que se asocia al botón de stop en el evento onClick
    voice.cancel()
  },

  linkButtonActions(buttonContainer, messageToPlay){
    const stopMessageButtonTemplate = document.body.querySelector(".voice-stop-button").cloneNode(true)

    buttonContainer.querySelector(".button-play-message").addEventListener('click', (e) => {
      e.preventDefault()
      TextToSpeech.play(messageToPlay)
    })
    buttonContainer.querySelector(".button-pause-message").addEventListener('click', (e) => {
        e.preventDefault()
        TextToSpeech.pause()
    })
    buttonContainer.querySelector(".button-stop-message").addEventListener('click', (e) => {
      e.preventDefault()
      TextToSpeech.stop()
    })
  }
}
