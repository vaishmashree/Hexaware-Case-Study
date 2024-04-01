import pyodbc
from dao.IVirtualArtGallery import IVirtualArtGallery
from util.DBConnection import DBConnection
from exception.Artworkid_exception import ArtworkIdNotFoundException
from exception.Userid_exception import UserIdNotFoundException
from entity.artwork import Artwork
from typing import List, Tuple

class VirtualArtGalleryimpl(IVirtualArtGallery):
    def __init__(self):
        self.conn = DBConnection.getConnection()
        self.cursor = self.conn.cursor()

    def __del__(self):
        if self.conn is not None and not self.conn.closed:
            self.conn.close()

    def addArtwork(self, artwork: Artwork) -> bool:
        try:
            self.cursor.execute("""INSERT INTO Artwork VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                (artwork.getArtworkId(), artwork.getTitle(), artwork.getDescription(),
                                 artwork.getCreationDate(), artwork.getMedium(), artwork.getImageUrl(), artwork.getArtistId()))
            self.conn.commit()
            return True
        except pyodbc.Error as err:
            print(f"Artwork cannot be added : {err}")
            return False
    
    def updateArtwork(self, artwork: Artwork) -> bool:
        try:
            self.cursor.execute("""UPDATE Artwork SET Title=?, Description=?, CreationDate=?, Medium=?, ImageURL=?, ArtistID=?
                                WHERE ArtworkID=?""",
                                (artwork.getTitle(), artwork.getDescription(), artwork.getCreationDate(),
                                 artwork.getMedium(), artwork.getImageUrl(), artwork.getArtistId(), artwork.getArtworkId()))
            self.conn.commit()
            return True
        except pyodbc.Error as err:
            print(f"Artwork cannot be updated : {err}")
            return False

    def removeArtwork(self, artworkid) -> bool:
        try:
            self.cursor.execute("""DELETE FROM Artwork WHERE ArtworkID=?""", (artworkid,))
            self.conn.commit()
            return True
        except pyodbc.Error as err:
            print(f"Artwork cannot be deleted : {err}")
            return False     
            
    def getArtworkById(self, artworkid) -> Artwork:
        try:
            self.cursor.execute("""SELECT * FROM Artwork WHERE ArtworkID=?""", (artworkid,))
            result = self.cursor.fetchone()
            if result:
                artwork = Artwork(*result)
                return artwork
            else:
                raise ArtworkIdNotFoundException(artworkid)
        except ArtworkIdNotFoundException as err:
            print(f"Exception : {err}")
            return []

    def searchArtworks(self, keyword: str) -> List[Tuple[str]]:
        try:
            self.cursor.execute("""SELECT * FROM Artwork WHERE Title LIKE ?""", ('%' + keyword + '%',))
            records = self.cursor.fetchall()
            if records:
                artworks = [(str(record[0]), record[1], record[2], record[3], record[4], record[5]) for record in records]
                return artworks
            else:
                print("No artworks found with the given keyword.")
                return []
        except pyodbc.Error as e:
            print(f"Error fetching artworks: {e}")
            return []

    def addArtworkToFavorite(self, userid, artworkid) -> bool:
        try:
            self.cursor.execute("""INSERT INTO User_Favorite_Artwork (UserID, ArtworkID) VALUES (?, ?)""", (userid, artworkid))
            self.conn.commit()
            return True
        except pyodbc.Error as err:
            print(f"Artwork cannot be added to favorite: {err}")
            return False

    def removeArtworkFromFavorite(self, userId, artworkId) -> bool:
        try:
            self.cursor.execute("""DELETE FROM User_Favorite_Artwork WHERE UserID=? AND ArtworkID=?""", (userId, artworkId))
            self.conn.commit()
            return True
        except pyodbc.Error as err:
            print(f"Artwork cannot be removed from favorites: {err}")
            return False

    def getUserFavoriteArtworks(self, userId) -> bool:
        try:
            self.cursor.execute("""
                SELECT a.*
                FROM Users u
                JOIN User_Favorite_Artwork uf ON u.UserID = uf.UserID
                JOIN Artwork a ON uf.ArtworkID = a.ArtworkID
                WHERE u.UserID = ?
            """, (userId,))
            result = self.cursor.fetchall()
            if result:
                print(f"Favorite artworks for user {userId}:")
                for row in result:
                    artwork_id, title, description, creation_date, medium, image_url, artist_id = row
                    print(f"Artwork ID: {artwork_id}")
                    print(f"Title: {title}")
                    print(f"Description: {description}")
                    print(f"Creation Date: {creation_date}")
                    print(f"Medium: {medium}")
                    print(f"Image URL: {image_url}")
                    print(f"Artist ID: {artist_id}")
                return True
            else:
                raise UserIdNotFoundException(userId)
        except pyodbc.Error as err:
            print(f"User favorite artwork cannot be able to display : {err}")

    def searchGalleries(self, keyword: str) -> List[Tuple[str]]:
        try:
            self.cursor.execute("""SELECT * FROM Gallery WHERE Name LIKE ?""", ('%' + keyword + '%',))
            records = self.cursor.fetchall()
            if records:
                galleries = [(record[0], record[1], record[2], record[3], record[4], record[5]) for record in records]
                return galleries
            else:
                print("No galleries found with the given keyword.")
                return []
        except pyodbc.Error as e:
            print(f"Error fetching galleries: {e}")
            return []
