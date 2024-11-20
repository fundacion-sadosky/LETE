;(() => {
    setTitle("")
    const chatMessages = document.getElementById("chat-column-user-agent")
    const userMessageTemplate = chatMessages.querySelector(".from-me").cloneNode(true)
    const agentMessageTemplate = chatMessages.querySelector(".from-them").cloneNode(true)
    clearChatMessages()
    const form = document.getElementById("form-send-text")
    const messageInput = document.getElementById("input-message")
    const button = document.getElementById("button-message")
    appStateInpersonateAgent.onSelectedConversationChange(changeChatTitleConversationName)
    appStateInpersonateAgent.onMessagesListChange(refreshMessageList)
    form.disabled = true
    messageInput.disabled = true
    button.disabled = true
    appStateInpersonateAgent.onActivatedAgentChange(() => {
        form.disabled = appStateInpersonateAgent.activatedAgent
        messageInput.disabled = appStateInpersonateAgent.activatedAgent
        button.disabled = appStateInpersonateAgent.activatedAgent
    })
    form.addEventListener('submit', (e) => {
        e.preventDefault()
        sendMessage(messageInput.value)
        messageInput.value = ""
    })

    function clearChatMessages(){
        chatMessages.innerHTML = ""
    }

    function setTitle(title){
        const chatTitle = document.body.querySelector("#Encabezado-3 > p")
        chatTitle.innerText = title
    }

    function changeChatTitleConversationName(conversation){
        if(!conversation.participant1||!conversation.participant2) {
            setTitle('')
        }else{
        setTitle(`${conversation.participant1}-${conversation.participant2}`)
        }
    }

    function refreshMessageList(messageList){
        clearChatMessages()
        for (const message of messageList) {
            let chatMessage
            if (!(message.sender === appStateInpersonateAgent.selectedAgentId)){
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
        if (!_.isEmpty(appStateInpersonateAgent.selectedConversation)){
            const response = await backendLocalCharlatan.sendMessageToAgentSkippingFlow(message)
        }
    }

})()