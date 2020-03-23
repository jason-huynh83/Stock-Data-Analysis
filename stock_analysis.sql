create database stock;
create table stock_table (
	Symbol varchar(50),
    Company varchar(100),
    Earnings_Date varchar(100),
    EPS_Estimate varchar(10),
    Reported_EPS varchar(20),
    Surprise_percent varchar(20)
);
select * from stock_table;
desc stock_table;
drop table stock_table;
