;(() => {
    setTitle("")
    const chatMessages = document.body.querySelector(".chat-column.chat-window.agents-chat")
    const userMessageTemplate = chatMessages.querySelector(".from-me").cloneNode(true)
    const agentMessageTemplate = chatMessages.querySelector(".from-them").cloneNode(true)
    clearChatMessages()
    appState.onSelectedConversationChange(changeChatTitleConversationName)
    appState.onSelectedConversationMessagesChange(refreshMessageList)

    function clearChatMessages(){
        chatMessages.innerHTML = ""
    }

    function setTitle(title){
        const chatTitle = document.body.querySelector("#Encabezado-4 > p")
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
        const isInitialScrollHeight = chatMessages.scrollHeight === chatMessages.clientHeight

        clearChatMessages()
        for (const message of messageList) {
            let chatMessage
            if (message.sender === appState.selectedConversation.participant1){
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
            chatMessages.appendChild(chatMessage)
        }
        if(isInitialScrollHeight || chatMessages.scrollTop + chatMessages.clientHeight >= chatMessages.scrollHeight - 20) 
            chatMessages.scrollTo(0,chatMessages.scrollHeight)
    }

})()