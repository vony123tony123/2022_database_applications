USE [StockAnaylze]
GO
/****** Object:  UserDefinedFunction [dbo].[find_date]    Script Date: 2023/3/20 下午 02:21:33 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER function [dbo].[find_date](@startdate varchar(50), @count_date int, @include_the_day bit, @is_back bit)
returns @result table
(
 date date,
 day_of_stock int,
 other nvarchar(50)
)
as
begin
	declare @date_cnt int;
	declare @start_count int;
	if (@include_the_day=1)
	begin
		SET @start_count=0;
	end
	else
		SET @start_count=1;


	select @date_cnt = day_of_stock from dbo.calendar where date=@startdate;
	if (@is_back = 0)
		insert @result
		select Top(@count_date) * from dbo.calendar where date <= @startdate
		and day_of_stock!=-1 
		and abs(@date_cnt - day_of_stock)%@count_date between @start_count and @count_date
		order by date desc;
	else
		insert @result
		select  Top(@count_date) * from dbo.calendar where date >= @startdate
		and day_of_stock!=-1 
		and abs(day_of_stock - @date_cnt)%@count_date between @start_count and @count_date
		order by date asc;
	return
end;