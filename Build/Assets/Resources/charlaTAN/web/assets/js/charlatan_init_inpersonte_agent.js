;(async () => {
    appStateInpersonateAgent.onSelectedAgentIdChange(async () => {
        appStateInpersonateAgent.messageList = []
        appStateInpersonateAgent.selectedConversation={}
        localStorage.setItem("latestAgentId", appStateInpersonateAgent.selectedAgentId)
        const conversationListAgent = await conversationsAgent(appStateInpersonateAgent.selectedAgentId)
        appStateInpersonateAgent.conversationList = conversationListAgent
        appStateInpersonateAgent.activatedAgent = true
    })

    appStateInpersonateAgent.onAgentListChange((list) => {
        const latestAgentId = localStorage.getItem("latestAgentId")
        if(latestAgentId && list?.includes(latestAgentId)){
            appStateInpersonateAgent.selectedAgentId = latestAgentId
        }
    })

    appStateInpersonateAgent.messageList = []
    appStateInpersonateAgent.conversationList = []
    appStateInpersonateAgent.agentList = await backendLocalCharlatan.getAgentsCharlatan()
    appStateInpersonateAgent.onSelectedConversationChange(() =>{
        appStateInpersonateAgent.messageList = []
        refreshSelectedConversationChatMessages()
    })
    setInterval(refreshSelectedConversationChatMessages, 2500)
    setInterval(()=> {appStateInpersonateAgent.activatedAgent = appStateInpersonateAgent.activatedAgent}, 90000)
    document.body.style.display = "block"

    async function conversationsAgent(agentName){
        const conversations = await backendLocalCharlatan.getConversationsParticipant(agentName)
        return conversations
    }

    async function refreshSelectedConversationChatMessages(){
        if(!appStateInpersonateAgent.selectedConversation?.id) return
        const messages = await backendLocalCharlatan.getConversationMessages(appStateInpersonateAgent.selectedConversation.id, appStateInpersonateAgent.messageList.length > 0 ? appStateInpersonateAgent.messageList[appStateInpersonateAgent.messageList.length - 1].timestamp : null)
        appStateInpersonateAgent.messageList = [...appStateInpersonateAgent.messageList, ...messages]
    }
})()