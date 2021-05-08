--database
USE master;
CREATE DATABASE iMediaDB
ON
	(NAME = iMedia_dat, FILENAME = 'E:\dev\iMedia\iMedia.mdf')
LOG ON
	(NAME = iMedia_log, FILENAME = 'E:\dev\iMedia\iMedia.ldf')

--table of WebSites
USE iMediaDB;
CREATE TABLE Sites (
	ID tinyint NOT NULL,
	Link varchar(255) NOT NULL,
	SitePriority int,
	CONSTRAINT PK_SiteID PRIMARY KEY (ID)
);

--table of Website's structure
USE iMediaDB;
CREATE TABLE SitePath (
	SiteID tinyint NOT NULL,
	DateTimePath varchar(100),
	ViewsPath varchar(100),
	TitlePath varchar(100),
	TextPath varchar(100),
	CONSTRAINT FK_SiteID FOREIGN KEY (SiteID) REFERENCES Sites(ID)
);