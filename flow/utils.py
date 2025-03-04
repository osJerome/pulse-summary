import json


def normalize_data(data: list[dict]) -> list[dict]:
    normalized_data = []

    try:
        for row in data:
            normalized_row = dict(row)

            # Combine relevant text data for summarization
            normalized_row["combined_text"] = (
                f"Description: {normalized_row['description'] or ''}\n"
                f"Message: {normalized_row['message_content'] or ''}"
            )

            normalized_data.append(normalized_row)

        return normalized_data
    except Exception as e:
        print(f"[utils.py -> normalize_data] Unable to normalize data, {str(e)}")
        return []
