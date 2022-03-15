========
Settings
========
ScrapQD uses below default configuration to function properly. Below configs can be overridden by user config.
Default config is located `here <https://github.com/dduraipandian/scapqd/blob/sphinx_doc/scrapqd/settings/_default_config.py>`__.

    - `Config`_
        - `APP_NAME`_
        - `CRAWLERS`_
        - `LEAVES`_
        - `QUERY_FIELDS`_
        - `BROWSERS`_
        - `DATATYPE_CONVERSION`_
        - `NON_MULTI_RESULT_LIST`_
        - `LOCAL_CACHE_TTL`_
        - `USER_AGET_DATA_FILE`_
        - `USER_AGET_DATA`_
        - `CHROMIUM_VERSION`_
        - `GECKODRIVER_VERSION`_
    - `How to create config`_

Config
======

APP_NAME
--------
Default app name is ScrapQD. You can change this from config.

CRAWLERS
--------
Requests and Selenium are system crawlers. If the defines customer executor, it needs to defined in the config.

LEAVES
------
Application owner can define custom leaves for their use case and provide in config to use in the query. Leaves are explained `here <query.html#leaf-type>`_.

QUERY_FIELDS
------------
Application owner can define additional query fields (ex: puppeteer) and provide in the config. Queries are explained `here <query.html#query-type>`__.

BROWSERS
---------
System uses GOOGLE_CHROME, FIREFOX browser in selenium to crawl modern webpages (javascript rendering). Custom browser can be created using Browser class and update this configuration.

DATATYPE_CONVERSION
-------------------
Additional custom data type conversion mapping for the application.

NON_MULTI_RESULT_LIST
---------------------
Config whether to send result as List or return single element when multi=False in the leaf nodes. You can read more from `here <query.html#multi>`__.

LOCAL_CACHE_TTL
----------------
Fetch results are cached in local memory to speed up development. However, lifetime of the cache will be 10 minutes by default.
You can update this config to change ttl of cache. You can read more about this `here <query.html#query-type>`__.

USER_AGET_DATA_FILE
-------------------
User-Agent is added to each request headers while using `fetch <query.html#fetch>`_ query.
ScrapQD library has set of latest user agents in the file to load.

You can override them if you have your own user-agent files. Each user agent entry should on new line.

.. note::

    Best to keep user-agent updated with latest agents on regular basis. Sites might return different format for older user agents.

USER_AGET_DATA
--------------
You can set this as list of user agents. System will use this and ignore `USER_AGET_DATA_FILE`_ config.

CHROMIUM_VERSION
----------------
System downloads latest version on chromium engine. You can set this to use the same version. Latest version will be downloaded by default.

GECKODRIVER_VERSION
-------------------
If you are using firefox browser, you can set this to use specific gecko driver version. Otherwise latest version will be used.

DEFAULT_BROWSER
---------------
GOOGLE_CHROME is the default browser used in the library. You can update this to change to "FIREFOX".

How to Create config
======================
You can add additional `LEAVES`_, `CRAWLERS`_, `QUERY_FIELDS`_ and `DATATYPE_CONVERSION`_. But you can not override the system config.

You can override rest of the configs. You can create the file with configs as `here <https://github.com/dduraipandian/scapqd/blob/sphinx_doc/scrapqd/settings/_default_config.py>`__ and set `SCRAPQD_CONFIG` environment variable.

**Example:**

Your project files are under google_search and you have your config /google_search/configuration/scrapqd_config.py.

Your environment variable should be

.. code-block:: python

    SCRAPQD_CONFIG=configuration.scrapqd_config
