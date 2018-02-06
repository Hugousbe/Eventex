from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscritpionFormTest(TestCase):
    def test_form_has_filelds(self):
        """Form must have 4 fields"""
        form = SubscriptionForm()
        expected=['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        """cpf must only have digits"""
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def tes_cpf_has_11_digits(self):
        """CPF must have 11 digits."""
        form = self.make_validated_form(cpf='1234')
        field = 'cpf'
        code ='length'
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        """"""
        form = self.make_validated_form(name='HUGO Bernardes')
        self.assertEqual('Hugo Bernardes', form.cleaned_data['name'])

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def make_validated_form(self, **kwargs):
        valid = dict(name='Hugo Bernardes', cpf='12345678901',
                    email='hugo@develoop.com.br', phone='11 99485-0141')
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form
