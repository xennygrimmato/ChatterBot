from tests.base_case import ChatBotTestCase
from chatterbot.conversation import Statement
from chatterbot.adapters.logic import LogicAdapter
from chatterbot.adapters.logic import MultiLogicAdapter


class TestAdapterA(LogicAdapter):

    def process(self, statement):
        return 0.2, Statement('Good morning.')


class TestAdapterB(LogicAdapter):

    def process(self, statement):
        return 0.5, Statement('Good morning.')


class TestAdapterC(LogicAdapter):

    def process(self, statement):
        return 0.7, Statement('Good night.')


class MultiLogicAdapterTestCase(ChatBotTestCase):

    def setUp(self):
        super(MultiLogicAdapterTestCase, self).setUp()
        self.adapter = MultiLogicAdapter()
        self.adapter.set_context(self.chatbot)

    def test_sub_adapter_agreement(self):
        """
        In the case that multiple adapters agree on a given
        statement, this statement should be returned with the
        highest confidence available from these matching options.
        """
        self.adapter.add_adapter(TestAdapterA())
        self.adapter.add_adapter(TestAdapterB())
        self.adapter.add_adapter(TestAdapterC())

        confidence, statement = self.adapter.process(Statement('Howdy!'))

        self.assertEqual(confidence, 0.5)
        self.assertEqual(statement, 'Good morning.')

    def test_get_greatest_confidence(self):
        statement = 'Hello'
        options = [
            (0.50, 'Hello'),
            (0.85, 'Hello'),
            (0.42, 'Hello')
        ]
        value = self.adapter.get_greatest_confidence(statement, options)

        self.assertEqual(value, 0.85)

    def test_add_adapter(self):
        sub_adapter = TestAdapterA()
        adapter_count_before = len(self.adapter.adapters)
        self.adapter.add_adapter(sub_adapter)
        adapter_count_after = len(self.adapter.adapters)

        self.assertEqual(adapter_count_after, adapter_count_before + 1)

    def test_set_context(self):
        adapter = MultiLogicAdapter()
        adapter.set_context(self.chatbot)

        # Test that the multi adapter's context is set
        self.assertEqual(adapter.context, self.chatbot)

        # Test that all sub adapters have the context set
        for sub_adapter in adapter.adapters:
            self.assertEqual(sub_adapter.context, self.chatbot)