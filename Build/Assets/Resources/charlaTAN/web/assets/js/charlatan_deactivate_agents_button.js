;(() => {
    const buttonDeactivate = document.body.querySelector(".btn.btn-primary.modal-button-chat-off")
    const buttonActivete = document.body.querySelector(".btn.btn-primary.modal-button-chat-activate")
    const column = buttonActivete.parentNode
    const texto = document.createElement("span")
    texto.innerText = "activado"
    texto.style.marginLeft = "5px"
    column.appendChild(texto)
    buttonActivete.addEventListener('click', (e) => {
        e.preventDefault()
        appStateInpersonateAgent.activatedAgent = true
    })
    buttonDeactivate.addEventListener('click', (e) => {
        e.preventDefault()
        appStateInpersonateAgent.activatedAgent = false
    })
    appStateInpersonateAgent.onActivatedAgentChange(() =>{
        if (appStateInpersonateAgent.activatedAgent){
            backendLocalCharlatan.activateAgent(appStateInpersonateAgent.selectedAgentId)
            buttonDeactivate.style.display = "inline-block"
            buttonActivete.style.display = "none"
            texto.innerText = "Activado"
        }
        else{
            backendLocalCharlatan.deactivateAgent(appStateInpersonateAgent.selectedAgentId)
            buttonDeactivate.style.display = "none"
            buttonActivete.style.display = "inline-block"
            texto.innerText = "Desactivado"
        }
    })
})()