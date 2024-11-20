;(() => {
    const agentsContainer = document.getElementById("agents-bar")
    const agentListItemTemplate = agentsContainer.querySelector("li").cloneNode(true)
    agentListItemTemplate.querySelector("a").classList.remove("active")
    clearAgentsList()
    appStateInpersonateAgent.onAgentListChange(agents => {
        clearAgentsList()
        agents.forEach(addAgentToList)
        enableAgent(appStateInpersonateAgent.selectedAgentId)
    })
    appStateInpersonateAgent.onSelectedAgentIdChange(enableAgent)

    function clearAgentsList(){
        agentsContainer.innerHTML = ""
    }

    function addAgentToList(agentName){
        const agentItem = agentListItemTemplate.cloneNode(true)
        const link = agentItem.querySelector("a")
        agentItem.dataset.agentName = agentName
        link.innerText = agentName
        link.addEventListener('click', (e) => {
            e.preventDefault()
            appStateInpersonateAgent.selectedAgentId = agentName
        })
        agentsContainer.appendChild(agentItem)
    }

    function enableAgent(agentName){
        disableAllAgents()
        const item = agentsContainer.querySelector(`li[data-agent-name="${agentName}"] > a`)
        item?.classList.add("active")
    }

    function disableAllAgents(){
        const allLinks = agentsContainer.querySelectorAll("a.active")
        allLinks.forEach(element => {
            element.classList.remove("active")
        })
    }
})()