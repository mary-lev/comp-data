
class Processor():
    """
        The base class for the processors.
        The variable path_url containing the path or the URL of the database, 
        initially set as an empty string, that will be updated with the method setDbPathOrUrl.
        """
    dbPathOrUrl = ""

    def __init__(self, path_url: str = ""):
        self.dbPathOrUrl = path_url

    def getDbPathOrUrl(self) -> str: 
        """it returns the path or URL of the database."""
        return self.dbPathOrUrl

    def setDbPathOrUrl(self, path_url: str):
        """it enables to set a new path or URL for the database to handle."""
        self.dbPathOrUrl = path_url


class QueryProcessor(Processor):

    def getEntityById():
        """it returns a data frame with all the entities matching the input identifier (i.e. maximum one entity)."""
        pass
