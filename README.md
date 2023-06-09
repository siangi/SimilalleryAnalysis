# SimilalleryAnalysis

Analyses Saliency, Gradient Orientation and Color Palette of all Images linked in a CSV.
When Analysis is done it writes all the results and the metadata from the same csv into a database.

To run it you need the database ready, the databse data is in the [SimilalleryAPI Repository](https://github.com/siangi/SimilalleryAPI). Also you will need to enter the proper csvPath in AnalysisController.py and install everything from requirements.txt

Once you've done all that, start the analysis with:

### `python AnalysisController.py`
