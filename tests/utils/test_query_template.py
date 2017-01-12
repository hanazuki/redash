from redash.utils import QueryTemplate
from collections import namedtuple
from unittest import TestCase


class TestQueryTemplateParameters(TestCase):
    def test_returns_empty_list_for_regular_query(self):
        query = u"SELECT 1"
        self.assertEqual([], QueryTemplate(query).parameters)

    def test_finds_all_params(self):
        query = u"SELECT {{param}} FROM {{table}}"
        params = ['param', 'table']
        self.assertEqual(params, QueryTemplate(query).parameters)

    def test_deduplicates_params(self):
        query = u"SELECT {{param}}, {{param}} FROM {{table}}"
        params = ['param', 'table']
        self.assertEqual(params, QueryTemplate(query).parameters)

    def test_handles_nested_params(self):
        query = u"SELECT {{param}}, {{param}} FROM {{table}} -- {{#test}} {{nested_param}} {{/test}}"
        params = ['param', 'table', 'test', 'nested_param']
        self.assertEqual(params, QueryTemplate(query).parameters)

class TestQueryTemplateRender(TestCase):
    def test_renders_without_params(self):
        query = u"SELECT 1"
        self.assertEqual(u"SELECT 1", QueryTemplate(query).render({}))

    def test_renders_with_params(self):
        query = u"SELECT {{param}} FROM {{table}}"
        param_values = {'param': 'id', 'table': 'entries'}
        self.assertEqual(u"SELECT id FROM entries", QueryTemplate(query).render(param_values))

    def test_raise_for_missing_values(self):
        query = u"SELECT {{param1}}, {{param2}} FROM {{table}}"
        param_values = {'param1': 'id'}

        with self.assertRaises(QueryTemplate.ParameterValuesMissing) as cm:
            QueryTemplate(query).render(param_values)

        self.assertEqual(cm.exception.message, "Missing")
