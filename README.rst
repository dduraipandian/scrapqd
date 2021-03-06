
ScrapQD - Scraper Query Definition (beta)
=========================================

.. inclusion-marker-do-not-remove-start

ScrapQD consists of query definition created for scraping web data using `GraphQL-Core <https://github.com/graphql-python/graphql-core>`_
which is port of `GraphQL.js <https://github.com/graphql/graphql-js>`_.

Library intends to focus on how to locate data from website and eliminate backend process of crawling. So people can just have xpath and get data right away.

It supports scraping using `requests <https://github.com/psf/request>`_ for traditional websites and
`selenium <https://github.com/baijum/selenium-python>`_ for modern websites (js rendering).
Under selenium it supports Google Chrome and FireFox drivers.

ScrapQD library only uses `lxml <https://lxml.de/parsing.html>`_ parser and `xpath <https://www.w3schools.com/xml/xpath_syntax.asp>`_ used to locate elements.

.. inclusion-marker-do-not-remove-end

|

.. image:: https://github.com/dduraipandian/scrapqd/actions/workflows/test.yml/badge.svg?branch=main
    :target: https://github.com/dduraipandian/scrapqd/
    :alt: Test GA

.. image:: https://codecov.io/gh/dduraipandian/scrapqd/branch/development/graph/badge.svg
  :target: https://codecov.io/gh/dduraipandian/scrapqd
  :alt: codecov test coverage

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
  :target: https://opensource.org/licenses/MIT
  :alt: MIT License

.. image:: https://readthedocs.org/projects/scrapqd/badge/?version=latest
    :target: https://scrapqd.readthedocs.io/en/latest/
    :alt: Documentation Status

|

- `Explore the docs » <https://scrapqd.readthedocs.io/en/latest>`_
- `Source Code » <https://github.com/dduraipandian/scrapqd/>`_
- `Report Bug » <https://github.com/dduraipandian/scrapqd/issues>`_
- `Request Feature » <https://github.com/dduraipandian/scrapqd/issues/>`_

|

.. image:: https://github.com/dduraipandian/scrapqd/raw/main/docs/_static/scrapqd_ui.png
  :width: 100%
  :alt: scrapqd ui

.. inclusion-marker-do-not-remove-start-1

Getting Started
===============

.. topic:: **How to install**

    .. code-block:: shell

        pip install scrapqd


.. topic:: **How to run the server standalone**

    You can run scrapqd graphql server standalone without any additional code with below command.
    `Flask <https://github.com/pallets/flask/>`_ is used as server and `localhost <http://127.0.0.1:5000/scrapqd>`_.

    .. code-block:: shell

        python -m scrapqd

    Flask uses 5000 as default port. You can change the port and host with below options.

    .. code-block:: shell

        python -m scrapqd --port 5001 --host x.x.x.x

.. inclusion-marker-do-not-remove-end-1

Query
======

Sample query is loaded to GraphQL UI and `sample page <https://scrapqd.readthedocs.io/en/latest/sample.html>`_ is available within the server to practice.

.. code-block:: graphql

    query test_query($url: String!, $name: GenericScalar!) {
      result: fetch(url: $url) {
        name: constant(value: $name)
        summary: group {
          total_emp_expenses: text(xpath: "//*[@id='emp-exp-total']", data_type: INT)
          total_shown_expenses: text(xpath: "//*[@id='exp-total']/span[2]", data_type: INT)
          total_approved_expenses: text(xpath: "//*[@id='emp-exp-approved']/span[2]", data_type: INT)
        }
        exp_details: list(xpath: "//div[@class='card']") {
          name: text(xpath: "//div[contains(@class,'expense-emp-name')]")
          amount: group {
            money: text(xpath: "//h6[contains(@class,'expense-amount')]/span[1]", data_type: INT)
            name: text(xpath: "//h6[contains(@class,'expense-amount')]/span[2]")
          }
        }
      }
    }


**query variable**

.. code-block:: javascript

    // url will be used in the above query
    query_variables = {
        "url": "http://localhost:5000/scrapqd/sample_page/",
        "name": "local-testing"
    }

**Result**

.. code-block:: javascript

    {
      "data": {
        "result": {
          "name": "local-testing",
          "summary": {
            "total_emp_expenses": 309,
            "total_shown_expenses": 40,
            "total_approved_expenses": 4
          },
          "exp_details": [
            {
              "name": "Friedrich-Wilhelm, Langern",
              "amount": {
                "money": 8800,
                "name": "egp"
              }
            },
            {
              "name": "Sebastian, Bien",
              "amount": {
                "money": 3365,
                "name": "mkd"
              }
            },
            {
              "name": "Rosa, Becker",
              "amount": {
                "money": 6700,
                "name": "xof"
              }
            },
            {
              "name": "Ines, Gröttner",
              "amount": {
                "money": 8427,
                "name": "npr"
              }
            }
          ]
        }
      }
    }

.. inclusion-marker-do-not-remove-start-2

Executing with client
=====================

.. code-block:: python

    from scrapqd.client import execute_sync

    query = r"""
            query test_query($url: String!, $name: GenericScalar!) {
              result: fetch(url: $url) {
                name: constant(value: $name)
                summary: group {
                  total_shown_expenses: regex(xpath: "//*[@id='exp-total']", pattern: "(\\d+)")
                }
              }
            }"""

    query_variables = {
        "url": "http://localhost:5000/scrapqd/sample_page/",
        "name": "local-testing"
    }
    result = execute_sync(self.query, query_variables)

Integrating with existing Flask app
===================================

Sample Flask app
-----------------

.. code-block:: python

    from flask import Flask

    name = __name__
    app = Flask(name)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"


Integrating scrapqd with existing app
-------------------------------------

.. code-block:: python

    from scrapqd.app import register_scrapqd
    register_scrapqd(app,
                     register_sample_url=True,
                     redirect_root=True)

**app:** Flask application

**register_sample_url:** ``False`` will not register sample page url to Flask application. Default is ``True``

**redirect_root:** Redirect root url to graphql ui if this is set to ``True``. This will not reflect, if there is already root route defined as above example.


FAQs
====

- How to copy query from graphql ui to python code.

    - you can normally copy code from ui to python code to execute using client.
    - if you hav ``regex`` query, patterns needs to escaped in the python code. In such, use python `raw strings <https://docs.python.org/3/library/re.html#raw-string-notation>`_, where backslashes are treated as literal characters, as above example.

- How to suppress webdriver logs

    - If you see webdriver logs like below, set ``WDM_LOG_LEVEL=0`` as environment variable and run

        ..  code-block:: shell

            [INFO] [97002] [2022-03-14T02:18:26+0530] [SCRAPQD] [/webdriver_manager/logger.py:log():26] [WDM] [Driver [/99.0.4844.51/chromedriver] ...]

- How to change log level for scrapqd library

    - ``ERROR`` level is default logging. You can change this with ``SCRAPQD_LOG_LEVEL`` environment variable.

.. inclusion-marker-do-not-remove-end-2

Contribution
============

* Report bugs and request features in the `issue tracker <https://github.com/dduraipandian/scrapqd/issues>`_.

* Submit pull requests for new functionalities and/or bug fixes. Please read `Submitting Patches`_ for the process.

Submitting Patches
==================

- Follow `Test <test-for-development>`_ to test the ``main`` branch.
- Read the relevant topic from the `Document <https://scrapqd.readthedocs.io/en/latest/>`_.
- Make the required changes.
- Create test cases for your changes.
- Test your changes with tox as `Test <test-for-development>`_ in your local environment.
- Feel free to add yourself to the `AUTHORS <AUTHORS>`_ file.
- Once tests are 100% successful, Create a pull request.

Test (for development)
======================

- Clone the github repository

    .. code-block:: shell

        git clone https://github.com/dduraipandian/scrapqd.git

- Create virtual environment to work

    .. code-block:: shell

        pip3 install virtualenv
        virtualenv scrapqd_venv
        source scrapqd_venv/bin/activate

- Install tox

    .. code-block:: shell

        pip install tox

- Run tox from the project root directory

    - Current tox have four python version - py37,py38,py39,py310
    - Check your python version

        .. code-block:: shell

            python3 --version

            # Python 3.9.10

    - Once you get your version (example: use py39 for 3.9) to run tox

        .. code-block:: shell

            tox -e py39


License
=======

This project is licensed under the MIT License - see the `LICENSE <LICENSE>`_ file for details
