;(() => {
    setTitle("")
    const chatMessages = document.body.querySelector(".chat-column.chat-window:not(.agents-chat)")
    const userMessageTemplate = chatMessages.querySelector(".from-me").cloneNode(true)
    const agentMessageTemplate = chatMessages.querySelector(".from-them").cloneNode(true)
    const form = document.getElementById("form-send-text-1")
    const messageInput = document.getElementById("input-message-1")
    const button = document.getElementById("button-message-1")

    clearChatMessages()
    if(!appState.selectedAgentId){
        button.disabled = true
        messageInput.disabled = true
    }
    appState.onSelectedAgentIdChange(changeChatTitleAgentName)
    appState.onSelectedAgentIdChange( () => {
        button.disabled = false
        messageInput.disabled = false
    })
    appState.onMessagesListChange(refreshMessageList)
    form.addEventListener('submit', (e) => {
        e.preventDefault()
        sendMessage(messageInput.value)
        messageInput.value = ""
    })

    function clearChatMessages(){
        chatMessages.innerHTML = ""
    }

    function setTitle(title){
        const chatTitle = document.body.querySelector("#Encabezado-2 > p")
        chatTitle.innerText = title
    }

    function changeChatTitleAgentName(agentName){
        setTitle(`Chat con ${agentName}`)
    }

    function refreshMessageList(messageList){
        clearChatMessages()
        for (const message of messageList) {
            let chatMessage
            if (message.sender === appState.selectedAgentId){
                chatMessage = agentMessageTemplate.cloneNode(true)
            }else{
                chatMessage = userMessageTemplate.cloneNode(true)
            }
            if(message.text){
                chatMessage.querySelector("p").innerText = message.text
                TextToSpeech.linkButtonActions(chatMessage.querySelector(".container-button"), message.text)
            }else if(message.image){
                chatMessage.querySelector("p").innerHTML = `<img src="${message.image}" style="width: 100%"/>`
            }else{
                chatMessage.querySelector("p").innerHTML = "<i>Unsupported message</i>"
            }
            const div = document.createElement("div")
            div.style.fontSize = "0.8em"
            div.style.marginTop = "-12px"
            div.style.padding = "0 9px"
            div.style.fontStyle = "italic"
            div.style.opacity = "0.6"
            div.innerText = dayjs.unix(message.timestamp).format("DD/MM/YYYY HH:mm:ss")
            chatMessages.appendChild(chatMessage)
            chatMessage.appendChild(div)
        }
        chatMessages.scrollTo(0,chatMessages.scrollHeight)
    }

    async function sendMessage(message){
        const response = await backendLocalCharlatan.sendMessageToAgent(message, appState.userId, appState.selectedAgentId)
    }

})()