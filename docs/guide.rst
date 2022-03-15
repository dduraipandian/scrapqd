============
How to Guide
============

.. contents::
    :depth: 3

How to add custom executors to system
-------------------------------------

    - Understand `Executor Interface <executor.html#executor-interface>`_
    - Create your custom executor similar to `Requests <executor.html#requests>`_ or `Selenium <executor.html#selenium-executor>`_.
    - Add to the config - `CRAWLERS <config.html#crawlers>`_. Example: Puppeteer

        .. code-block:: python

            from crawler.executors import Puppeteer, SeleniumOther

            CRAWLERS = {
                "PUPPETEER": Puppeteer,
                "SELENIUM_OTHER": SeleniumOther
            }

    - `Override config  <config.html#how-to-create-config>`_
    - Restart your application
    - You should be able to use `select_options` as leaf query from the graphql ui.

How to add new leaves to system
--------------------------------

    - Understand `Query fields <query_fields.html>`_
    - Create your custom field similar to `Example text field <query_fields.html##example-text-field>`_.
    - Add to the config - `LEAVES <config.html#leaves>`_. Example: select_options. It should be dict(name: field object).

        .. code-block:: python

            from crawlers.fields import select_options

            LEAVES = {
                'select_options': select_options
            }

    - `Override config  <config.html#how-to-create-config>`_
    - Restart your application
    - You should be able to use `select_options` as leaf query from the graphql ui.


How to add additional data type
-------------------------------

    - Understand `Data Type <query.html#data-types>`_
    - Create your data type conversion function.

        Function should accept one value to process and return one value after conversion. Example function to boolean data conversion.

        .. code-block:: python

            def boolean(value):
                if isinstance(value, int) or isinstance(value, float):
                    value = False if value == 0 else True
                elif isinstance(value, bool):
                    pass
                elif isinstance(value, str):
                    if value.isdigit():
                        value = False if float(value) == 0 else True
                    else:
                        try:
                            value = float(value)
                            value = False if value == 0 else True
                        except:
                            value = False if value == 'false' else True
                elif value is not None:
                    value = True
                else:
                    value = False
                return value


    - Add to the config - `DATATYPE_CONVERSION <config.html#datatype-conversion>`_. Example: boolean. It should be dict(name: function).

        .. code-block:: python

            from crawlers.data_types import boolean

            LEAVES = {
                'boolean': boolean
            }

    - `Override config  <config.html#how-to-create-config>`_
    - Restart your application
    - You should be able to use `boolean` as data type in the query.


How to add browsers to system
-----------------------------

    - Understand `Browser <executor.html#selenium-browser>`_ implementation.
    - Create your custom browser similar to `GoogleChrome <executor.html#scrapqd.executor.selenium_driver.browsers.GoogleChrome>`_.
    - Add to the config - `BROWSER <config.html#leaves>`_. Example: chromium. It should be dict(name: field object).

        .. code-block:: python

            from crawlers.browsers import chromium

            LEAVES = {
                'CHROMIUM': chromium
            }

    - `Override config  <config.html#how-to-create-config>`_
    - Restart your application
    - You should be able to use `CHROMIUM` in the `browser with selenium query <query.html#browser>`_.
