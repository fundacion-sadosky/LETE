;(() => {
    const conversationsContainer = document.getElementById("agents-bar-1")
    const conversationsListItemTemplate = conversationsContainer.querySelector("li").cloneNode(true)
    conversationsListItemTemplate.querySelector("a").classList.remove("active")
    clearConversationsList()
    appStateInpersonateAgent.onConversationListChange(conversations => {
        clearConversationsList()
        conversations.forEach(addconversationsToList)
        enableConversation(appStateInpersonateAgent.selectedConversation)
    })
    appStateInpersonateAgent.onSelectedConversationChange(enableConversation)

    function clearConversationsList(){
        conversationsContainer.innerHTML = ""
    }

    function addconversationsToList(conversation){
        const agentItem = conversationsListItemTemplate.cloneNode(true)
        const link = agentItem.querySelector("a")
        agentItem.dataset.conversationName = `${conversation.participant1}-${conversation.participant2}`
        link.innerText = `${conversation.participant1}-${conversation.participant2}`
        link.addEventListener('click', (e) => {
            e.preventDefault()
            appStateInpersonateAgent.selectedConversation = conversation
        })
        conversationsContainer.appendChild(agentItem)
    }

    function enableConversation(conversation){
        disableAllAgents()
        const item = conversationsContainer.querySelector(`li[data-conversation-name="${conversation?.participant1}-${conversation?.participant2}"] > a`)
        item?.classList.add("active")
    }

    function disableAllAgents(){
        const allLinks = conversationsContainer.querySelectorAll("a.active")
        allLinks.forEach(element => {
            element.classList.remove("active")
        })
    }
})()