class AppStateInpersonateAgent{
    constructor(){
        this._selectedAgentIdSubject= new rxjs.Subject();
        this._agentListSubject= new rxjs.Subject();
        this._conversationListSubject= new rxjs.Subject();
        this._messageListSubject= new rxjs.Subject();
        this._selectedConversationSubject= new rxjs.Subject();
        this._activatedAgentSubject= new rxjs.Subject();
    }

    //Getters
    get selectedAgentId(){
        return this._selectedAgentId;
    }

    get agentList(){
        return this._agentList;
    }

    get conversationList(){
        return this._conversationList;
    }


    get messageList(){
        return this._messageList;
    }

    get selectedConversation(){
        return this._selectedConversation;
    }

    get activatedAgent(){
        return this._activatedAgent;
    }


    //Setters
    set selectedAgentId(value){
        this._selectedAgentId= value;
        this._selectedAgentIdSubject.next(value);
    }

    set agentList(value){
        this._agentList= value;
        this._agentListSubject.next(value);
    }

    set conversationList(value){
        this._conversationList= value;
        this._conversationListSubject.next(value);
    }

    set messageList(value){
        this._messageList= value;
        this._messageListSubject.next(value);
    }

    set selectedConversation(value){
        this._selectedConversation= value;
        this._selectedConversationSubject.next(value);
    }

    set activatedAgent(value){
        this._activatedAgent= value;
        this._activatedAgentSubject.next(value);
    }

    //Changes
    onSelectedAgentIdChange(subscriber){
        this._selectedAgentIdSubject.subscribe({
            next: subscriber,
        });
    }
    
    onAgentListChange(subscriber){
        this._agentListSubject.subscribe({
            next: subscriber,
        });
    }

    onConversationListChange(subscriber){
        this._conversationListSubject.subscribe({
            next: subscriber,
        });
    }

    onMessagesListChange(subscriber){
        this._messageListSubject.subscribe({
            next: subscriber,
        });
    }

    onSelectedConversationChange(subscriber){
        this._selectedConversationSubject.subscribe({
            next: subscriber,
        });
    }

    onActivatedAgentChange(subscriber){
        this._activatedAgentSubject.subscribe({
            next: subscriber,
        });
    }

}