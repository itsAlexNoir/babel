# 📚 Babel

A Streamlit web application for managing a personal library catalog. Babel provides an intuitive interface to organize, search, and maintain records of your book collection.

## ✨ Features

- **Browse Library**: View and explore your library database in interactive table and dataframe formats
- **Search Functionality**: Search for books by various fields (title, author, year, language, tags, etc.)
- **Add Entries**: Easily add new books to your library
- **Edit Entries**: Modify existing book records
- **Delete Entries**: Remove books from your library
- **Automatic Backups**: Create automatic backups of your library database
- **Backup Management**: Clear old backups while preserving the most recent ones

## 📋 Requirements

- **Python**: 3.13 or higher
- **Dependencies**:
  - `streamlit` (>=1.48.1) - Web app framework
  - `pandas` (>=2.3.1) - Data manipulation
  - `rich` (>=14.1.0) - Terminal formatting

## 🚀 Quick Start

### Installation

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

## 📖 Usage

1. **Start the App**: Run the application with your database path (CSV file)
   ```bash
   python main.py --db_path databases/babel_db.csv
   ```

2. **Main Interface**:
   - View all books in your library
   - Use the search bar to find books by specific fields
   - Choose from actions in the sidebar: Add, Edit, or Delete entries
   - Save changes with the "Save library" button
   - Reload the library or clear old backups as needed

## 💾 Database Format

The library database must be a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| `autor/a` | Author of the book |
| `título` | Title of the book |
| `título original` | Original title (if translated) |
| `traductor/a` | Translator of the book |
| `editorial` | Publisher |
| `año publicacion` | Year of publication |
| `año edicion` | Year of edition |
| `idioma` | Language of the book |
| `etiquetas` | Tags/categories (separated by semicolons) |

### Example CSV Row:
```
autor/a,título,título original,traductor/a,editorial,año publicacion,año edicion,idioma,etiquetas
Gabriel García Márquez,Cien años de soledad,One Hundred Years of Solitude,Gregory Rabassa,Sudamericana,1967,1997,Español,Realismo mágico;Ficción;Colombia
```

## 🔄 Backup Management

The application automatically creates timestamped backups of your database in the `databases/backups/` directory. This ensures you never lose your library data.

**Features**:
- Backups are created automatically with timestamps
- Use the "Clear backups" button to remove old backups
- Only the most recent backup is preserved when clearing

## 📁 Project Structure

```
babel/
├── main.py                 # Application entry point
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
├── src/
│   ├── library.py          # Core library management logic
│   └── __pycache__/
└── databases/
    ├── babel_db.csv        # Main database file
    └── backups/            # Automatic backup directory
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Submit issues for bugs or feature requests
- Create pull requests with improvements
- Suggest enhancements to the interface or functionality

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 💡 Tips & Tricks

- **Keyboard Shortcuts**: Use Streamlit's keyboard shortcuts to refresh the app (Ctrl+R or Cmd+R)
- **Search Tips**: Leave the search field empty to see all entries; type to filter results
- **Regular Backups**: The app automatically creates backups, but consider periodic manual exports for extra safety
- **Data Organization**: Use consistent formatting for author names and tags for better search results

## 📧 About

Babel is a personal project designed to help organize and maintain a personal book collection. Named after Borges' "The Library of Babel," this tool brings order to infinite possibilities of literature.

---

**Last Updated**: December 6, 2025
