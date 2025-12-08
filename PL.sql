/*
Project Group 29 - Team Erlenmyer - Groove Journal
Group Project Step 4 draft
CS340 Fall 2025
Members:
Jorge Rodriguez
Antonio Olaguer II
Description: This file contains all the stored procedures for the Groove Journal project.
Citations: 
- Initial database schema creation and reset procedure inspired by CS340 course materials.
- All code written by Jorge Rodriguez and Antonio Olaguer II unless otherwise noted.
*/

/*
stored procedure to insert new diary_entry into Diary_Entries
*/
DELIMITER //
DROP PROCEDURE IF EXISTS sp_InsertDiaryEntry;

CREATE PROCEDURE sp_InsertDiaryEntry(IN diary_entry_text LONGTEXT, IN diary_entry_datetime DATETIME, IN diary_entry_author_id INT, IN diary_entry_album INT)
BEGIN
    INSERT INTO Diary_Entries (diary_entry, diary_entry_datetime, author_user_id, listened_to_album_id)
    VALUES (
        diary_entry_text,
        diary_entry_datetime,
        diary_entry_author_id,
        diary_entry_album
        );        

END //
DELIMITER ;

/*
stored procedure to insert album into Albums_have_Owners
*/
DROP procedure IF EXISTS sp_InsertAlbumsHaveOwners;

DELIMITER //
CREATE PROCEDURE `sp_InsertAlbumsHaveOwners` (IN album_entry_id INT, user_entry_id INT)
BEGIN
    INSERT INTO Albums_have_Owners (album_id, user_id)
    VALUES (
        album_entry_id,
        user_entry_id
        );      
END//
DELIMITER ;


/*
stored procedure to insert album into Albums
*/

DROP procedure IF EXISTS `sp_InsertAlbum`;

DELIMITER //
CREATE PROCEDURE `sp_InsertAlbum` (
    IN album_entry_title VARCHAR(255), 
    IN album_entry_label VARCHAR(255), 
    IN album_entry_country VARCHAR(255), 
    IN album_entry_year INT,
    OUT result INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        SET result = -99;
        ROLLBACK;
    END;

    START TRANSACTION;
    -- Insert into Albums
    INSERT INTO Albums (album_title, album_label, album_country, album_year)
    VALUES (
        album_entry_title,
        album_entry_label,
        album_entry_country,
        album_entry_year
    );
    SET result = LAST_INSERT_ID();

    COMMIT;
END //

DELIMITER ;

/*
stored procedure to insert track into Tracks
*/
DROP procedure IF EXISTS `sp_InsertTrack`;

DELIMITER //
CREATE PROCEDURE `sp_InsertTrack` (
    IN track_entry_title VARCHAR(255),
    OUT result INT
)
proc: BEGIN
    DECLARE existing_id INT DEFAULT NULL;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET result = -99;
        ROLLBACK;
    END;

   -- Check if track_title already exists
    SELECT track_id INTO existing_id
    FROM Tracks
    WHERE track_title = track_entry_title
    LIMIT 1;

    IF existing_id IS NOT NULL THEN
        SET result = existing_id;
        LEAVE proc;
    END IF;

    START TRANSACTION;

    -- Insert the track
    INSERT INTO Tracks (track_title)
    VALUES (track_entry_title);
    SET result = LAST_INSERT_ID();

    COMMIT;
END proc //

DELIMITER ;

/*
stored procedure to insert track into Albums_Have_Tracks
*/
DELIMITER //
CREATE PROCEDURE `sp_InsertAlbumsHaveTracks` (IN track_entry_id INT, album_entry_id INT, track_entry_order_num INT)
BEGIN
	INSERT INTO Albums_have_Tracks (track_id, album_id, track_order_num)
		VALUES (
			track_entry_id,
            album_entry_id,
            track_entry_order_num
            );
END //

DELIMITER ;

/*
stored procedure to insert artist into Artists
*/

DROP PROCEDURE IF EXISTS `sp_insertArtist`;

DELIMITER //
CREATE PROCEDURE `sp_insertArtist` (
    IN artist_entry_name VARCHAR(255),
    OUT result INT
)
proc: BEGIN
    DECLARE existing_id INT DEFAULT NULL;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET result = -99;
        ROLLBACK;
    END;

    -- Check if artist already exists
    SELECT artist_id INTO existing_id
    FROM Artists
    WHERE artist_name = artist_entry_name
    LIMIT 1;

    IF existing_id IS NOT NULL THEN
        SET result = existing_id;
        LEAVE proc; 
    END IF;

    START TRANSACTION;

    -- Insert new artist
    INSERT INTO Artists (artist_name)
    VALUES (artist_entry_name);

    SET result = LAST_INSERT_ID();

    COMMIT;

END proc //
DELIMITER ;

/*
stored procedure to insert artist into Artists_Have_Tracks
*/
DROP procedure IF EXISTS `sp_InsertArtistsHaveTracks`;

DELIMITER //
CREATE PROCEDURE `sp_InsertArtistsHaveTracks`(
				IN artist_entry_id INT, 
                IN track_entry_id INT
                )
                
BEGIN
	INSERT INTO Artists_have_Tracks (artist_id, track_id)
		VALUES (
			artist_entry_id,
			track_entry_id
            );
            
END //

DELIMITER ;

/*
stored procedure to insert artist into Albums_Have_Artists
*/
DROP procedure IF EXISTS `sp_InsertAlbumsHaveArtists`;

DELIMITER //
CREATE PROCEDURE `sp_InsertAlbumsHaveArtists`(
                    IN album_entry_id INT,
                    IN artist_entry_id INT
                            )
                
BEGIN
	INSERT INTO Albums_have_Artists (album_id, artist_id)
		VALUES (
			album_entry_id,
      artist_entry_id
    );
            
END //

DELIMITER ;

/*
stored procedure to remove an album from a users collection
*/
DELIMITER //

DROP PROCEDURE IF EXISTS sp_RemoveAlbumFromCollection;

CREATE PROCEDURE sp_RemoveAlbumFromCollection(IN input_user_id INT, IN input_album_id INT)
BEGIN
    DELETE FROM Albums_have_Owners WHERE user_id = input_user_id AND album_id = input_album_id;

END //
DELIMITER ;

/*
stored procedure to delete the specified diary_entry by Jorge Rodriguez and Antonio Olaguer II
*/

DELIMITER //

DROP PROCEDURE IF EXISTS sp_DeleteDiaryEntry;


CREATE PROCEDURE sp_DeleteDiaryEntry(IN input_diary_entry_id INT)
BEGIN
    DELETE from Diary_Entries WHERE diary_entry_id = input_diary_entry_id;

END //
DELIMITER ;
/*

stored procedure to get all artists by Jorge Rodriguez and Antonio Olaguer II

*/

DELIMITER //

DROP PROCEDURE IF EXISTS sp_GetArtists;


CREATE PROCEDURE sp_GetArtists()
BEGIN
    SELECT 
        artist_id, artist_name
    FROM
        Artists
    ORDER BY artist_name ASC;



END //
DELIMITER ;

/*
stored procedure to get all tracks by Jorge Rodriguez and Antonio Olaguer II

*/

DELIMITER //

DROP PROCEDURE IF EXISTS sp_GetTracks;


CREATE PROCEDURE sp_GetTracks()
BEGIN
    SELECT 
        track_id, track_title
    FROM
        Tracks
    ORDER BY track_id ASC;



END //
DELIMITER ;
/*
stored procedure to get user albums by Jorge Rodriguez and Antonio Olaguer II

*/

DELIMITER //

DROP PROCEDURE IF EXISTS sp_GetUserAlbums;


CREATE PROCEDURE sp_GetUserAlbums(IN input_id INT)
BEGIN
    SELECT 
        a.album_id, a.album_title,
        t.track_id, t.track_title,
        aht.track_order_num,
        ar.artist_id, ar.artist_name
            FROM Albums a
            JOIN Albums_have_Owners aho ON a.album_id = aho.album_id
            JOIN Users u ON u.user_id = aho.user_id
            JOIN Albums_have_Tracks aht ON a.album_id = aht.album_id
            JOIN Tracks t ON t.track_id = aht.track_id
            JOIN Artists_have_Tracks aht2 ON t.track_id = aht2.track_id
            JOIN Artists ar ON ar.artist_id = aht2.artist_id
            WHERE u.user_id = input_id
            ORDER BY a.album_id, aht.track_order_num;



END //
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS sp_GetUserJustAlbums;

CREATE PROCEDURE sp_GetUserJustAlbums(IN input_id INT)
BEGIN
    SELECT a.album_id, a.album_title
    FROM Albums a
    JOIN Albums_have_Owners aho ON a.album_id = aho.album_id
    WHERE aho.user_id = input_id;

END //
DELIMITER ;

/*
stored procedure to get all albums by Jorge Rodriguez and Antonio Olaguer II
*/

DELIMITER //
DROP PROCEDURE IF EXISTS sp_GetAllAlbums;

CREATE PROCEDURE sp_GetAllAlbums()
BEGIN
    SELECT a.album_id, a.album_title
    FROM Albums a;
END //

DELIMITER ;

/*
stored procedure to get diary_entries of specified user by Jorge Rodriguez and Antonio Olaguer II

*/

DELIMITER //

DROP PROCEDURE IF EXISTS sp_GetUserDiaries;


CREATE PROCEDURE sp_GetUserDiaries(IN input_id INT)
BEGIN
    SELECT 
        d.diary_entry_id, d.diary_entry_datetime, d.diary_entry, a.album_title
    FROM
        Diary_Entries as d
    JOIN
        Albums as a ON d.listened_to_album_id = a.album_id
    WHERE d.author_user_id = input_id
    ORDER BY diary_entry_datetime ASC;



END //
DELIMITER ;

/*
stored procedure to reset data by Jorge Rodriguez and Antonio Olaguer II
*/

DELIMITER //

DROP PROCEDURE IF EXISTS sp_ResetInitialData;


CREATE PROCEDURE sp_ResetInitialData()
BEGIN

SET FOREIGN_KEY_CHECKS = 0;

-- Albums: holds all the non-dependent information about an Album

DROP TABLE IF EXISTS Albums ;

CREATE TABLE Albums (
  album_id INT NOT NULL UNIQUE AUTO_INCREMENT,
  album_title VARCHAR(255) NOT NULL,
  album_label VARCHAR(255) NULL,
  album_country VARCHAR(255) NULL,
  album_year INT NULL,
  PRIMARY KEY (album_id)
);

-- Artists: holds all the non-depedent information about an Artist

DROP TABLE IF EXISTS Artists ;

CREATE TABLE Artists (
  artist_id INT NOT NULL UNIQUE AUTO_INCREMENT,
  artist_name VARCHAR(255) NOT NULL,
  PRIMARY KEY (artist_id)
);

-- Tracks: holds all the non-depedent information about a Track

DROP TABLE IF EXISTS Tracks ;

CREATE TABLE Tracks (
  track_id INT NOT NULL UNIQUE AUTO_INCREMENT,
  track_title VARCHAR(255) NOT NULL,
  PRIMARY KEY (track_id)
);

-- Users: holds all the non-depedent information about a User

DROP TABLE IF EXISTS Users ;

CREATE TABLE Users (
  user_id INT NOT NULL UNIQUE AUTO_INCREMENT,
  user_fname VARCHAR(255) NOT NULL,
  user_lname VARCHAR(255) NOT NULL,
  user_email VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY (user_id)
);

-- Diary Entries: holds all information about a Diary Entry, including references to what Album is the subject and which User wrote it

DROP TABLE IF EXISTS Diary_Entries ;

CREATE TABLE Diary_Entries (
  diary_entry_id INT NOT NULL UNIQUE AUTO_INCREMENT,
  diary_entry LONGTEXT NOT NULL,
  diary_entry_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  author_user_id INT NOT NULL,
  listened_to_album_id INT NOT NULL,
  PRIMARY KEY (diary_entry_id),
  CONSTRAINT fk_Diary_Entries_Users1
    FOREIGN KEY (author_user_id)
    REFERENCES Users (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Diary_Entries_Albums1
    FOREIGN KEY (listened_to_album_id)
    REFERENCES Albums (album_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);

-- Albums_have_Artists: intersection table which shows which Artists are associated with which Albums. One Album can have multiple Artists (such as a complication album) and one Artist can have multiple Albums

DROP TABLE IF EXISTS Albums_have_Artists ;

CREATE TABLE Albums_have_Artists (
  album_id INT NOT NULL,
  artist_id INT NOT NULL,
  PRIMARY KEY (album_id, artist_id),
  CONSTRAINT fk_Artists_has_Albums_Artists1
    FOREIGN KEY (artist_id)
    REFERENCES Artists (artist_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT fk_Artists_has_Albums_Albums1
    FOREIGN KEY (album_id)
    REFERENCES Albums (album_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);


-- Artists_have_Tracks: intersection table which shows which Tracks are associated with which Artists. One Artist can have many Tracks and one Track can have multiple Artists (such as a collaboration track)

DROP TABLE IF EXISTS Artists_have_Tracks ;

CREATE TABLE IF NOT EXISTS Artists_have_Tracks (
  track_id INT NOT NULL,
  artist_id INT NOT NULL,
  PRIMARY KEY (track_id, artist_id),
  CONSTRAINT fk_Tracks_has_Artists_Tracks1
    FOREIGN KEY (track_id)
    REFERENCES Tracks (track_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT fk_Tracks_has_Artists_Artists1
    FOREIGN KEY (artist_id)
    REFERENCES Artists (artist_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);

-- Albums_have_Tracks: intersection table which shows which Tracks are associated with which Albums. One Album can have many tracks and one track can appear on multiple Albums (such as anthologies or compilations)

DROP TABLE IF EXISTS Albums_have_Tracks ;

CREATE TABLE Albums_have_Tracks (
  track_id INT NOT NULL,
  album_id INT NOT NULL,
  track_order_num INT NOT NULL,
  PRIMARY KEY (track_id, album_id),
  CONSTRAINT fk_Tracks_has_Albums_Tracks1
    FOREIGN KEY (track_id)
    REFERENCES Tracks (track_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT fk_Tracks_has_Albums_Albums1
    FOREIGN KEY (album_id)
    REFERENCES Albums (album_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);

-- Albums_have_Owners: intersection table which shows which Users own which Albums. This is table essentially relates a User's collection of Albums.

DROP TABLE IF EXISTS Albums_have_Owners ;

CREATE TABLE Albums_have_Owners (
  album_id INT NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (album_id, user_id),
  CONSTRAINT fk_Albums_has_Users_Albums1
    FOREIGN KEY (album_id)
    REFERENCES Albums (album_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT fk_Albums_has_Users_Users1
    FOREIGN KEY (user_id)
    REFERENCES Users (user_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);

INSERT INTO Artists (artist_name)
VALUES (
    "Orquesta Aragon"
),
(
    "Fela Kuti"
),
(
    "Pierre Rassin et son Orchestre Antillais"
);

INSERT INTO Albums (
    album_title,
    album_label,
    album_country,
    album_year
)
VALUES (
    "Charleston Cha",
    "Areito",
    "Cuba",
    1966
),
(
    "Calpyso-Biguine-Merengue",
    "Disques Vogue",
    "Martinique",
    1966
),
(
    "Black President",
    "Capitol Records",
    "Nigeria",
    1981
);

INSERT INTO Tracks (track_title)
VALUES ("Sorrow Tears and Blood"),
    ("Colonial Mentality"),
    ("I.T.T."),
    ("El Paso de Encarnacion"),
    ("Tu No Sabes de Amor"),
    ("Si Envidia"),
    ("Jardinero del Amor"),
    ("Espero Tu Carta"),
    ("Cha-Cha-Cha de las Doce"),
    ("El Cuini Tiene Bandera"),
    ("Mi Charleston-Cha"),
    ("La Cancion de los Niños"),
    ("Mi Gallo Pinto"),
    ("Bella Perla del Sur"),
    ("Aleluya en Navidad"),
    ("Les Oignons"),
    ("Petite Fleur Fanee"),
    ("La Cruz"),
    ("Bon'm Siro A"),
    ("Felicia"),
    ("Fanagalo"),
    ("Madame Becassine"),
    ("Le Redoute"),
    ("Nhome Ka Pote Cone"),
    ("Tout Ca Ke Change"),
    ("Box Car Shorty"),
    ("Yoka");
    
INSERT INTO Albums_have_Artists (album_id, artist_id)
VALUES (
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
),
(
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT album_id FROM Albums WHERE album_title="Black President"),
    (SELECT artist_id FROM Artists WHERE artist_name="Fela Kuti")
);

INSERT INTO Artists_have_Tracks (track_id, artist_id)
VALUES (
    (SELECT track_id FROM Tracks WHERE track_title="Sorrow Tears and Blood"),
    (SELECT artist_id FROM Artists WHERE artist_name="Fela Kuti")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Colonial Mentality"),
    (SELECT artist_id FROM Artists WHERE artist_name="Fela Kuti")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="I.T.T."),
    (SELECT artist_id FROM Artists WHERE artist_name="Fela Kuti")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="El Paso de Encarnacion"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Tu No Sabes de Amor"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Si Envidia"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Jardinero del Amor"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Espero Tu Carta"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Cha-Cha-Cha de las Doce"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="El Cuini Tiene Bandera"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Mi Charleston-Cha"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="La Cancion de los Niños"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Mi Gallo Pinto"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Bella Perla del Sur"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Aleluya en Navidad"),
    (SELECT artist_id FROM Artists WHERE artist_name="Orquesta Aragon")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Les Oignons"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Petite Fleur Fanee"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="La Cruz"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Bon'm Siro A"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Felicia"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Fanagalo"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Madame Becassine"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Le Redoute"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Nhome Ka Pote Cone"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Tout Ca Ke Change"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Box Car Shorty"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Yoka"),
    (SELECT artist_id FROM Artists WHERE artist_name="Pierre Rassin et son Orchestre Antillais")
);

INSERT INTO Albums_have_Tracks (track_id, album_id, track_order_num)
VALUES (
    (SELECT track_id FROM Tracks WHERE track_title="Sorrow Tears and Blood"),
    (SELECT album_id FROM Albums WHERE album_title="Black President"),
    1
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Colonial Mentality"),
    (SELECT album_id FROM Albums WHERE album_title="Black President"),
    2
),
(
    (SELECT track_id FROM Tracks WHERE track_title="I.T.T."),
    (SELECT album_id FROM Albums WHERE album_title="Black President"),
    3
),
(
    (SELECT track_id FROM Tracks WHERE track_title="El Paso de Encarnacion"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    1
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Tu No Sabes de Amor"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    2
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Si Envidia"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    3
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Jardinero del Amor"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    4
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Espero Tu Carta"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    5
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Cha-Cha-Cha de las Doce"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    6
),
(
    (SELECT track_id FROM Tracks WHERE track_title="El Cuini Tiene Bandera"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    7
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Mi Charleston-Cha"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    8
),
(
    (SELECT track_id FROM Tracks WHERE track_title="La Cancion de los Niños"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    9
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Mi Gallo Pinto"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    10
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Bella Perla del Sur"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    11
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Aleluya en Navidad"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    12
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Les Oignons"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    1
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Petite Fleur Fanee"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    2
),
(
    (SELECT track_id FROM Tracks WHERE track_title="La Cruz"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    3
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Bon'm Siro A"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    4
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Felicia"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    5
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Fanagalo"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    6
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Madame Becassine"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    7
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Le Redoute"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    8
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Nhome Ka Pote Cone"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    9
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Tout Ca Ke Change"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    10
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Box Car Shorty"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    11
),
(
    (SELECT track_id FROM Tracks WHERE track_title="Yoka"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    12
);

INSERT INTO Users (user_fname, user_lname, user_email)
VALUES ("Jorge", "Rodriguez", "jorge@fakemail.com"),
       ("Antonio", "Olaguer", "antonio@fakemail.com"),
       ("Record", "Collectorman", "recordguy@fakemail.com");
       
INSERT INTO Albums_have_Owners (album_id, user_id)
VALUES (
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue"),
    (SELECT user_id FROM Users WHERE user_email="jorge@fakemail.com")
),
(
    (SELECT album_id FROM Albums WHERE album_title="Black President"),
    (SELECT user_id FROM Users WHERE user_email="jorge@fakemail.com")
),
(
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    (SELECT user_id FROM Users WHERE user_email="jorge@fakemail.com")
),
(
    (SELECT album_id FROM Albums WHERE album_title="Black President"),
    (SELECT user_id FROM Users WHERE user_email="antonio@fakemail.com")
),
(
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha"),
    (SELECT user_id FROM Users WHERE user_email="recordguy@fakemail.com")
);

INSERT INTO Diary_Entries (diary_entry, diary_entry_datetime, author_user_id, listened_to_album_id)
VALUES (
    "I've never heard music from Martinique, absolutely fascinating album. I've heard of Calypso and Merengue, but never Biguine. Very fun listening experience!",
    "2024-10-24 14:30:00",
    (SELECT user_id FROM Users WHERE user_email="jorge@fakemail.com"),
    (SELECT album_id FROM Albums WHERE album_title="Calpyso-Biguine-Merengue")
),
(
    "One of my favorite Fela albums. I never get tired of listening to Sorrow Tears and Blood.",
    "2023-11-24 14:30:00",
    (SELECT user_id FROM Users WHERE user_email="antonio@fakemail.com"),
    (SELECT album_id FROM Albums WHERE album_title="Black President")
),
(
    "Love listening to Cuban music. This one is special because it is a record pressed in Cuba, from the label Areito. Very rare!",
    "2024-04-24 14:30:00",
    (SELECT user_id FROM Users WHERE user_email="recordguy@fakemail.com"),
    (SELECT album_id FROM Albums WHERE album_title="Charleston Cha")
);

SET FOREIGN_KEY_CHECKS=1;

END //
DELIMITER ;

