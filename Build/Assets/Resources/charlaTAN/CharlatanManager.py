import os
import logging
from rasa.shared.utils.io import read_config_file
from rasa.core.utils import read_endpoint_config
from rasa.core.utils import EndpointConfig
from rasa.core.agent import Agent
from rasa.exceptions import ModelNotFound
from rasa.shared.constants import DEFAULT_MODELS_PATH, DEFAULT_ENDPOINTS_PATH
from rasa.model import get_local_model
from typing import Dict, Text, List
from CharlatanExceptions import AgentNotExists, AgentNotReady, FolderNotFound, CharlatanExceptions
from CharlatanConstants import DEFAULT_CHATBOTS_PATH, PREFIX_CHATBOTS_IN_PROGRESS

logger = logging.getLogger(__name__)


def get_subfolders(folder_path) -> List[str]:
    try:
        return [f.path for f in os.scandir(folder_path) if f.is_dir()]
    except FileNotFoundError:
        raise Exception(f"No existe el directorio {folder_path}")


class CharlatanManager:
    def __init__(self) -> None:
        self._agents = {}
        self.agents_errors: List[CharlatanExceptions] = []
        self.agents_warnings: List[CharlatanExceptions] = []
        self.agents_debug: List[CharlatanExceptions] = []
        self._agents_paths = {}
        self._load_agents(DEFAULT_CHATBOTS_PATH)

    def get_agent_path(self, agent_name: str):
        return self._agents_paths[agent_name]

    def agent_exists(self, name):
        return name in self._agents

    def get_agent(self, agent_name: Text):
        """
            Return Agent if exists, if doesnt exists return none
        """
        try:
            return self._agents[agent_name]
        except KeyError:
            exception = AgentNotExists(f"No existe {agent_name} en el conjunto de chatbots")
            self.agents_warnings.append(exception)
            logger.warning(exception)
            raise exception

    def exists_agent(self, agent_name):
        return agent_name in self._agents.keys()

    def _load_agents(self, folder_path):
        """
        folder_path = Folder that contains all the RASA Projects. Example:
            Main_Folder
                      | Chatbots
                                | Chatbot1
                                         | actions
                                         | data
                                         | models
                                         | ...
                                | Chatbot2
                                         | ...
            So, folder_path = "Chatbots" -> Remmeber PythonPath has "Main_Folder" in his definition
        """
        subfolders = get_subfolders(folder_path)
        for subdir in subfolders: 
            agent_name = subdir.replace(folder_path+os.path.sep, "")
            endpoint_path = os.path.join(subdir, DEFAULT_ENDPOINTS_PATH)
            model_path = os.path.join(subdir, DEFAULT_MODELS_PATH)
            self._agents_paths[agent_name] = subdir
            if agent_name.startswith(PREFIX_CHATBOTS_IN_PROGRESS):
                self._try_load_agent(agent_name, model_path, endpoint_path)
            else:
                self._load_specific_agent(agent_name, model_path, endpoint_path)
        self.print_errors()           
        self.print_warnings()
        self.print_debug()

    def _try_load_agent(self, agent_name, model_path, endpoint_path):
        try:
            self._load_specific_agent(agent_name, model_path, endpoint_path)
        except FolderNotFound as err:
            self.agents_errors.append(err)
        except AgentNotReady as war: 
            self.agents_warnings.append(war)

    
    def _load_specific_agent(self, agent_name, model_path, endpoint_path) -> bool:
        #endpoint_path = path to endpoints.yml
        try:
            local_model_path = get_local_model(model_path)
            _action_endpoint = read_endpoint_config(endpoint_path, endpoint_type="action_endpoint")
            new_agent = Agent.load(model_path=local_model_path, action_endpoint= _action_endpoint)
            if not new_agent.is_ready():
                raise AgentNotReady(f"{agent_name} no pudo ser cargado correctamente")
            self._agents[agent_name] = new_agent
            self.agents_debug.append(f"{agent_name} cargado exitosamente")
        except ModelNotFound: 
            raise FolderNotFound(f"No existe {model_path} al cargar {agent_name}")

    def print_warnings(self):
        if self.agents_warnings:
            for element in self.agents_warnings:
                logger.warning(element)

    def print_errors(self):
        if self.agents_errors:
            for element in self.agents_errors:
                logger.error(element)    
    
    def print_debug(self):
        if self.agents_debug:
            for element in self.agents_debug:
                logger.debug(element)
    
    def get_agents(self) -> Dict[str, Agent]:
        return self._agents
    
    def deactivate_agent(self, agent_name):
        agent = self.get_agent(agent_name)
        agent.deactivate_agent()
    
    def activate_agent(self, agent_name):
        agent = self.get_agent(agent_name)
        agent.activate_agent()