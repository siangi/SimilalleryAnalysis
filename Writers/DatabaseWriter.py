from Writers.WriterBase import WriterBase
from ImageAnalysisData import ImageAnalysisData
import mysql.connector
import connection

class MySqlWriter(WriterBase):
    def __init__(self) -> None:
        super().__init__()
        self.connection = None

    def prepare(self):
        self.connection = mysql.connector.connect(host=connection.host, username=connection.username, password=connection.password, database="scheme_test_similallery")
        
    # map the analysis values to the correct columns and insert it
    def writeRow(self, sourceRow: dict, analysisResult: ImageAnalysisData, artistBio: tuple):
        INSERT_QUERY = """INSERT INTO `scheme_test_similallery`.`image`
            (`title`,
            `year`,
            `URL`,
            `artist_id`,
            `category_id`,
            `h_1`, `s_1`, `l_1`,
            `h_2`, `s_2`, `l_2`, 
            `h_3`, `s_3`, `l_3`,
            `h_4`, `s_4`, `l_4`,
            `h_5`, `s_5`, `l_5`,
            `pal_ratio_1`, `pal_ratio_2`, `pal_ratio_3`, `pal_ratio_4`, `pal_ratio_5`,
            `angle_ratio_1`, `angle_ratio_2`, `angle_ratio_3`, `angle_ratio_4`, `angle_ratio_5`, 
            `angle_ratio_6`, `angle_ratio_7`, `angle_ratio_8`, 
            `sal_center_x`,
            `sal_center_y`,
            `sal_rect_x`,
            `sal_rect_y`,
            `sal_rect_width`,
            `sal_rect_height`)
            VALUES
            (%(title)s,
            %(year)s,
            %(URL)s,
            %(artistID)s,
            %(categoryID)s,
            %(h1)s, %(s1)s, %(l1)s,
            %(h2)s, %(s2)s, %(l2)s,
            %(h3)s, %(s3)s, %(l3)s,
            %(h4)s, %(s4)s, %(l4)s,
            %(h5)s, %(s5)s, %(l5)s,
            %(palRatio1)s,%(palRatio2)s,%(palRatio3)s,%(palRatio4)s,%(palRatio5)s,
            %(angleRatio1)s, %(angleRatio2)s, %(angleRatio3)s, %(angleRatio4)s, 
            %(angleRatio5)s, %(angleRatio6)s, %(angleRatio7)s, %(angleRatio8)s,
            %(salCenterX)s,
            %(salCenterY)s,
            %(salRectX)s,
            %(salRectY)s,
            %(salRectWidth)s,
            %(salRectHeight)s);
            """
        artistID = self._getArtistID(artistBio[0], artistBio[1])
        categoryID = self._getCategoryID(sourceRow["Category"])

        cursor = self.connection.cursor(buffered=True)
        try:
            datadict = {
                "title": sourceRow["Title"].strip(),
                "year": sourceRow["Year"],
                "URL": sourceRow["URL"],
                "artistID": artistID,
                "categoryID": categoryID,
                "h1": analysisResult.colorPalette[0]["h"],
                "s1": analysisResult.colorPalette[0]["s"],
                "l1": analysisResult.colorPalette[0]["l"],
                "h2": analysisResult.colorPalette[1]["h"],
                "s2": analysisResult.colorPalette[1]["s"],
                "l2": analysisResult.colorPalette[1]["l"],
                "h3": analysisResult.colorPalette[2]["h"],
                "s3": analysisResult.colorPalette[2]["s"],
                "l3": analysisResult.colorPalette[2]["l"],
                "h4": analysisResult.colorPalette[3]["h"],
                "s4": analysisResult.colorPalette[3]["s"],
                "l4": analysisResult.colorPalette[3]["l"],
                "h5": analysisResult.colorPalette[4]["h"],
                "s5": analysisResult.colorPalette[4]["s"],
                "l5": analysisResult.colorPalette[4]["l"],
                "palRatio1": analysisResult.paletteRatios[0],
                "palRatio2": analysisResult.paletteRatios[1],
                "palRatio3": analysisResult.paletteRatios[2],
                "palRatio4": analysisResult.paletteRatios[3],
                "palRatio5": analysisResult.paletteRatios[4],
                "angleRatio1": analysisResult.angleRatios[0],
                "angleRatio2": analysisResult.angleRatios[1],
                "angleRatio3": analysisResult.angleRatios[2],
                "angleRatio4": analysisResult.angleRatios[3],
                "angleRatio5": analysisResult.angleRatios[4],
                "angleRatio6": analysisResult.angleRatios[5],
                "angleRatio7": analysisResult.angleRatios[6],
                "angleRatio8": analysisResult.angleRatios[7],
                "salCenterX": analysisResult.saliencyCenter[0],
                "salCenterY": analysisResult.saliencyCenter[1],
                "salRectX": analysisResult.saliencyRect[0],
                "salRectY": analysisResult.saliencyRect[1],
                "salRectWidth": analysisResult.saliencyRect[2],
                "salRectHeight": analysisResult.saliencyRect[3],
            }
            
            cursor.execute(INSERT_QUERY, datadict)
            self.connection.commit()
        except Exception as err:
            print(err)
        finally:
            cursor.close()
    
    # find or insert the right category
    def _getCategoryID(self, category: str):
        SELECT_QUERY = "SELECT idcategory FROM category WHERE name = %(name)s"
        INSERT_QUERY = "INSERT INTO `scheme_test_similallery`.`category`(`name`) VALUES (%(name)s);"
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(SELECT_QUERY, {"name": category.strip()})
        try:
            if (cursor.rowcount > 1):
                raise Exception("illegal Database state, duplicate category")
            elif (cursor.rowcount == 1):
                return cursor.fetchone()[0]
            else:
                cursor.execute(INSERT_QUERY, {"name": category.strip()})
                return cursor.lastrowid
        except Exception as err:
            print(err)
        finally:
            cursor.close()
    
    # find or insert the right artist
    def _getArtistID(self, artist:str, nationality:str):
        SELECT_QUERY = "SELECT `artist`.`idartist` FROM `scheme_test_similallery`.`artist` WHERE `name` = %(name)s AND nationalityID = %(nationalityId)s;"
        INSERT_QUERY = "INSERT INTO `scheme_test_similallery`.`artist` (`name`, `nationalityID`) VALUES (%(name)s, %(nationalityId)s);"
        nationalityId = self._getNationalityID(nationality)
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(SELECT_QUERY, {"name": artist.strip(), "nationalityId": nationalityId})
        try:
            if(cursor.rowcount > 1):
                raise Exception("illegal Database state, duplicate artist")
            elif(cursor.rowcount == 1):
                return cursor.fetchone()[0]
            else:
                cursor.execute(INSERT_QUERY, {"name": artist.strip(), "nationalityId": nationalityId})
                return cursor.lastrowid
        except Exception as err:
            print(err)
        finally:
            cursor.close()

    # find or insert the right nationality
    def _getNationalityID(self, nationality):
        SELECT_QUERY = "SELECT `nationality`.`idnationality` FROM `scheme_test_similallery`.`nationality` WHERE `nationality`.`name` = %(nationality)s"
        INSERT_QUERY = "INSERT INTO `scheme_test_similallery`.`nationality` (`name`) VALUES (%(nationality)s);"
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(SELECT_QUERY, {"nationality": nationality.strip()})
        try: 
            if(cursor.rowcount > 1):
                raise Exception("illegal Database state, duplicate Nationality")
            elif(cursor.rowcount == 1):
                return cursor.fetchone()[0]
            else:
                cursor.execute(INSERT_QUERY, {"nationality": nationality.strip()})
                return cursor.lastrowid  
        except Exception as err:
            print(err)
        finally:
            cursor.close()

    def cleanup(self):
        self.connection.close()