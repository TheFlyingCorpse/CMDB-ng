/****** Object:  Table [dbo].[objectStore]    Script Date: 16/07/2017 23:17:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[objectStore](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[source] [varchar](50) NULL,
	[source_key] [varchar](255) NULL,
	[jsonblob] [varchar](max) NULL,
	[metablob] [nvarchar](max) NULL,
	[jsonlastmodified] [datetime] NULL,
	[metalastmodified] [datetime] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[objectStore_log]    Script Date: 16/07/2017 23:17:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[objectStore_log](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[object_id] [int] NULL,
	[source] [nvarchar](50) NOT NULL,
	[source_key] [nvarchar](50) NOT NULL,
	[jsonblob] [nvarchar](max) NOT NULL,
	[metablob] [nvarchar](max) NULL,
	[lastmodified] [datetime] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[utility_scripts]    Script Date: 16/07/2017 23:17:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[utility_scripts](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[script] [nvarchar](50) NULL,
	[parameter] [nvarchar](50) NULL,
	[config] [nvarchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Index [IX_objectStore]    Script Date: 16/07/2017 23:17:23 ******/
CREATE UNIQUE NONCLUSTERED INDEX [IX_objectStore] ON [dbo].[objectStore]
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [dbo].[objectStore] ADD  DEFAULT (getdate()) FOR [jsonlastmodified]
GO
ALTER TABLE [dbo].[objectStore] ADD  DEFAULT (getdate()) FOR [metalastmodified]
GO
ALTER TABLE [dbo].[objectStore_log] ADD  DEFAULT (getdate()) FOR [lastmodified]
GO
/****** Object:  Trigger [dbo].[ObjectStoreLogTrigger]    Script Date: 16/07/2017 23:15:19 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TRIGGER [dbo].[ObjectStoreLogTrigger] on [dbo].[objectStore] FOR UPDATE AS
DECLARE @NOW DATETIME
SET @NOW = CURRENT_TIMESTAMP
UPDATE objectStore_log
   SET lastmodified = @now
  FROM objectStore_log, DELETED
 WHERE objectStore_log.object_id = DELETED.id
   AND objectStore_log.lastmodified IS NULL
INSERT INTO objectStore_log (object_id,source,source_key,jsonblob,metablob)
SELECT inserted.id,inserted.source,inserted.source_key,inserted.jsonblob,inserted.metablob
FROM INSERTED, DELETED
WHERE INSERTED.jsonblob <> DELETED.jsonblob
GO
ALTER TABLE [dbo].[objectStore] ENABLE TRIGGER [ObjectStoreLogTrigger]
GO
