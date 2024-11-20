from typing import List, Dict, Text, Any


class ExportableElement:
    def to_dict(self) -> Dict[Text, Any]:
        raise NotImplementedError('Definir su formato en dict para ser exportado')


class ConversationExport:
    def __init__(self, elements_to_export: List[ExportableElement]) -> None:
        self._elements_to_export = elements_to_export

    def export(self):
        raise NotImplementedError('Definir el metodo export')


class ListExport(ConversationExport):

    def __init__(self, elements_to_export: List[ExportableElement]) -> None:
        super().__init__(elements_to_export)

    def export(self) -> List[Dict]:
        result = []
        for element_to_export in self._elements_to_export:
            result.append(element_to_export.to_dict())
        return result
