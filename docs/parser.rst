=======
Parser
=======
Parser is used in the GraphQL query to parse the html. Current system supports xpath in Lxml parser.

Library does not support Beautiful soup as it slower than lxml parser and Selector parsing is comparatively slower than xpath.

    - `Lxml`_

Lxml
====

.. autoclass:: scrapqd.gql_parser.lxml_parser.LXMLParser
    :members: