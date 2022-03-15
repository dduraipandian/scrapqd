======
Query
======
Scrape Query can be created with query, group and leaf queries.

    - `Query Type`_
        - `fetch`_
        - `selenium`_

    - `Group Type`_
        - `group`_
        - `list`_

    - `Leaf Type`_
        - `constant`_
        - `text`_
        - `attr`_
        - `link`_
        - `query_params`_
        - `form_input`_
        - `regex`_

Sample Query
============

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

**Query variables**

.. code-block:: json

    {
        "url": "http://localhost:5000/scrapqd/sample_page/",
        "name": "local-testing"
    }


Query Type
==========
Query type queries are used for crawling url using different executors and pass down the data to child queries Leaf type for further processing. They expect leaf queries as sub query.

``fetch``
---------

.. function:: fetch(url, headers={}, executor="requests", is_json_response=false, method="GET", cache=false)

    Fetch query will crawl the traditional websites.

    .. py:attribute:: url

        URL to crawl

    .. py:attribute:: headers

        - sometimes websites need additional headers in the request. By default, system provides below headers. The given headers will be updated with default headers. So default system headers are constant which will be sent for all the request.

            - User-Agent: from the data files. This can be changed using USER_AGET_DATA_FILE or USER_AGET_DATA config.
            - Connection: keep-alive
            - Upgrade-Insecure-Requests: 1
            - Accept-Language: en-US,en;q=0.9
            - Accept-Encoding: gzip, deflate, br
            - Pragma: no-cache

        - You might not need this for most website. API type urls might need other extra headers and other http methods.

    .. py:attribute:: executor

        - Executors define how to crawl the url and how to process their response. By default system has "requests" executors which supports Requests library.
        - Custom executors can be creating by extending Executor class.

    .. py:attribute:: is_json_response

        - It is by default False. You have to set True if the url returns json data. Processing of json data is not supported as of now. This is for future enhancement. System will throw error if this is set to True.

    .. py:attribute:: method

        - http method to use for the request.
        - System uses **GET** by default. For website crawl you do not need to set this parameter.
        - API type urls might need other http methods like **POST**.

    .. py:attribute:: cache

        .. note:: This should be used in development period

        - Fetch will be time consuming as it gets website data from internet. While developing the query, you may run the query multiple times. It will affect the development time.
        - Setting ``cache = true`` will cache the result of the url for consequent same url.
        - Setting ``ENV=DEVELOPMENT`` in config will enable cache for all the queries by default. Anything other than development, cache parameter is ignored.


``selenium``
------------

.. function:: selenium(url, browser=GOOGLE_CHROME, options={}, is_json_response=false, cache=false)

    Selenium query will crawl the modern websites with javascript rendering.

    .. py:attribute:: url

        URL to crawl.

    .. py:attribute:: browser

        System supports below browser.

            - GOOGLE_CHROME
            - FIREFOX

    .. py:attribute:: options

        Additional options to be used in crawling using selenium.

            - ``xpath`` Selenium will wait this element to be present in the loaded webpage.
            - ``wait_time`` Selenium will wait for above xpath target (wait_time) secs.

    .. py:attribute:: is_json_response

        It is by default False. You have to set True if the url returns json data. Processing of json data is not supported as of now. This is for future enhancement. System will throw error if this is set to True.

    .. py:attribute:: cache

        Similar to cache parameter in fetch query.

Group Type
==========
Group queries process groups multiple leaf nodes and process multiple results of a xpath. They expect leaf or group queries as sub query.

- group
- list

``group``
------------
Group query will group the leaf node output under group variable to returns result to client.
This will be helpful to group certain types of elements/data from the query without needing addition outside code.

.. code-block:: graphql

    amount: group {
        money: text(xpath: "//h6[contains(@class,'expense-amount')]/span[1]", data_type: INT)
        name: text(xpath: "//h6[contains(@class,'expense-amount')]/span[2]")
    }


``list``
--------

.. function:: list(xpath)

    List query will help you to write sub-query to extract data from the parent and returns.
    If the list xpath return multiple elements, sub-query applied on each item in the list.

    .. py:attribute:: xpath

        to locate element

**Example**

.. code-block:: graphql

    exp_details: list(xpath: "//div[@class='card']") {
        name: text(xpath: "//div[contains(@class,'expense-emp-name')]")
        amount: group {
            money: text(xpath: "//h6[contains(@class,'expense-amount')]/span[1]", data_type: INT)
            name: text(xpath: "//h6[contains(@class,'expense-amount')]/span[2]")
        }
    }


**Result**

.. code-block:: python

    {
        "result": {
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
                },
                {
                  "name": "Clarissa, Bonbach",
                  "amount": {
                    "money": 1609,
                    "name": "fjd"
                  }
                },
                {
                  "name": "Zbigniew, Stolze",
                  "amount": {
                    "money": 8789,
                    "name": "ern"
                  }
                },
                {
                  "name": "Ines, Mentzel",
                  "amount": {
                    "money": 1750,
                    "name": "srd"
                  }
                }
              ],
        }
    }


Leaf Type
=========
Leaf nodes are final queries to get the value from html element such as :code:`text` from above query. You can not provide another leaf query as sub query.

- `constant`_
- `text`_
- `attr`_
- `link`_
- `query_params`_
- `form_input`_
- `regex`_

Data Types
----------
Few leaf queries support data types. If the data type is given, the element content will be converted to the given data type and sent to client.
System supported below data types. Custom data types can be created as well.

    .. py:attribute:: TEXT

        Default data type.

    .. py:attribute:: RAW

        When the element text is extract, text might have extra whitespace. They are stripped away by default. When RAW data type is given, data will be sent as it is extracted from the element.

    .. py:attribute:: INT

        - Data is converted to integer.
        - Example

            - 1,024 -> 1024
            - 12K -> 12000 (k/K - thousand, m/M - million, b/B - billion)

    .. py:attribute:: FLOAT

        - Data is converted to decimal.

Multi
-----
Leaf nodes support multi parameter. Xpath will locate multiple elements. This parameter will help the system who to process and return to client.

- ``false`` Only first element will be processed and returned to the client.
- ``true`` All the elements will be processed. Result will be sent as array/list to client. If the query supports data_type parameter, data_type conversion will be applied on all elements.

When multi is set false, result format will be not same when it is set to true.

you can set `NON_MULTI_RESULT_LIST <config.html#non-multi-result-list>`_ to ``True`` to have same format on both cases in the config file.

``constant``
------------

.. function:: constant(value)

    Constant query will give back results to client as hard coded in the query or value passed from query variables.

    .. py:attribute:: value

        Non null value in the query or can be passed from query variable as from the example.

.. code-block:: graphql

    name: constant(value:"local-testing")


``text``
--------

.. function:: text(xpath, data_type: TEXT, multi: false)

    Text query will get the content of the given element. Text does not represent that it will return text. It simply denotes that it will extract text from element.

    .. py:attribute:: xpath

        Path to locate element

    .. py:attribute:: data_type

        Data type to return

    .. py:attribute:: multi

        when xpath matches multiple elements,

         - ``False`` Processes first element
         - ``True`` Processes all elements

**Example**

.. code-block:: graphql

    total_emp_expenses: text(xpath: "//*[@id='emp-exp-total']", data_type: INT)

``attr``
--------

.. function:: attr(xpath, name=null, multi=false)

    Element will have multiple attributes as below. Attr query will help to fetch all of them or specified one. Data-hovercard-type, href are ``attributes`` on the example element. It will extract attributes value  as key, value pair. Key as name, value as value of the attribute.

    .. py:attribute::xpath

        Path to locate element

    .. py:attribute:: name

        - If the name is not given, it will extract all the attributes.
        - For example, if the name = 'href' given, it will get "{href: /abcxcom}" mapping.

    .. py:attribute:: multi

        when xpath matches multiple elements,

         - ``False`` Processes first element
         - ``True`` Processes all elements

**Example**

.. code-block:: graphql

    approval_id: attr(xpath: "//button[contains(@class, 'expense-approve')]", name: "id")


``link``
--------

.. function:: link(xpath, base_url=null, multi=false)

    In html, anchor <a> tag defines link to another web page. With link query, you can get entire url with ease.
    There are times websites use relative url.

    Link query construct full url from the requested url automatically. You can override the parent url with base_url parameter in the query.

    .. py:attribute:: xpath

        Path to locate element

    .. py:attribute:: base_url

        Custom url to create absolute url

    .. py:attribute:: multi

        when xpath matches multiple elements,

         - ``False`` Processes first element
         - ``True`` Processes all elements

**Example**

.. code-block:: graphql

    website : link(xpath:"//a[contains(@class, 'site-link')]")


``query_params``
----------------

.. function:: query_params(xpath, name: null, multi: false)

    When you want to extract query parameter from url in anchor tag or any element has url type content,
    you can use ``query_params`` query.

    .. py:attribute:: xpath

        Path to locate element

    .. py:attribute:: name

        - If the name is not given, it will extract all the query parameters in the url.
        - For example, if the name = 'product' given, it will get "{product: xyzcourse}" mapping.

    .. py:attribute:: multi

        when xpath matches multiple elements,

         - ``False`` Processes first element
         - ``True`` Processes all elements

**Example**

.. code-block:: graphql

    user_id: query_params(xpath:"//a/@href", name: "user")

**Result**

.. code-block: json

    "user_id": {
        "user": "friwilan0123"
    },

``regex``
---------

.. function:: regex(xpath, pattern, source="TEXT", multi: false)

    Regex will be used on the located element using xpath and returns the result.

    .. py:attribute:: xpath

        Path to locate element

    .. py:attribute:: pattern

        Regular expression pattern to match and it will be used in re.findall from python to extract data.

    .. py:attribute:: source

        Regular expression can be applied on located element's content or element's source html itself.

            - ``text`` Regex will be applied on element's content. This is default value.
            - ``html`` Regex will be applied on element's html.

    .. py:attribute:: multi

        when xpath matches multiple elements,

         - ``False`` Processes first element
         - ``True`` Processes all elements


**Example**

.. code-block:: graphql

    total_shown_expenses: regex(xpath: "//*[@id='exp-total']", pattern: "(\\d+)")

**Result**

.. code-block:: json

    "total_shown_expenses": [
        "40"
    ]

``form_input``
--------------

.. function:: form_input(xpath, name: null, multi: false)

    Form input query will help you to extract input elements name, value pair from form element.

    .. py:attribute:: xpath

        Path to locate form element

    .. py:attribute:: name

        - If the name is not given, it will extract all the input elements under the form.
        - If the name is given, it will get input element with the given name.

    .. py:attribute:: multi

        when xpath matches multiple elements,

         - ``False`` Processes first element
         - ``True`` Processes all elements


**Example**

**Html**

.. code-block:: html

    <form class="requestParams" id="apiAttr">
        <input name="rlz" value="1C5CHFA_enIN991IN991" type="hidden">
        <input name="tbm" value="lcl" type="hidden">
        <input name="sxsrf" value="APq-WBu3vzrA9-WQU_Mp0Zs9aq2a-PQlJg:1644327612221" type="hidden">
        <input value="vHICYpKHDaWXseMP57uWuA4" name="ei" type="hidden">
        <input value="AHkkrS4AAAAAYgKAzF3dfuu_a7YROtX7wSMb404M2sTE" disabled="true" name="iflsig" type="hidden">
    </form>

**Query**

.. code-block:: graphql

    meta_data: form(xpath: "//form[@class='requestParams']", name: "sxsrf")
