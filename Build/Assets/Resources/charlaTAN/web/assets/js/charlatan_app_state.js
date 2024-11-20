class AppState{
    constructor(){
        this._selectedAgentIdSubject= new rxjs.Subject();
        this._userIdSubject= new rxjs.Subject();
        this._agentListSubject= new rxjs.Subject();
        this._messageListSubject= new rxjs.Subject();
        this._conversationTreeSubject= new rxjs.Subject();
        this._selectedConversationSubject= new rxjs.Subject();
        this._selectedConversationMessagesSubject= new rxjs.Subject();
    }

    //Getters
    get selectedAgentId(){
        return this._selectedAgentId;
    }

    get userId(){
        return this._userId;
    }

    get agentList(){
        return this._agentList;
    }

    get messageList(){
        return this._messageList;
    }

    get conversationTree(){
        return this._conversationTree;
    }

    get selectedConversation(){
        return this._selectedConversation;
    }

    get selectedConversationMessages(){
        return this._selectedConversationMessages;
    }


    //Setters
    set selectedAgentId(value){
        this._selectedAgentId= value;
        this._selectedAgentIdSubject.next(value);
    }

    set userId(value){
        this._userId= value;
        this._userIdSubject.next(value);
    }

    set agentList(value){
        this._agentList= value;
        this._agentListSubject.next(value);
    }

    set messageList(value){
        this._messageList= value;
        this._messageListSubject.next(value);
    }

    set conversationTree(value){
        this._conversationTree= value;
        this._conversationTreeSubject.next(value);
    }

    set selectedConversation(value){
        this._selectedConversation= value;
        this._selectedConversationSubject.next(value);
    }

    set selectedConversationMessages(value){
        this._selectedConversationMessages= value;
        this._selectedConversationMessagesSubject.next(value);
    }

    //Changes
    onSelectedAgentIdChange(subscriber){
        this._selectedAgentIdSubject.subscribe({
            next: subscriber,
        });
    }

    onUserIdChange(subscriber){
        this._userIdSubject.subscribe({
            next: subscriber,
        });
    }
    
    onAgentListChange(subscriber){
        this._agentListSubject.subscribe({
            next: subscriber,
        });
    }

    onMessagesListChange(subscriber){
        this._messageListSubject.subscribe({
            next: subscriber,
        });
    }

    onConversationTreeChange(subscriber){
        this._conversationTreeSubject.subscribe({
            next: subscriber,
        });
    }

    onSelectedConversationChange(subscriber){
        this._selectedConversationSubject.subscribe({
            next: subscriber,
        });
    }

    onSelectedConversationMessagesChange(subscriber){
        this._selectedConversationMessagesSubject.subscribe({
            next: subscriber,
        });
    }
}