from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')  # client já vem no TestCase do Django

    def test_get(self):
        """Get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use template subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit')

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form=self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_filelds(self):
        """Form must have 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name','cpf','email','phone'], list(form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        """Valid POST should redirect to /inscricao/"""
        data = dict(name='Hugo Bernardes', cpf='12345678901',
                    email='hugo.bernardes@gmail.com', phone='11 99485-0141')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid PST should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        """"Email subject must be 'Confirmação de inscrição' """
        email = mail.outbox[0] #outbox guarda uma lista dos objetos criados
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        """Email must be from contato@eventex.com"""
        email = mail.outbox[0]
        expect = 'contato@eventex.com'
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        """"Email must be sent to the user and to the sender"""
        email = mail.outbox[0]
        expect = ['contato@eventex.com', 'hugo.bernardes@gmail.com']
        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        """Email body must contain name, cpf, email and phone"""
        email = mail.outbox[0]
        self.assertIn('Hugo Bernardes', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('hugo.bernardes@gmail.com', email.body)
        self.assertIn('11 99485-0141', email.body)


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Hugo Bernardes', cpf='12345678901',
        email='contato@develoop.com.br', phone='11 99485-0141')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')
