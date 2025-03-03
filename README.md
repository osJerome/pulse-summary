# Pulse Summary Flow

A Python application that fetches data from a PostgreSQL database, processes it, and generates AI-powered pulse summaries using LangChain.

## Setup and Installation

### Prerequisites

- Python 3.7+
- PostgreSQL database

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pulse-summary.git
   cd pulse-summary
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database connection:
   
   Open `database.py` and update the database connection parameters:
   ```python
   conn = psycopg2.connect(
       dbname="your_database",
       user="your_username",
       password="your_password",
       host="your_host",
       port="your_port"
   )
   ```

5. Set your OpenAI API key:
   ```bash
   # On Windows
   set OPENAI_API_KEY=your_openai_api_key
   
   # On macOS/Linux
   export OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

Run the application with:
```bash
python main.py
```

The application will:
1. Connect to your PostgreSQL database
2. Fetch relevant data from the notifications and messages tables
3. Normalize the data
4. Generate concise summaries using OpenAI via LangChain
5. Save the summaries to the feeds table in your database

## Project Structure

- `main.py`: Entry point that orchestrates the workflow
- `database.py`: Database connection and query functions
- `utils.py`: Data normalization utilities
- `summarizer.py`: AI-powered summary generation logic
