-- ================================================
-- Template generated from Template Explorer using:
-- Create Procedure (New Menu).SQL
--
-- Use the Specify Values for Template Parameters 
-- command (Ctrl-Shift-M) to fill in the parameter 
-- values below.
--
-- This block of comments will not be included in
-- the definition of the procedure.
-- ================================================
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE update_all_MA
	-- Add the parameters for the stored procedure here
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	declare @stock_code int
	declare @date date
	declare cur cursor local for 
		select stock_code, date from historyPriceInfo 
	open cur
	fetch next from cur into @stock_code, @date

	while @@FETCH_STATUS = 0 
	begin
		exec MA_calculator @date, @stock_code
		fetch next from cur into @stock_code, @date
	end

	close cur
	deallocate cur
END
GO
