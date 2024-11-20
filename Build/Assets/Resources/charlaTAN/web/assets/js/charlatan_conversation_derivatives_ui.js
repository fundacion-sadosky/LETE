;(() => {
  const container = document.getElementById("ListaPadre")
  container.innerHTML=""
  appState.onConversationTreeChange(refreshConversationTree)
  appState.onSelectedConversationChange(enableConversation)
  
  function refreshConversationTree(conversation){
    container.innerHTML=""
    if(!conversation?.children) return
    for (const child of conversation.children) {
      container.appendChild(createConversation(child))
    }  
  }
  
  function createStandaloneConversation(conversation){
    const a = document.createElement('a')

    a.style.paddingLeft='17px'
    a.href='#'
    a.innerText= `${conversation.participant1}-${conversation.participant2}`
    return a
  }
  
  function createParentConversation(conversation){
    const details = document.createElement('details')
    const summary = document.createElement('summary')
    const a = document.createElement('a')

    details.style.paddingLeft='10px'
    summary.style.marginLeft='-10px'
    a.href='#'
    a.innerText= `${conversation.participant1}-${conversation.participant2}`
    
    summary.appendChild(a)
    details.appendChild(summary)
    return [details, a]
  }
  
  function createConversation(conversation){
    let container,a
    if(conversation.children){
      const [_container, _a]= createParentConversation(conversation)
      for (const child of conversation.children) {
        _container.appendChild(createConversation(child))  
      }
      container=_container
      a=_a
    }else{
      container = a = createStandaloneConversation(conversation)
    }
    a.addEventListener('click',(e)=>{
      e.preventDefault()
      appState.selectedConversation=conversation
    })
    a.style.color="#000"
    a.style.textDecoration='none'
    a.dataset.conversationId=conversation.id
    return container
  }
  
  function enableConversation(conversation){
    disableAllConversations()
    const item = container.querySelector(`a[data-conversation-id="${conversation.id}"]`)
    if(item){
      item.style.fontWeight='bold'
    }
  }
  
  function disableAllConversations(){
    const allLinks = container.querySelectorAll("a")
    allLinks.forEach(element => {
      element.style.fontWeight='normal'
    })
  }
  
})()