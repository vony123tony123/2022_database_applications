USE [StockAnaylze]
GO
/****** Object:  StoredProcedure [dbo].[MA_calculator]    Script Date: 2023/3/20 下午 02:11:06 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
ALTER PROCEDURE [dbo].[MA_calculator]
	-- Add the parameters for the stored procedure here
	@date char(10),
	@stock_code varchar(10)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	declare @MA5 real
	declare @MA10 real
	declare @MA20 real
	declare @MA60 real
	declare @MA120 real
	declare @MA240 real

    -- Insert statements for procedure here
	SELECT @MA5 = AVG([c])
	FROM historyPriceInfo
	WHERE date in (Select date from find_date(@date, 5,1,0)) and stock_code = @stock_code

	SELECT @MA10 = AVG([c])
	FROM historyPriceInfo
	WHERE date in (Select date from find_date(@date, 10,1,0)) and stock_code = @stock_code

	SELECT @MA20 = AVG([c])
	FROM historyPriceInfo
	WHERE date in (Select date from find_date(@date, 20,1,0)) and stock_code = @stock_code

	SELECT @MA60 = AVG([c])
	FROM historyPriceInfo
	WHERE date in (Select date from find_date(@date, 60,1,0)) and stock_code = @stock_code

	SELECT @MA120 = AVG([c])
	FROM historyPriceInfo
	WHERE date in (Select date from find_date(@date, 120,1,0)) and stock_code = @stock_code

	SELECT @MA240 = AVG([c])
	FROM historyPriceInfo
	WHERE date in (Select date from find_date(@date, 240,1,0)) and stock_code = @stock_code

	update historyPriceInfo
	set MA5 = @MA5, MA10=@MA10, MA20=@MA20, MA60=@MA60, MA120=@MA120, MA240=@MA240
	where date=@date and stock_code = @stock_code

END
