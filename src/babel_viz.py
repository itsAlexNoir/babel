import argparse
import streamlit as st
from library import Library, console


def get_flags():
    parser = argparse.ArgumentParser(description='Babel UI.')
    parser.add_argument('--db_path', type=str, help='Path to the database')
    return parser.parse_args()


def main(args):
    console.log('Starting app')
    if args.db_path is None:
        raise FileNotFoundError('Please provide a valid database path.')

    st.title('Babel!')
    st.header('Consultar la libreria')
    st.text('Puedes explorar el dataframe de la biblioteca')

    babel = Library(args.db_path)
    babel.show_db()

    if st.sidebar.button('Clear backups'):
        babel.clear_backups()
    if st.sidebar.button('Save library'):
        babel.save_db()
    if st.sidebar.button('Reload library'):
        babel.read_database()

    st.header('Buscar una entrada en la biblioteca')
    
    search_key = st.selectbox('Campo', babel.get_db.columns.tolist())
    str_search = st.text_input('Búsqueda', '')
    partial_db = babel.search_by(search_key, str_search)
    
    if str_search != '':
        table_on = st.checkbox('See as a table')
        if table_on:
            st.table(partial_db)
        else:
            st.dataframe(partial_db)
    
    acciones = ['Añadir entrada', 'Editar entrada', 'Borrar entrada']
    accion = st.sidebar.selectbox('Selecciona una acción', acciones)
    if accion=='Añadir entrada':
        babel.add_entry()
    elif accion=='Editar entrada':
        selected = st.selectbox('Seleccionar la entrada a editar', partial_db.index.tolist())
        babel.edit_entries(partial_db.loc[selected])
    elif accion=='Borrar entrada':
        selected = st.multiselect('Seleccionar las entradas a borrar', partial_db.index.tolist())
        if st.button('¿Borrar la(s) entradas seleccionada(s)?'):
            babel.remove_entries(partial_db.loc[selected])
        
 
if __name__ == '__main__':
    args = get_flags()
    main(args)