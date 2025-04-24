# 📚 babel

A Streamlit webpage app for keeping record of my library.

## Features

- View and explore your library database in a tabular format.
- Add new entries to the library.
- Edit existing entries in the library.
- Search for books by various fields (e.g., title, author, year, etc.).
- Delete entries from the library.
- Create automatic backups of the library database.
- Clear old backups, keeping only the most recent one.

## Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `streamlit`
  - `pandas`
  - `rich`

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd babel
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py --db_path <path_to_your_database>
   ```

## Usage

1. Provide the path to your library database file (CSV format) using the `--db_path` argument.
2. Use the Streamlit interface to:
   - View and search your library.
   - Add, edit, or delete entries.
   - Manage backups.

## Database Format

The library database should be a CSV file with the following columns:
- `autor/a`: Author of the book.
- `título`: Title of the book.
- `título original`: Original title of the book.
- `traductor/a`: Translator of the book.
- `editorial`: Publisher of the book.
- `año publicacion`: Year of publication.
- `año edicion`: Year of edition.
- `idioma`: Language of the book.
- `etiquetas`: Tags associated with the book (separated by semicolons).

## Backup Management

The app automatically creates backups of the database in the `databases/backups` folder. You can clear old backups using the "Clear backups" button in the sidebar.

## Contributing

Feel free to submit issues or pull requests to improve this project.

## License

This project is licensed under the MIT License.
