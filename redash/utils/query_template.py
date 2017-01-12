import pystache
from funcy import distinct

class QueryTemplate:
    def __init__(self, query):
        self.query = query

    @staticmethod
    def _collect_key_names(nodes):
        keys = []
        for node in nodes._parse_tree:
            if isinstance(node, pystache.parser._EscapeNode):
                keys.append(node.key)
            elif isinstance(node, pystache.parser._SectionNode):
                keys.append(node.key)
                keys.extend(_collect_key_names(node.parsed))

            return distinct(keys)

    @property
    def parameters(self):
        nodes = pystache.parse(self.query)
        keys = QueryTemplate._collect_key_names(nodes)
        return keys

    def render(self, parameter_values):
        missing_params = set(self.parameters) - set(parameter_values.keys())
        if missing_params:
            raise ParameterValuesMissing('Missing parameter value for: {}'.format(", ".join(missing_params)))

        return pystache.render(self.query, parameter_values)

    class ParameterValuesMissing(Exception):
        pass
