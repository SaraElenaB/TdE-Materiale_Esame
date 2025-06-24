
class DAO():

    @staticmethod
    def getAllAnni():
        conn = DBConnect.get_connection()
        ris=[]
        cursor = conn.cursor(dictionary=True)

        query="""  """
        cursor.execute(query)

        for row in cursor:
            ris.append( row[" "])

        cursor.close()
        conn.close()
        return ris