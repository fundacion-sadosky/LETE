function mapConversationListToTree(conversationList, rootId){
  const conversationTree = new Map(conversationList.map(conversation => [conversation.id, {...conversation}]))
  for (const conversation of conversationList) {
    if (!conversation.parent_conversation)continue
    const parentConversation = conversationTree.get(conversation.parent_conversation)
    if (!parentConversation && conversation.id!==rootId){
      throw new Error('Padre erroneo de una conversacion')
    }
    if(!parentConversation.children){
      parentConversation.children = []
    }
    parentConversation.children.push(conversationTree.get(conversation.id))
  }
  return conversationTree.get(rootId)
}