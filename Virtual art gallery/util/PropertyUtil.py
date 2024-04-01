class PropertyUtil:
    @staticmethod
    def getPropertyString():
        hostname = "HP\SQLEXPRESS"
        dbname = "VirtualArt"
    
        connection_string = (
            f'Driver={{SQL Server}};'
            f'Server={hostname};'
            f'Database={dbname};'
        )
        return connection_string








