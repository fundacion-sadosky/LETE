;(() => {
    let userId
    if(localStorage.getItem("userId")){
        userId = localStorage.getItem("userId")
    }else{
        userId = uuidv4()
        localStorage.setItem("userId", userId)
    }
    const backendLocalCharlatan = new CharlatanBackend('http://localhost:5012'); //Cambiar a IP publica
    const agentId = "minorista" //Se debe extraer de otro lado el nombre del agente
    const title =  document.getElementById("titulo-contenedor")
    title.innerHTML = `Chat con ${agentId}`
    let messageList = []
    const chat = document.querySelector(".charlatan-chat-window-conteiner");
    const btnOpen = document.getElementById("modal-button-chat");
    const chatMessages = document.body.querySelector(".chat-column.chat-window-log");
    const userMessageTemplate = chatMessages.querySelector(".from-me").cloneNode(true)
    const agentMessageTemplate = chatMessages.querySelector(".from-them").cloneNode(true)
    
    btnOpen.addEventListener('click', (async (e) => { 
        e.preventDefault()
        await loadMessage();
        refreshMessageList()
        chat.style.display = "flex";
        btnOpen.style.display = "none"
        btnClose.style.display = "flex";
        const sb = document.querySelector(".chat-window-log");
        sb.scrollTop = sb.scrollHeight;
    }));

    const btnClose = document.getElementById("modal-button-chat-off");
    btnClose.addEventListener('click', ((e) => { 
        e.preventDefault()
        chat.style.display = "none";
        btnOpen.style.display = "inline-block";
        btnClose.style.display = "none";        
    }));
    const btnCloseMini = document.getElementById("modal-button-chat-off-1");
    btnCloseMini.addEventListener('click', ((e) => { 
        e.preventDefault()
        chat.style.display = "none";
        btnOpen.style.display = "inline-block";
        btnClose.style.display = "none";
    }));

    const btnForm = document.getElementById("form-send-text");
    const messageInput = document.getElementById("input-message")
    btnForm.addEventListener('submit', ((e) => { 
        e.preventDefault(); 
        sendMessage(messageInput.value)
        messageInput.value = ""
    }));
    
    async function loadMessage() {
        const [conversationId] = await backendLocalCharlatan.getIdConversation(userId, agentId)
        const messages = await backendLocalCharlatan.getConversationMessages(conversationId, messageList.length > 0 ? messageList[messageList.length - 1].timestamp : null)
        messageList = [...messageList, ...messages]
    }

    function clearChatMessages(){
        chatMessages.innerHTML = "";
    }

    async function sendMessage(message){
        const response = await backendLocalCharlatan.sendMessageToAgent(message, userId, agentId)
        await loadMessage()
        refreshMessageList()
    }

    function refreshMessageList(){
        clearChatMessages()
        console.log(messageList)
        for (const message of messageList) {
            let chatMessage
            if (message.sender === agentId){
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
            div.style.fontSize = "0.65em"
            div.style.marginTop = "-12px"
            div.style.padding = "10px 9px 0px"
            div.style.fontStyle = "italic"
            div.style.opacity = "0.6"
            div.innerText = dayjs.unix(message.timestamp).format("DD/MM/YYYY HH:mm:ss")
            chatMessages.appendChild(chatMessage)
            chatMessage.appendChild(div)
        }
        chatMessages.scrollTo(0,chatMessages.scrollHeight)
    }

})()
