import uuid
from typing import Optional, List, Text

from matplotlib.cbook import flatten
from conversation.conversation_dto import ConversationDTO


class ConversationManager:
    def get_or_create_conversation_id(self, participant1: Text, participant2: Text, parent_conversation: Text) -> str:
        raise NotImplementedError('Necesita ser implementada la manera de obtener el id de una conversacion segun sus participantes y su conversacion padre')

    def get_children(self, parent_conversation_id: Text) -> List[ConversationDTO]:
        raise NotImplementedError('Se debe poder obtener cada una de las conversaciones hijas dado un parent_conversation_id.')

    def get_all_conversations_id(self) -> List[ConversationDTO]:
        raise NotImplementedError('Es necesario acceder a todas las conversaciones')

    def exists_this_conversation_id(self, conversation_id: Text) -> bool:
        raise NotImplementedError('Se debe poder saber si existe un conversation_id o no')

    def get_conversation_by_id(self, conversation_id: Text) -> ConversationDTO:
        raise NotImplementedError('Se debe poder obtener el objeto que representa la conversacion por medio de su ID')

    def get_conversation_by_participants(self, participant1: Text, participant2: Text) -> List[Text]:
        raise NotImplementedError('Es necesario acceder a las conversation-id que tienen como participante a participant1 y participant2')
    
    def get_conversations_by_participant(self, participant: Text) -> List[Text]:
        raise NotImplementedError('Se debe obtener las conversaciones donde participant participa')

class InMemoryConversationManager(ConversationManager):
    def __init__(self) -> None:
        super().__init__()
        self._ids_container = set()

    def get_conversations_by_participant(self, participant: Text) -> List[Text]:
        return list(
            filter(
                lambda conversation: conversation.is_participant(participant),
                self._ids_container
            )
        )

    def get_conversation_by_participants(self, participant1: Text, participant2: Text) -> List[Text]:
        result = list(
            map(
                lambda e: e.get_id(),
                filter(
                    lambda conversation: conversation.is_participant(participant1) and conversation.is_participant(participant2),
                    self._ids_container
                )
            )
        )
        if not result:
            result = [self.get_or_create_conversation_id(participant1=participant1, participant2=participant2, parent_conversation=None)]
        return result

    def get_all_conversations_id(self) -> List[ConversationDTO]:
        return list(self._ids_container)

    def exists_this_conversation_id(self, conversation_id: Text) -> bool:
        return self.get_conversation_by_id(conversation_id) is not None

    def get_conversation_by_id(self, conversation_id: Text) -> ConversationDTO:
        for conversation in self._ids_container:
            conversation: ConversationDTO
            if conversation.get_id() == conversation_id:
                return conversation
        return None

    def get_or_create_conversation_id(self, participant1: Text, participant2: Text, parent_conversation: Text) -> str:
        conversation_line = ConversationDTO(id=None, participant1=participant1, participant2=participant2, parent_conversation=parent_conversation)
        conversation_id = self._give_id_or_none(conversation_line)
        if conversation_id is not None:
            return conversation_id
        else:
            conversation_line._id = uuid.uuid4().hex
            self._ids_container.add(conversation_line)
            return conversation_line._id

    def get_children(self, parent_conversation_id: Text) -> List[ConversationDTO]:
        """
            Devuelve una lista ordenada por timestamp, la lista esta compuesta por 
            Conversation-ID:Text que cumple que tiene como padre parent_conversation_id(param)
        """

        result_list = list(
            filter(
                lambda conversation: conversation.get_parent_conversation_id() == parent_conversation_id,
                self._ids_container
            )
        )
        result_list = [
            *result_list,
            *flatten(
                map(
                    lambda conversation: self.get_children(conversation.get_id()),
                    result_list
                )
            )
        ]
        
        return result_list

    def _give_id_or_none(self, to_search: ConversationDTO) -> Optional[str]:
        for conversation in self._ids_container:
            conversation: ConversationDTO
            if (conversation.compare_participant(to_search) and
                    conversation.get_parent_conversation_id() == to_search.get_parent_conversation_id()):
                return conversation.get_id()
        return None
