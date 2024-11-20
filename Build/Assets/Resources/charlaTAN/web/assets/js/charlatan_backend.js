class CharlatanBackend {
  constructor(urlBaseCharltan){
    this.urlBaseApiCharlatan = urlBaseCharltan;
  }

  async getAgentsCharlatan(){
    const response = await fetch(`${this.urlBaseApiCharlatan}/webhooks/rest/get_agents`)
    if (response.ok) {
      const jsonValueAgents = await response.json();
      return jsonValueAgents['agents'];
    } else {
      throw new Error('Error getting agents.');
    }
  }

  async sendMessageToAgent(message, userId, agentId){
    const url = `${this.urlBaseApiCharlatan}/webhooks/rest/webhook/?receiver=${agentId}`
    const response = await fetch(url,{method:'POST', body: JSON.stringify({message, sender: userId})})
    if (response.ok) {
      const jsonResponse = await response.json();
      return jsonResponse.map(backendMessage => ({
        sender: agentId,
        receiver: backendMessage.recipient_id,
        text: backendMessage.text,
        image: backendMessage.image,
        timestamp: Date.now()/1000
      }));
    } else {
      throw new Error(`Error getting response from ${agentId}.`);
    }
  }

  async getIdConversation(participant1, participant2){
    const response = await fetch(`${this.urlBaseApiCharlatan}/conversations/conversation-id/?participant1=${participant1}&participant2=${participant2}`)
    if (response.ok) {
      const jsonIdConversation = await response.json();
      return jsonIdConversation.conversations
    } else {
      throw new Error('Error getting id conversation.');
    }
  }

  async getConversations(){
    const response = await fetch(`${this.urlBaseApiCharlatan}/conversations/`)
    if (response.ok) {
      const jsonConversations = await response.json();
      return jsonConversations.conversations
    } else {
      throw new Error('Error getting conversations.');
    }
  }

  async getConversationsParticipant(participant){
    const response = await fetch(`${this.urlBaseApiCharlatan}/conversations/${participant}`)
    if (response.ok) {
      const jsonConversations = await response.json();
      return jsonConversations.conversations
    } else {
      throw new Error('Error getting conversations.');
    }
  }

  async getConversationMessages(idConversation, latestMessageTimestamp){
    const response = await fetch(`${this.urlBaseApiCharlatan}/conversations/${idConversation}/messages/${latestMessageTimestamp ? `?timestamp=${latestMessageTimestamp}` : "" }`)
    if (response.ok) {
      const jsonConversation = await response.json();
      const messages = jsonConversation['messages']
      return messages
    } else {
      throw new Error('Error getting conversation.');
    }
  }

  async getAssociatedConversations(idConversation){
    const response = await fetch(`${this.urlBaseApiCharlatan}/conversations/${idConversation}/associated`)
    if (response.ok) {
      const jsonAssociatedConversation = await response.json();
      return jsonAssociatedConversation
    } else {
      throw new Error('Error getting conversation.');
    }
  }

  async deactivateAgent(agentName){
    const response = await fetch(`${this.urlBaseApiCharlatan}/deactivate_agent/?agent_name=${agentName}`,{method:'POST'})
    if (!response.ok) {
      throw new Error(`Error deactivating an agent ${agentName}`)
    }
  }

  async activateAgent(agentName){
    const response = await fetch(`${this.urlBaseApiCharlatan}/activate_agent/?agent_name=${agentName}`,{method:'POST'})
    if (!response.ok) {
      throw new Error(`Error activating an agent ${agentName}`)
    }
  }

  async sendMessageToAgentSkippingFlow(message){
    const url = `${this.urlBaseApiCharlatan}/webhooks/rest/register-message/?receiver=${appStateInpersonateAgent.selectedAgentId}&conversation=${appStateInpersonateAgent.selectedConversation.id}`    
    const response = await fetch(url,{method:'POST', body: JSON.stringify({message, sender: appStateInpersonateAgent.selectedAgentId})})
    if (!response.ok) {
      throw new Error(`Error al enviar el mensaje para que se registre en el agente ${appStateInpersonateAgent.selectedAgentId}.`);
    }
  }

}
