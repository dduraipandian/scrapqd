============
Query Fields
============

Query fields are GraphQL fields. scrapqd.gql has all the graphql related implementation. Refer `GraphQL documentation <https://graphql-core-3.readthedocs.io/en/latest/>`_ for more information.

Query type, Leaves type and group are categorized in scrapqd based on their role. But for graphql all the fields are created in same manner.


How to create query fields
--------------------------

Query fields are creating using ``GraphQLField`` attaching to resolver function. Resolver function will be invoked by graphql to process the query.

**Resolver function**

.. function:: resolver(parser: Parser, info: ResolveInfo, xpath, **kwargs)

        Resolver function for the graphql field.

        .. py:attribute:: parser

           Parser instance passed down from parent query.

        .. py:attribute:: info

           GraphQLResolveInfo instance which gives resolver information.

        .. py:attribute:: xpath

           path to locate node(tag).

        .. py:attribute:: kwargs

           any additional parameters defined in the GraphQL field.

**GraphQL Field**

    .. class:: Field

        GraphQL field class is used to create scrapqd query

        .. py:attribute:: type

            GraphQL field type. Mostly ``GenericScalar`` type is used for fields in the scrapqd library.

        .. py:attribute:: args

            Dictionary of arguments for the field in query ex: xpath, name.
            This should be argumented in resolver function above.

        .. py:attribute:: resolve

            resolver function which will be invoked while querying. Above resolver function should be given here.

        .. py:attribute:: description

            This description will be shown in the graphql ui for documentation.


Example: Text field
-------------------

**Resolver function**

.. code-block:: python

    @with_error_traceback
    def resolve_text(parser: Parser, info: ResolveInfo,
                     xpath, data_type=const.DATA_TYPE_DEFAULT_VALUE, multi=const.MULTI_DEFAULT_VALUE):
        """Extracts node(tag) content using given XPath.

        :param parser: Parser instance passed down from parent query.
        :param info: GraphQLResolveInfo instance which gives resolver information.
        :param xpath: path to locate node(tag).
        :param data_type:   Extracted text will be always in text format. When the data type is provided,
                            content is converted to that format and returned to the client.
                            Accepted data types:

                                - text (default)
                                - int
                                - float

        :param multi: by default, it is set to False. Thus, when the given xpath locates multiple nodes,
                   it returns first node value. if it is set `true`, it will return all the node values" \
                   as list.Given data type is applied to all the nodes individually.
        :return:

                - text - when multi is set to False, This option can be overridden to return list with single value using `NON_MULTI_RESULT_LIST`.
                - List - when multi is set to True
        """
        key = get_key(info)
        parser.datatype_check(key, data_type)
        result = parser.extract_text(key=key, multi=multi, xpath=xpath)
        result = parser.data_conversion(result, data_type)
        result = parser.get_multi_results(multi, result)
        parser.caching(key, result)
        return result


**Query Field**

.. code-block:: python

    text = Field(GenericScalar,
             args={
                 'xpath': Argument(NonNull(String), description=const.xpath_desc),
                 'data_type': Argument(DataTypeEnum, description="data type which should be converted"),
                 'multi': Argument(Boolean, description=const.multi_desc),
             },
             resolve=resolve_text,
             description="Extracts text content from the give xpath")
