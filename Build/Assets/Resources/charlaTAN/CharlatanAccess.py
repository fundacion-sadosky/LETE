from CharlatanManager import CharlatanManager
from conversation.conversation_manager import InMemoryConversationManager, ConversationManager
from conversation.message_history import InMemoryMessageHistory, MessageHistory

charlatan_manager: CharlatanManager = CharlatanManager()
charlatan_conversation_manager: ConversationManager = InMemoryConversationManager()
charlatan_message_history: MessageHistory = InMemoryMessageHistory()
