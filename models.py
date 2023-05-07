# Importa as bibliotecas
import psycopg2
import urllib.parse as up
import os
from dotenv import load_dotenv

# Classe Materia (model)
class Materia:
    # Configura o arquivo do banco de dados
    def __init__(self) -> None:
        """
            Model de matéria.
        """

        load_dotenv()

        up.uses_netloc.append("postgres")
        url = up.urlparse(os.environ["DATABASE_URL"])

        self.conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cur = self.conn.cursor()

    def create(self, materia: str, tipo: str) -> None:
        """
            Cria uma nova matéria no banco de dados.

            Uma matéria tem o seu nome (ex: História) e o seu tipo (se é exata, humana ou linguagem).

            Parâmetros:
                materia - Matéria a ser adicionada
                tipo - Tipo da matéria a ser adicionada
        """

        self.cur.execute(
            f"""
                INSERT
                INTO    materias
                        (materia, tipo)
                VALUES
                        ('{materia}', '{tipo}')
            """
        )

        self.conn.commit()
    def get(self, order_by: str = "", order: str = "ASC") -> dict:
        """
            Obtêm todas as matérias cadastradas no banco de dados e as retorna como uma lista de tuplas, onde cada tupla é uma linha do banco.
        """

        if not order_by == "":
            self.cur.execute(
                f"""
                    SELECT      *
                    FROM        materias
                    ORDER BY    {order_by} {order}
                """
            )
        else:
            self.cur.execute(
                f"""
                    SELECT  *
                    FROM    materias
                """
            )

        rows = self.cur.fetchall()
        table = []

        # Transforma a lista de tuplas que o sqlite3 retorna em um array de dicionários (mais semelhante ao JSON)
        for row_data in rows:
            row = {
                "materia": row_data[0],
                "tipo": row_data[1]
            }

            table.append(row)

        return table
    def update(self, materiaToUpdate: str, newMateria: str, newTipo: str) -> None:
        """
            Atualiza uma matéria no banco de dados.

            Parâmetros:
                materiaToUpdate - matéria existente no banco a ser atualizada
                newMateria - Nova matéria
                newTipo - Novo tipo de matéria
        """

        self.cur.execute(
            f"""
                UPDATE  materias
                SET
                        materia = '{newMateria}',
                        tipo    = '{newTipo}'
                WHERE   materia = '{materiaToUpdate}'
            """
        )

        self.conn.commit()
    def delete(self, materia: str) -> None:
        """
            Deleta uma matéria do banco de dados.

            Parâmetros:
                materia - Matéria a ser deletada do banco.
        """

        self.cur.execute(
            f"""
                DELETE
                FROM    materias
                WHERE   materia = '{materia}'
            """
        )

        self.conn.commit()
