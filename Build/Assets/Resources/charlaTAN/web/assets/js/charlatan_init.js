;(async () => {
    if(localStorage.getItem("userId")){
        appState.userId = localStorage.getItem("userId")
    }else{
        appState.userId = uuidv4()
        localStorage.setItem("userId", appState.userId)
    }

    appState.onSelectedAgentIdChange(() => {
        appState.messageList = []
        appState.selectedConversation={}
        appState.conversationTree={}
        appState.selectedConversationMessages=[]
        localStorage.setItem("latestAgentId", appState.selectedAgentId)
    })

    appState.onAgentListChange((list) => {
        const latestAgentId = localStorage.getItem("latestAgentId")
        if(latestAgentId && list?.includes(latestAgentId)){
            appState.selectedAgentId = latestAgentId
        }
    })

    appState.messageList = []
    appState.onSelectedAgentIdChange(refreshConversationsTree)
    setInterval(refreshConversationsTree, 2500)
    appState.onSelectedConversationChange(refreshSelectedConversationChatMessages)
    setInterval(refreshSelectedConversationChatMessages, 2500)
    appState.onSelectedAgentIdChange(refreshMessageList)
    setInterval(refreshMessageList, 2500)
    appState.agentList = await backendLocalCharlatan.getAgentsCharlatan()
    document.body.style.display = "block"

    async function refreshConversationsTree(){
        if(!appState.selectedAgentId || !appState.userId) return
        const [conversationId] = await backendLocalCharlatan.getIdConversation(appState.userId,appState.selectedAgentId)
        const {conversations}= await backendLocalCharlatan.getAssociatedConversations(conversationId)
        appState.conversationTree = mapConversationListToTree(conversations,conversationId) 
    }

    async function refreshSelectedConversationChatMessages(){
        if(!appState.selectedConversation?.id) return
        const messages = await backendLocalCharlatan.getConversationMessages(appState.selectedConversation.id, appState.selectedConversationMessages.length > 0 ? appState.selectedConversationMessages[appState.selectedConversationMessages.length - 1].timestamp : null)
        appState.selectedConversationMessages = [...appState.selectedConversationMessages, ...messages]
    }

    async function refreshMessageList(){
        const [conversationId] = await backendLocalCharlatan.getIdConversation(appState.userId,appState.selectedAgentId)
        const messages = await backendLocalCharlatan.getConversationMessages(conversationId, appState.messageList.length > 0 ? appState.messageList[appState.messageList.length - 1].timestamp : null)
        appState.messageList = [...appState.messageList, ...messages]
    }
})()