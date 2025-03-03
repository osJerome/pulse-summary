import json


def normalize_data(data: list[dict]) -> list[dict]:
    normalized_data = []

    try:
        for row in data:
            normalized_row = dict(row)

            # Convert metadata from JSON to string if it's not already a string
            if isinstance(normalized_row["metadata"], (dict, list)):
                normalized_row["metadata"] = json.dumps(normalized_row["metadata"])
            elif normalized_row["metadata"] is None:
                normalized_row["metadata"] = ""

            # Combine relevant text data for summarization
            normalized_row["combined_text"] = (
                f"Description: {normalized_row['description'] or ''}\n"
                f"Metadata: {normalized_row['metadata'] or ''}\n"
                f"Message: {normalized_row['message_content'] or ''}"
            )

            normalized_data.append(normalized_row)

        return normalized_data
    except Exception as e:
        print(f"[utils.py -> normalize_data] Unable to normalize data, {str(e)}")
        return []
