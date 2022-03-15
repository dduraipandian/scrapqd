============
Executor
============
Executor is a crawler engine to scrape data. Any custom executor extends Executor interface and implements abstract method.

    - `Executor Interface`_
    - `Requests`_
    - `Selenium`_
        - `Selenium Driver`_
        - `Selenium Browser`_
        - `Selenium Executor`_

Executor Interface
==================

Understanding executor interface is crucial to understand default executors and creating custom executors.

.. autoclass:: scrapqd.fetch.interface.Executor
    :members:

Requests
========

Requests uses requests library for executing requests and implements parent abstract methods.

.. code-block:: python

    class Requests(Executor):
        def get_response_url(self):
            return self.response.url

        def get_response_headers(self):
            return dict(self.response.headers)

        def get_status_code(self):
            return self.response.status_code

        def get_response_text(self):
            return self.response.content

        def get_response_json(self):
            return self.response.json()

        def is_success(self):
            status_code = self.get_status_code()
            return status_code in self.success_status_code

        def crawl(self, url, headers=None, method="get", **kwargs):
            return requests.request(self.method, self.url, headers=headers, **kwargs)

Selenium
========

Selenium Driver
---------------
SeleniumDriver is the generic implementation for crawling using selenium.

.. autoclass:: scrapqd.executor.selenium_driver.selenium.SeleniumDriver
    :members:

Selenium Browser
----------------

GoogleChrome, Firefox browsers are implemented currently. GoogleChrome is given as example here.

.. autoclass:: scrapqd.executor.selenium_driver.browsers.GoogleChrome
    :members:


Selenium Executor
-----------------

Selenium executor is used to crawl modern webpages which uses javascript rendering (client-side rendering).

.. code-block:: python

    class Selenium(Executor):
        """SeleniumExecutor is class a generic processor (facade) for all browsers and
        implements all abstract method from `Executor` class."""

        def __init__(self, url, **kwargs):
            super().__init__(url, **kwargs)
            self._response_headers = {}
            self._current_url = None

        def get_response_url(self):
            if not self._current_url:
                logger.error("Not able to get current_url for %s from selenium", self.url, exc_info=True)
                return self.url
            return self._current_url

        def is_success(self):
            return True

        def get_response_text(self):
            return self.response

        def get_response_json(self):
            if isinstance(self.response, str):
                try:
                    self.response = json.loads(self.response)
                except Exception:
                    logger.exception("Not able to get convert to json data %s", self.url, exc_info=True)

            return self.response

        def get_status_code(self):
            return 200

        def get_response_headers(self):
            return self._response_headers

        def crawl(self, url, method="get", headers=None, **kwargs):
            """"Selenium crawl gets browser from browser factory and crawls the url"""
            browser_name = kwargs.get("browser", "GOOGLE_CHROME")
            browser = BrowserFactory().get(browser_name)()
            response = browser.get_page_source(url, **kwargs)
            self._response_headers = browser.get_response_headers()
            self._current_url = browser.get_current_url()
            return response