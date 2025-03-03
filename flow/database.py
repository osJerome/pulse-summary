import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection


def connect_database(name: str, user: str, password: str, host: str, port: int) -> connection | None:
    try:
        conn = psycopg2.connect(
            dbname=name,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        
        return conn
    except Exception as e:
        print(f"[database.py -> connect_database] Unable to create a connection, {str(e)}")
        return None


def retrieve_pulse_information(conn: connection) -> list[dict]:
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # CONTEXT: The query will retrieve the required pulse contextual information for summarization
    # TODO: These pulse information SHOULD be batched; the order MUST follow by the hour of its created date

    query = """
        SELECT
            n.description,
            n.pulse_id,
            n.organization_id, 
            m.content
        AS
            message_content,
            m.user_id
        FROM
            notifications n
        JOIN
            messages m
        ON
            n.organization_id = m.organization_id
    """

    try:
        cursor.execute(query)
        pulse_information = cursor.fetchall()
        cursor.close()

        return pulse_information
    except Exception as e:
        print(f"[database.py -> retrieve_pulse_information] Unable to retrieve pulse information, {str(e)}")
        cursor.close()
        return []


def save_summaries(conn: connection, summaries: list[dict]) -> bool:
    cursor = conn.cursor()
    
    try:
        for i, row in enumerate(summaries):
            query = """
            UPDATE
                pulses
            SET
                summary = %s,
                updated_at = NOW()
            WHERE
                id = %s
            """
            
            try:
                cursor.execute(
                    query, 
                    (
                        row['summary'],
                        row['pulse_id']
                    )
                )
                print(f"Saved summary {i + 1} of {len(summaries)}")
            except Exception as e:
                print(f"Error updating summary in database: {e}")
        
        conn.commit()
        cursor.close()
        print(f"Successfully saved {len(summaries)} summaries.")
        return True
    except Exception as e:
        print(f"[database.py -> save_summaries] Unable to save summaries, {str(e)}")
        return False