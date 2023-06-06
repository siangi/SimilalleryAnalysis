from Writers.WriterBase import WriterBase
import csv

# I used this to test the analysis before the databse existed. 
#It's not in use anymore.
class CSVWriter(WriterBase):
    def __init__(self, path) -> None:
        self.path = path
        self.writeFile = None
        self.writer = None

    def prepare(self, Header):
        self.writeFile = open(self.path, "w", encoding="utf8", newline="")
        self.writer = csv.DictWriter(f=self.writeFile, fieldnames=Header, delimiter=";")
        self.writer.writeheader()
    
    def writeRow(self, sourceRow, analysisResult):
        writeDict = self._createResultRow(sourceRow, analysisResult)
        self.writer.writerow(writeDict)

    def _createResultRow(self, sourceRow, analysisResult):
        sourceRow.update(vars(analysisResult))
        return sourceRow