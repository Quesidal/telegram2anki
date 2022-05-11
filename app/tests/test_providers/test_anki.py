from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from providers.anki import AnkiProvider

csrf_token_mock = 'test_token'
page_part = f"""
<form action="https://ankiweb.net/account/login" id="form"
      method="post">
    <input type="hidden" name="submitted" value="1">
    <input type="hidden" name="csrf_token" value="{csrf_token_mock}">

    <div class="row form-group">
        <label for="email" class="col-2 col-form-label">Email</label>
        <div class="col-10"><input type="text" name="username"
                                  id="email" value="" autofocus></div>
    </div>
"""


class AnkiProviderTestCase(IsolatedAsyncioTestCase):
    # @patch.object(AnkiProvider, '_request', return_value=page_part)
    # async def test_get_csrf_token(self, _):
    #     csrf_token = await AnkiProvider().get_csrf_token()
    #     self.assertEqual(csrf_token, csrf_token_mock)

    # async def test_login(self):
    #     csrf_token = await AnkiProvider().login()

    async def test_save_card(self):
        anki = AnkiProvider()
        # await anki.login()
        await anki.save_card()
