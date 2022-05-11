import asyncio
import logging
import re

import aiohttp
import backoff

logger = logging.getLogger('providers')


class AnkiProvider:
    LOGIN_URL = 'https://ankiweb.net/account/login'
    SAVE_CARD_URL = 'https://ankiuser.net/edit/save'
    SAVE_CARD_FORM_URL = 'https://ankiuser.net/edit/'

    def __init__(self, username=None, password=None, login_cookie=None):
        self._username = username
        self._password = password

        self._login_cookie = login_cookie

        self._session = None

    async def save_card(self, front: str, back: str):
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            self._session = session

            if self._login_cookie is None:
                logger.debug('Start login')
                await self.login()

            csrf_token_form = await self.get_edit_form_csrf_token()

            data = 'nid=&' \
                   f'data=%5B%5B%22{front}%22%2C%22{back}%22%5D%2C%22%22%5D&' \
                   f'csrf_token={csrf_token_form}&' \
                   'mid=1650612674725&deck=1'

            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'cookie': f'ankiweb={self._login_cookie}'
            }

            result = await self._request_save_card(data, headers)

            self._session = None

        logger.info(f"Card saved: {result}")
        return result

    async def login(self):
        login_csrf = await self.get_login_form_csrf_token()

        form = aiohttp.FormData()
        form.add_field(name='submitted', value=1)
        form.add_field(name='csrf_token', value=login_csrf)
        form.add_field(name='username', value=self._username)
        form.add_field(name='password', value=self._password)

        headers = {
            "cookie": "ankiweb=login",
        }

        self._login_cookie = await self._request_post_login(url=self.LOGIN_URL,
                                                            data=form,
                                                            headers=headers)
        return self._login_cookie

    async def get_edit_form_csrf_token(self) -> str:
        headers = {'cookie': f'ankiweb={self._login_cookie}'}
        login_page_html = await self._request(url=self.SAVE_CARD_FORM_URL, headers=headers)
        csrf_token_pattern = re.compile("(Editor\(')(.*)(',)")  # (group1)(group2)(group3)
        edit_form_csrf_token = csrf_token_pattern.search(login_page_html).group(2)  # group 2 is token value in regex
        logger.debug(f"Edit form CSRF token received: {edit_form_csrf_token}")
        return edit_form_csrf_token

    async def get_login_form_csrf_token(self) -> str:
        login_page_html = await self._request(url=self.LOGIN_URL, headers={})
        csrf_token_pattern = re.compile('("csrf_token")\s(value=")(.*)(")')  # (group1)\s(group2)(group3)(group4)
        login_form_csrf_token = csrf_token_pattern.search(login_page_html).group(3)  # group 3 is token value in regex
        logger.debug(f"Login form CSRF token received: {login_form_csrf_token}")
        return login_form_csrf_token

    @backoff.on_exception(backoff.expo, (aiohttp.ClientResponseError,))
    async def _request_save_card(self, data, headers):
        async with self._session.post(url=self.SAVE_CARD_URL, data=data, headers=headers) as resp:
            return await resp.text()

    async def _request(self, url: str, headers=None):
        if headers is None:
            headers = dict()

        async with self._session.get(url, headers=headers) as resp:
            return await resp.text()

    async def _request_post_login(self, url: str, data, headers: dict):
        async with self._session.post(url, data=data, headers=headers, allow_redirects=False) as resp:
            self._login_cookie = resp.cookies.get('ankiweb').value
            if self._login_cookie:
                logger.info(f"Successful logged {self._login_cookie}")
            return self._login_cookie

    async def _request_post(self, url: str, data: any, headers: dict):
        async with self._session.post(url, headers=headers, data=data) as resp:
            a = await resp.text()
            print(await resp.text())
            return a
