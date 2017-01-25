'''
Created on 25-Jan-2017

@author: keshvij
'''


class SqlParse():
    def __init__(self):
        pass
    def format(self, sql, **options):
        """Format *sql* according to *options*.
    
        Available options are documented in :ref:`formatting`.
    
        In addition to the formatting options this function accepts the
        keyword "encoding" which determines the encoding of the statement.
    
        :returns: The formatted SQL statement as string.
        """
        encoding = options.pop('encoding', None)
#         stack = engine.FilterStack()
#         options = formatter.validate_options(options)
#         stack = formatter.build_filter_stack(stack, options)
#         stack.postprocess.append(filters.SerializerUnicode())
#         return ''.join(stack.run(sql, encoding))

class SqlBeautifier():
    
    def formatSql(self, rawSql):
        formatSql = None
        sqlParse = None
        try:
            sqlParse = SqlParse()
            formatSql = sqlParse.format(rawSql
#                             keyword_case=settings.get("keyword_case"),
#                             identifier_case=settings.get("identifier_case"),
#                             strip_comments=settings.get("strip_comments"),
#                             indent_tabs=settings.get("indent_tabs"),
#                             indent_width=settings.get("indent_width"),
#                             reindent=settings.get("reindent")
                            )
        except Exception as e:
            print(e)
            formatSql = None
        
        return formatSql
        

if __name__ == '__main__':
    pass
