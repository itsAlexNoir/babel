import os
from glob import glob
import pandas as pd
import streamlit as st
from datetime import datetime
from rich.console import Console

console = Console()


class Library(object):
    def __init__(self, db_path):
        if not os.path.isfile(db_path):
            raise FileNotFoundError("File does not exists")
        self.db_folder = "databases"
        self.db_filepath = db_path
        self.filename = os.path.basename(db_path).split(".")[0]

        self.backup_folder = os.path.join(self.db_folder, "backups")
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)

        self.db = self.read_database()
        self.create_backup()
        self.db_slot = st.empty()

    @property
    def get_db(self):
        return self.db

    def read_database(self):
        db = pd.read_csv(self.db_filepath)
        db = db.fillna("")
        db["año publicacion"] = db["año publicacion"].apply(
            lambda x: str(x).split(".")[0]
        )
        db["año edicion"] = db["año edicion"].apply(lambda x: str(x).split(".")[0])
        return db

    def create_backup(self):
        current_date = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
        console.log("Saving backup at " + datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        self.db.to_csv(
            os.path.join(
                self.backup_folder, self.filename + "__" + current_date + ".csv"
            ),
            index=False,
        )

    def clear_backups(self):
        backs = glob(os.path.join(self.backup_folder, self.filename + "_*"))
        dates = {
            datetime.strptime(x.split("__")[1].split(".csv")[0], "%d.%m.%Y_%H.%M.%S"): x
            for x in backs
        }
        last_date = sorted(list(dates.keys()))[-1]
        for date in dates.keys():
            if date != last_date:
                os.remove(dates[date])

    def add_item_to_library(self, new_entry):
        self.db = pd.concat([self.db, new_entry], ignore_index=True)

    def search_by(self, key, str_search):
        return self.db[self.db[key].str.lower().str.contains(str_search.lower())]

    def add_entry(self):
        st.header("Añadir una entrada en la biblioteca")
        new_title = st.text_input("Título", "")
        new_original_title = st.text_input("Título original", "")
        new_author = st.text_input("Autor/a", "")
        new_editorial = st.text_input("Editorial", "")
        new_traductor = st.text_input("Traductor/a", "")
        new_publication_year = st.text_input("Año de publicación", "")
        new_edition_year = st.text_input("Año de edición", "")
        new_language = st.text_input("Idioma", "")
        new_tags = st.text_input("Etiquetas (separadas por punto y coma)", "")

        new_entry_str = (
            f"### Nueva entrada:  \n"
            + f"- **Título**: {new_title} \n"
            + f"- **Autor/a**: {new_author} \n"
            + f"- **Título original**: {new_original_title} \n"
            + f"- **Traductor/a**: {new_traductor} \n"
            + f"- **Editorial**: {new_editorial} \n"
            + f"- **Año de publicación**: {new_publication_year} \n"
            + f"- **Año de edición**: {new_edition_year} \n"
            + f"- **Idioma**: {new_language} \n"
            + f"- **Etiquetas**: {new_tags}"
        )

        st.markdown(new_entry_str)
        new_entry_dict = [
            {
                "autor/a": new_author,
                "título": new_title,
                "título original": new_original_title,
                "traductor/a": new_traductor,
                "editorial": new_editorial,
                "año publicacion": new_publication_year,
                "año edicion": new_edition_year,
                "idioma": new_language,
                "etiquetas": new_tags,
            }
        ]
        new_entry = pd.DataFrame.from_dict(new_entry_dict)
        # Press to add a new entry
        if st.button("Añadir entrada"):
            self.add_item_to_library(new_entry)
            self.save_db()
            self.create_backup()
            self.show_db()
            st.write("Entrada añadida")

    def edit_entries(self, db_to_edit):
        st.header("Editar una entrada en la biblioteca")
        edit_title = st.text_input("Título (edit)", db_to_edit["título"])
        edit_original_title = st.text_input(
            "Título original (edit)", db_to_edit["título original"]
        )
        edit_author = st.text_input("Autor/a (edit)", db_to_edit["autor/a"])
        edit_editorial = st.text_input("Editorial (edit)", db_to_edit["editorial"])
        edit_traductor = st.text_input("Traductor/a (edit)", db_to_edit["traductor/a"])
        edit_publication_year = st.text_input(
            "Año de publicación (edit)", db_to_edit["año publicacion"]
        )
        edit_edition_year = st.text_input(
            "Año de edición (edit)", db_to_edit["año edicion"]
        )
        edit_language = st.text_input("Idioma (edit)", db_to_edit["idioma"])
        edit_tags = st.text_input(
            "Etiquetas (separadas por punto y coma) (edit)", db_to_edit["etiquetas"]
        )

        edit_entry_str = (
            f"### Editar entrada:  \n"
            + f"- **Título**: {edit_title} \n"
            + f"- **Autor/a**: {edit_author} \n"
            + f"- **Título original**: {edit_original_title} \n"
            + f"- **Traductor/a**: {edit_traductor} \n"
            + f"- **Editorial**: {edit_editorial} \n"
            + f"- **Año de publicación**: {edit_publication_year} \n"
            + f"- **Año de edición**: {edit_edition_year} \n"
            + f"- **Idioma**: {edit_language} \n"
            + f"- **Etiquetas**: {edit_tags}"
        )
        st.markdown(edit_entry_str)
        edit_entry_dict = [
            {
                "autor/a": edit_author,
                "título": edit_title,
                "título original": edit_original_title,
                "traductor/a": edit_traductor,
                "editorial": edit_editorial,
                "año publicacion": edit_publication_year,
                "año edicion": edit_edition_year,
                "idioma": edit_language,
                "etiquetas": edit_tags,
            }
        ]
        edit_entry = pd.DataFrame.from_dict(edit_entry_dict)
        if st.button("¿Editar la entrada?"):
            for col in self.db.columns:
                self.db.loc[db_to_edit.name][col] = edit_entry[col].iloc[0]
            self.save_db()
            self.create_backup()
            self.show_db()
            st.write("Entrada editada")

    def remove_entries(self, db_to_drop):
        self.db.drop(db_to_drop.index, inplace=True)
        self.save_db()
        st.write("Entrada borrada")

    def save_db(self):
        self.db.to_csv(self.db_filepath, index=False)

    def show_db(self):
        self.db_slot.write(self.db)
