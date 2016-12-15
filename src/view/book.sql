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