;(() => {
    let cssJsDelivr = document.createElement("link");
    cssJsDelivr.setAttribute("type", "text/css");
    cssJsDelivr.setAttribute("rel", "stylesheet");
    cssJsDelivr.setAttribute("href", "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css");
    document.head.appendChild(cssJsDelivr);

    let cssFontGoogleApi = document.createElement("link");
    cssFontGoogleApi.setAttribute("type", "text/css");
    cssFontGoogleApi.setAttribute("rel", "stylesheet");
    cssFontGoogleApi.setAttribute("href", "https://fonts.googleapis.com/css?family=Cookie");
    document.head.appendChild(cssFontGoogleApi);

    let cssCloudFlare = document.createElement("link");
    cssFontGoogleApi.setAttribute("type", "text/css");
    cssCloudFlare.setAttribute("rel", "stylesheet");
    cssCloudFlare.setAttribute("href", "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css");
    document.head.appendChild(cssCloudFlare);

    let scriptDayjs = document.createElement("script");
    scriptDayjs.setAttribute("type", "text/javascript");
    scriptDayjs.setAttribute("src", "https://unpkg.com/dayjs@1.8.21/dayjs.min.js");
    document.head.appendChild(scriptDayjs);

    let scriptCharlatanBackend = document.createElement("script");
    scriptCharlatanBackend.setAttribute("type", 'text/javascript');
    scriptCharlatanBackend.setAttribute("src", "./assets/js/charlatan_backend.js");
    document.head.appendChild(scriptCharlatanBackend);

    let cssChatFlotanteStyles = document.createElement("link");
    cssChatFlotanteStyles.setAttribute("type", "text/css");
    cssChatFlotanteStyles.setAttribute("rel", "stylesheet");
    cssChatFlotanteStyles.setAttribute("href", "./assets/css/chat_flotante.css");
    document.head.appendChild(cssChatFlotanteStyles);

    let divAgentsWidget = document.createElement("div");
    divAgentsWidget.setAttribute("id", "agents-widget");
    document.body.appendChild(divAgentsWidget);

    let divContenedor = document.createElement("div");
    divContenedor.setAttribute("id", "contenedor");
    divContenedor.classList.add("charlatan-chat-window-conteiner");
    divAgentsWidget.appendChild(divContenedor);

    let divAgentNavBar = document.createElement("div");
    divAgentNavBar.classList.add("charlatan-agent-navbar");
    divContenedor.appendChild(divAgentNavBar);

    let pTituloContainer = document.createElement("p");
    pTituloContainer.textContent = "Chat con Agente Minorista";
    pTituloContainer.setAttribute("id", "titulo-contenedor");
    pTituloContainer.classList.add("charlatan-chat-window-header");
    divAgentNavBar.appendChild(pTituloContainer);

    let buttonMiniClose = document.createElement("button");
    buttonMiniClose.setAttribute("id", "modal-button-chat-off-1");
    buttonMiniClose.setAttribute("type", "button");
    buttonMiniClose.classList.add("btn", "btn-primary", "charlatan-modal-button-chat-off-mini");
    divAgentNavBar.appendChild(buttonMiniClose);

    let divChatWindowCol = document.createElement("div");
    divChatWindowCol.setAttribute("id", "chat-window-column");
    divChatWindowCol.classList.add("col-md-3", "charlatan-chat-window-column");
    divContenedor.appendChild(divChatWindowCol);

    let divContenedorMensajes = document.createElement("div");
    divContenedorMensajes.setAttribute("id", "contenedor-mensajes");
    divContenedorMensajes.classList.add("charlatan-chat-column", "charlatan-chat-window-log");
    divChatWindowCol.appendChild(divContenedorMensajes);

    let divChatWindowMe = document.createElement("div");
    divChatWindowMe.classList.add("charlatan-chat-window-from-me");
    divContenedorMensajes.appendChild(divChatWindowMe);

    let pChat = document.createElement("p");
    pChat.setAttribute("id", "human-message");
    divChatWindowMe.appendChild(pChat);

    let br1 = document.createElement("br");
    pChat.appendChild(br1);

    let br2 = document.createElement("br");
    pChat.textContent = "xddddddddddddddddddddddddddddddddddddddd";
    br1.appendChild(br2);

    let divChatWindowThem = document.createElement("div");
    divChatWindowThem.classList.add("charlatan-chat-window-from-them");
    divContenedorMensajes.appendChild(divChatWindowThem);

    let pChatThem = document.createElement("p");
    pChatThem.setAttribute("id", "agent-message-x");
    divChatWindowThem.appendChild(pChatThem);

    let br1Them = document.createElement("br");
    pChatThem.appendChild(br1Them);

    let br2Them = document.createElement("br");
    pChatThem.textContent = "xddddddddddddddddddddddddddddddddddddddd";
    br1Them.appendChild(br2Them);


    let divInputButton = document.createElement("div");
    divInputButton.setAttribute("id", "input-and-button");
    divInputButton.classList.add("charlatan-input-message");
    divChatWindowCol.appendChild(divInputButton);

    let formSendText = document.createElement("form");
    formSendText.setAttribute("id", "form-send-text");
    formSendText.setAttribute("autocomplete", "off");
    formSendText.style.display = "inline-flex";
    formSendText.style.width = "100%";
    divInputButton.appendChild(formSendText);

    let inputText = document.createElement("input");
    inputText.setAttribute("id", "input-message");
    inputText.setAttribute("type", "text");
    inputText.classList.add("charlatan-form-control", "charlatan-text-input");
    formSendText.appendChild(inputText);

    let buttonSendText = document.createElement("button");
    buttonSendText.setAttribute("id", "button-message");
    buttonSendText.setAttribute("type", "submit");
    buttonSendText.classList.add("btn", "btn-primary", "charlatan-buttom-text-input");
    formSendText.appendChild(buttonSendText);

    let buttonOpenChat = document.createElement("button");
    buttonOpenChat.setAttribute("id", "modal-button-chat");
    buttonOpenChat.setAttribute("type", "button");
    buttonOpenChat.classList.add("btn", "btn-primary", "charlatan-modal-button-chat");
    divAgentsWidget.appendChild(buttonOpenChat);

    let buttonCloseChat = document.createElement("button");
    buttonCloseChat.setAttribute("id", "modal-button-chat-off");
    buttonCloseChat.setAttribute("type", "button");
    buttonCloseChat.classList.add("btn", "btn-primary", "charlatan-modal-button-chat-off");
    divAgentsWidget.appendChild(buttonCloseChat);

    let scriptBootstrap = document.createElement("script");
    scriptBootstrap.type = 'text/javascript';
    scriptBootstrap.src = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js";
    document.head.appendChild(scriptBootstrap);

    let scriptChatFlotante = document.createElement("script");
    scriptChatFlotante.setAttribute("type", 'text/javascript');
    scriptChatFlotante.setAttribute("src", "./assets/js/chat-flotante.js");
    document.head.appendChild(scriptChatFlotante);
})()