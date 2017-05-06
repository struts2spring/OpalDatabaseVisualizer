# import sublime, sublime_plugin

import sys
import os
from src.SqlBeautifier import sqlparse2
import logging

logger = logging.getLogger('extensive')
sys.path.append(os.path.dirname(__file__))

# if sys.version_info >= (3, 0):
#     import sqlparse3 as sqlparse
# else:
#     import sqlparse2 as sqlparse


# for ST2
settings ={
    "keyword_case": "upper",
    "identifier_case": None,
    "strip_comments": False,
    "indent_tabs": False,
    "indent_width": 2,
    "reindent": True
}
# sublime.load_settings('SQL Beautifier.sublime-settings')

# for ST3
def plugin_loaded():
    global settings
    settings ={
        "keyword_case": "upper",
        "identifier_case": None,
        "strip_comments": False,
        "indent_tabs": False,
        "indent_width": 2,
        "reindent": True
    }
 
#     sublime.load_settings('SQL Beautifier.sublime-settings')


# class SqlBeautifierCommand(sublime_plugin.TextCommand):
class SqlBeautifierCommand():
    def format_sql(self, raw_sql):
        try:
            formatted_sql = sqlparse2.format(raw_sql,
                keyword_case=settings.get("keyword_case"),
                identifier_case=settings.get("identifier_case"),
                strip_comments=settings.get("strip_comments"),
                indent_tabs=settings.get("indent_tabs"),
                indent_width=settings.get("indent_width"),
                reindent=settings.get("reindent")
            )

#             if self.view.settings().get('ensure_newline_at_eof_on_save'):
            formatted_sql += "\n"

            return formatted_sql
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def replace_region_with_formatted_sql(self, edit, region):
        selected_text = self.view.substr(region)
        foramtted_text = self.format_sql(selected_text)
        self.view.replace(edit, region, foramtted_text)

    def run(self, edit):
        window = self.view.window()
        view = window.active_view()

#         for region in self.view.sel():
#             if region.empty():
#                 selection = sublime.Region(0, self.view.size())
#                 self.replace_region_with_formatted_sql(edit, selection)
#                 self.view.set_syntax_file("Packages/SQL/SQL.tmLanguage")
#             else:
#                 self.replace_region_with_formatted_sql(edit, region)


if __name__=='__main__':
#     raw_sql='select a,b,c,d,e from abc;'
    raw_sql="""SELECT EmployeeID, FirstName, LastName, HireDate, City FROM Employees
WHERE City <> 'London';
SELECT EmployeeID, FirstName, LastName, HireDate, City FROM Employees
WHERE HireDate >= '1-july-1993';

SELECT EmployeeID, FirstName, LastName, HireDate, City FROM Employees
WHERE City IN ('Seattle', 'Tacoma', 'Redmond') ORDER BY City;

select * from book;
-- drop table book_folder;
-- drop table book_info;
DROP TABLE COMPANY;
CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     CHECK(AGE > 0),
   ADDRESS        CHAR(50),
   SALARY         REAL    DEFAULT 50000.00
);

CREATE TABLE DEPARTMENT(
   ID INT PRIMARY KEY      NOT NULL,
   DEPT           CHAR(50) NOT NULL,
   EMP_ID         INT      NOT NULL
);




CREATE VIEW book_author AS
SELECT book.book_name, author.author_name
FROM  book, author, book_author_link where book.id=book_author_link.id and author.id=book_author_link.id;

"""
    formatted_sql=SqlBeautifierCommand().format_sql(raw_sql)
    logger.debug(formatted_sql)
