USE [ICS_Reporting]
GO
/****** Object:  Table [dbo].[students]    Script Date: 3/14/2020 5:04:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[students](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [varchar](255) NOT NULL,
	[email] [varchar](255) NOT NULL,
	[phone] [varchar](255) NOT NULL,
 CONSTRAINT [PK_students] PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[students] ON
GO
INSERT [dbo].[students] ([id], [name], [email], [phone]) VALUES (3, N'Parwiz', N'parwiz.f@gmail.com', N'009378976767')
GO
INSERT [dbo].[students] ([id], [name], [email], [phone]) VALUES (4, N'John Doe', N'johndoe@gmail.com', N'999999999')
GO
INSERT [dbo].[students] ([id], [name], [email], [phone]) VALUES (5, N'Karimja', N'ka@gmail.com', N'7333392')
GO
INSERT [dbo].[students] ([id], [name], [email], [phone]) VALUES (6, N'Jamal', N'ja@gmail.com', N'3434343')
GO
INSERT [dbo].[students] ([id], [name], [email], [phone]) VALUES (7, N'Nawid', N'na@gmail.com', N'343434')
GO
INSERT [dbo].[students] ([id], [name], [email], [phone]) VALUES (8, N'Tom Logan', N'Tom@gmail.com', N'7347374347')
GO
INSERT [dbo].[students] ([id], [name], [email], [phone]) VALUES (12, N'Tom Logan', N'tom@gmail.com', N'11111111111')
GO
INSERT [dbo].[students] ([id], [name], [email], [phone]) VALUES (13, N'Fawad', N'fa@gmail.com', N'347374837483')
GO
INSERT [dbo].[students] ([id], [name], [email], [phone]) VALUES (14, N'Danny', N'wa@gmail.com', N'5026801944')
GO
SET IDENTITY_INSERT [dbo].[students] OFF
GO
