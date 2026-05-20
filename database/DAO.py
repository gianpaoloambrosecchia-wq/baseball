from database.DB_connect import DBConnect
from model.team import Team


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinct (t.year)
                    from teams t
                    where t.year >= 1980
                    """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getTeamsOfYear(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select *
                    from teams t
                    where t.year = %s
                    """

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getSalariesOfTeam(year, idMapTeams):
        conn = DBConnect.get_connection()



        cursor = conn.cursor(dictionary=True)

        query = """select t.ID, t.teamCode, sum(s.salary) as totSalary
                    from salaries s, teams t, appearances a
                    where s.year = t.year and t.year = a.year and a.year = %s
                          and t.ID = a.teamID and s.playerID = a.playerID
                    group by t.ID, t.teamCode
                    """

        cursor.execute(query, (year,))

        mapSalary = {}
        for row in cursor:
            # Uso una mappa con chiave i team e valore la somma dei salari (non serve appendere ad una lista)
            mapSalary[idMapTeams[row["ID"]]] = row["totSalary"]

        cursor.close()
        conn.close()
        return mapSalary

