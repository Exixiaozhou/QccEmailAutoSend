from enum import Enum


class WebHeaders(Enum):
    get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/95.0.4638.69 Safari/537.36'
    }


class LoginUrl(Enum):
    get = {
        'gcaptcha4_load': 'https://gcaptcha4.geetest.com/load',
        'gcaptcha4_verify': 'https://gcaptcha4.geetest.com/verify?',
        '': 'https://www.qcc.com/api/home/getNewsFlash?firstRankIndex='
        'https://gcaptcha4.geetest.com/load?callback=geetest_1690468808239&captcha_id=8daf8b2d78f74aea6a77c0d10da77d41&client_type=web&pt=1&lang=zho'
    }

    post = {
        'login': 'https://www.qcc.com/api/auth/pass-login'
    }


class IndexSearchUrl(Enum):
    get = {
        'index_url': 'https://www.qcc.com/web/search',
    }
