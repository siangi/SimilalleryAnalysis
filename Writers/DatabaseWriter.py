from Writers.WriterBase import WriterBase
from ImageAnalysisData import ImageAnalysisData
import mysql.connector
import connection.py

class MySqlWriter(WriterBase):
    def __init__(self) -> None:
        super().__init__()
        self.connection = None

    def prepare(self):
        self.connection = mysql.connector.connect(host=connection.host, username=connection.username, password=connection.password)
        pass

    def writeRow(self, sourceRow: dict, analysisResult: ImageAnalysisData):
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
            %(year)i,
            %(URL)s,
            %(artistID)i,
            %(categoryID)i,
            %(h1)i, %(s1)i, %(l1)i,
            %(h2)i, %(s2)i, %(l2)i,
            %(h3)i, %(s3)i, %(l3)i,
            %(h4)i, %(s4)i, %(l4)i,
            %(h5)i, %(s5)i, %(l5)i,
            %(palRatio2)f,%(palRatio3)f,%(palRatio1)f,%(palRatio4)f,%(palRatio5)f,
            %(angleRatio1)f, %(angleRatio2)f, %(angleRatio3)f, %(angleRatio4)f, 
            %(angleRatio5)f, %(angleRatio6)f, %(angleRatio7)f, %(angleRatio8)f,
            %(salCenterX)i,
            %(salCenterY)i,
            %(salRectX)i,
            %(salRectY)i,
            %(salRectWidth)i,
            %(salRectHeight)i);
            """
        artistID = self._getArtistID(sourceRow["Artist"])
        categoryID = self._getCategoryID(sourceRow["Category"])
        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execture(INSERT_QUERY, {
                "title": sourceRow["Title"],
                "year": sourceRow["Year"],
                "URL": sourceRow["URL"],
                "artistID": artistID,
                "categoryID": categoryID,
                "h1": analysisResult.colorPalette[0].h,
                "s1": analysisResult.colorPalette[0].s,
                "l1": analysisResult.colorPalette[0].l,
                "h2": analysisResult.colorPalette[1].h,
                "s2": analysisResult.colorPalette[1].s,
                "l2": analysisResult.colorPalette[1].l,
                "h3": analysisResult.colorPalette[2].h,
                "s3": analysisResult.colorPalette[2].s,
                "l3": analysisResult.colorPalette[2].l,
                "h4": analysisResult.colorPalette[3].h,
                "s4": analysisResult.colorPalette[3].s,
                "l4": analysisResult.colorPalette[3].l,
                "h5": analysisResult.colorPalette[4].h,
                "s5": analysisResult.colorPalette[4].s,
                "l5": analysisResult.colorPalette[4].l,
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
            })

            print(cursor.lastrowid())
        finally:
            cursor.close()
    
    def _getCategoryID(self, category: str):
        SELECT_QUERY = "SELECT idcategory FROM category WHERE name = %(name)"
        INSERT_QUERY = "INSERT INTO `scheme_test_similallery`.`category`(`name`) VALUES (`%(name)s`);"
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(SELECT_QUERY, {"name": category.strip()})
        try:
            if (cursor.rowcount > 1):
                raise Exception("illegal Database state, duplicate category")
            elif (cursor.rowcount == 1):
                return cursor.fetchone()
            else:
                cursor.execute(INSERT_QUERY, {"name": category.strip()})
                return cursor.lastrowid()
        finally:
            cursor.close()
    

    def _getArtistID(self, artist):
        SELECT_QUERY = "SELECT `artist`.`idartist` FROM `scheme_test_similallery`.`artist` WHERE `name` = %(name)s;"
        INSERT_QUERY = "INSERT INTO `scheme_test_similallery`.`artist` (`name`) VALUES %(name)s;"
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(SELECT_QUERY, {"name": artist.strip()})
        try:
            if(cursor.rowcount > 1):
                raise Exception("illegal Database state, duplicate artist")
            elif(cursor.rowcount == 1):
                return cursor.fetchone()
            else:
                cursor.execute(INSERT_QUERY, {"name": artist.strip()})
                return cursor.fetchone()
        finally:
            cursor.close()

    def cleanup(self):
        self.connection.close()