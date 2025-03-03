from os import getenv
from dotenv import load_dotenv

from flow.utils import normalize_data
from flow.summarizer import generate_summaries
from flow.database import connect_database, retrieve_pulse_information, save_summaries


load_dotenv()


def main():
    # Connect to database
    conn = connect_database(
        host=getenv("DB_HOST"),
        name=getenv("DB_NAME"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
    )
    if not conn:
        return

    try:
        # Fetch data from notifications and messages tables
        pulse_information = retrieve_pulse_information(conn)

        if not pulse_information:
            print("None or insufficient data to proceed for pulse summarization.")
            conn.close()
            return

        # Normalize the data
        normalized_data = normalize_data(pulse_information)

        # Generate summaries using LangChain
        data_with_summaries = generate_summaries(normalized_data)

        # Save summaries to pulses summary table; disable for testing
        # save_summaries(conn, data_with_summaries)

        print(f"Successfully processed {len(data_with_summaries)} records.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
