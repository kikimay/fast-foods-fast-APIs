import psycopg2


class DatabaseConnection(object):
    def DBConnection(self):
        conn_parameters = 'dbname = fast_food_fast user = fast_foods password = kikimay host = localhost'
        try:
            self.connection = psycopg2.connect(conn_parameters)

            return self.connection

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    
    
conn = DatabaseConnection().DBConnection()
cur = conn.cursor()

def save(DatabaseConnection):
        cur.close()
        DatabaseConnection.DBConnection.self.connection.commit()
