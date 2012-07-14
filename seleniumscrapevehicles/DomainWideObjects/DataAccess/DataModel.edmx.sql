
-- --------------------------------------------------
-- Entity Designer DDL Script for SQL Server 2005, 2008, and Azure
-- --------------------------------------------------
-- Date Created: 08/02/2011 19:03:10
-- Generated from EDMX file: C:\Users\jon.JMC\seleniumScrape\DomainWideObjects\DataAccess\DataModel.edmx
-- --------------------------------------------------

SET QUOTED_IDENTIFIER OFF;
GO
IF SCHEMA_ID(N'dbo') IS NULL EXECUTE(N'CREATE SCHEMA [dbo]');
GO

-- --------------------------------------------------
-- Dropping existing FOREIGN KEY constraints
-- --------------------------------------------------

IF OBJECT_ID(N'[dbo].[FK_Page2ListList]', 'F') IS NOT NULL
    ALTER TABLE [dbo].[Lists] DROP CONSTRAINT [FK_Page2ListList];
GO
IF OBJECT_ID(N'[dbo].[FK_PagePage2List]', 'F') IS NOT NULL
    ALTER TABLE [dbo].[Pages] DROP CONSTRAINT [FK_PagePage2List];
GO

-- --------------------------------------------------
-- Dropping existing tables
-- --------------------------------------------------

IF OBJECT_ID(N'[dbo].[Lists]', 'U') IS NOT NULL
    DROP TABLE [dbo].[Lists];
GO
IF OBJECT_ID(N'[dbo].[Pages]', 'U') IS NOT NULL
    DROP TABLE [dbo].[Pages];
GO
IF OBJECT_ID(N'[dbo].[ListGroups]', 'U') IS NOT NULL
    DROP TABLE [dbo].[ListGroups];
GO

-- --------------------------------------------------
-- Creating all tables
-- --------------------------------------------------

-- Creating table 'HTMLlists'
CREATE TABLE [dbo].[HTMLlists] (
    [ListId] int IDENTITY(1,1) NOT NULL,
    [ListHtml] nvarchar(max)  NOT NULL,
    [Page2List_ID] int  NOT NULL
);
GO

-- Creating table 'HTMLpages'
CREATE TABLE [dbo].[HTMLpages] (
    [PageID] int IDENTITY(1,1) NOT NULL,
    [VehicleModel] nvarchar(max)  NOT NULL,
    [VehicleMake] nvarchar(max)  NOT NULL,
    [Page2List_ID] int  NOT NULL
);
GO

-- Creating table 'ListGroups'
CREATE TABLE [dbo].[ListGroups] (
    [ID] int  NOT NULL
);
GO

-- --------------------------------------------------
-- Creating all PRIMARY KEY constraints
-- --------------------------------------------------

-- Creating primary key on [ListId] in table 'HTMLlists'
ALTER TABLE [dbo].[HTMLlists]
ADD CONSTRAINT [PK_HTMLlists]
    PRIMARY KEY CLUSTERED ([ListId] ASC);
GO

-- Creating primary key on [PageID] in table 'HTMLpages'
ALTER TABLE [dbo].[HTMLpages]
ADD CONSTRAINT [PK_HTMLpages]
    PRIMARY KEY CLUSTERED ([PageID] ASC);
GO

-- Creating primary key on [ID] in table 'ListGroups'
ALTER TABLE [dbo].[ListGroups]
ADD CONSTRAINT [PK_ListGroups]
    PRIMARY KEY CLUSTERED ([ID] ASC);
GO

-- --------------------------------------------------
-- Creating all FOREIGN KEY constraints
-- --------------------------------------------------

-- Creating foreign key on [Page2List_ID] in table 'HTMLlists'
ALTER TABLE [dbo].[HTMLlists]
ADD CONSTRAINT [FK_Page2ListList]
    FOREIGN KEY ([Page2List_ID])
    REFERENCES [dbo].[ListGroups]
        ([ID])
    ON DELETE NO ACTION ON UPDATE NO ACTION;

-- Creating non-clustered index for FOREIGN KEY 'FK_Page2ListList'
CREATE INDEX [IX_FK_Page2ListList]
ON [dbo].[HTMLlists]
    ([Page2List_ID]);
GO

-- Creating foreign key on [Page2List_ID] in table 'HTMLpages'
ALTER TABLE [dbo].[HTMLpages]
ADD CONSTRAINT [FK_PagePage2List]
    FOREIGN KEY ([Page2List_ID])
    REFERENCES [dbo].[ListGroups]
        ([ID])
    ON DELETE NO ACTION ON UPDATE NO ACTION;

-- Creating non-clustered index for FOREIGN KEY 'FK_PagePage2List'
CREATE INDEX [IX_FK_PagePage2List]
ON [dbo].[HTMLpages]
    ([Page2List_ID]);
GO

-- --------------------------------------------------
-- Script has ended
-- --------------------------------------------------