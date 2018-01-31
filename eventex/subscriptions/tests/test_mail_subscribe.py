from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        """Valid POST should redirect to /inscricao/"""
        data = dict(name='Hugo Bernardes', cpf='12345678901',
                    email='hugo.bernardes@gmail.com', phone='11 99485-0141')
        self.resp = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0] #outbox guarda uma lista dos objetos criados

    def test_subscription_email_subject(self):
        """"Email subject must be 'Confirmação de inscrição' """
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        """Email must be from contato@eventex.com"""
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        """"Email must be sent to the user and to the sender"""
        expect = ['contato@eventex.com.br', 'hugo.bernardes@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        """Email body must contain name, cpf, email and phone"""
        contents = ['Hugo Bernardes',
                    '12345678901',
                    'hugo.bernardes@gmail.com',
                    '11 99485-0141']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
