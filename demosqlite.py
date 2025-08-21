# Importamos las librerías necesarias:
# - streamlit: para construir la interfaz web
# - sqlite3: para manejar la base de datos SQLite
# - ast: para convertir cadenas en estructuras de Python (ej. listas)
import streamlit as st, sqlite3, ast

# Creamos o abrimos la base de datos 'db.db'
# y obtenemos un cursor para ejecutar comandos SQL
con = sqlite3.connect('db.db'); cur = con.cursor()

# Creamos una tabla llamada 'db' si no existe, con 3 columnas de texto
cur.execute('CREATE TABLE IF NOT EXISTS db(name TEXT, letters TEXT, note TEXT)')

# Si el usuario hace clic en el botón "Add New Row"
if st.button('Add New Row'):
    # Insertamos una nueva fila vacía en la tabla (name vacío, lista vacía, nota vacía)
    cur.execute('INSERT INTO db(name, letters, note) VALUES(?,?,?)', ('', '[]', ''))
    con.commit()  # Guardamos los cambios en la base de datos

# Recorremos cada fila de la tabla, obteniendo también el rowid (identificador interno de SQLite)
for row in cur.execute('SELECT rowid, name, letters, note FROM db ORDER BY name'):
    # Creamos un "expander" en la interfaz con el nombre de la fila (columna name)
    with st.expander(row[1]):
        # Creamos un formulario único para cada fila, usando el rowid en el ID
        with st.form(f'ID-{row[0]}'):
            # Campo de texto para el nombre, precargado con el valor actual
            name = st.text_input('Name', row[1])
            
            # Campo multiselección con opciones 'A', 'B', 'C'
            # Los valores se cargan convirtiendo el string almacenado (ej. "['A']") a lista real con ast.literal_eval
            letters = st.multiselect('Letters', ['A', 'B', 'C'], ast.literal_eval(row[2]))
            
            # Campo de texto largo para notas, precargado con el valor actual
            note = st.text_area('Note', row[3])

            # Si el usuario presiona "Save"
            if st.form_submit_button('Save'):
                # Actualizamos la fila con los nuevos valores
                # (OJO: aquí usas 'WHERE name=?' lo cual puede fallar si hay nombres repetidos;
                # lo recomendable es usar rowid como referencia única)
                cur.execute(
                    'UPDATE db SET name=?, letters=?, note=? WHERE name=?;',
                    (name, str(letters), note, str(row[1]))
                )
                con.commit()   # Guardamos los cambios
                st.rerun()     # Recargamos la app para reflejar los cambios

            # Si el usuario presiona "Delete"
            if st.form_submit_button('Delete'):
                # Eliminamos la fila usando su rowid (identificador único en SQLite)
                cur.execute(f'DELETE FROM db WHERE rowid="{row[0]}";')
                con.commit()              # Guardamos cambios
                st.rerun()   # Recargamos la app (en versiones nuevas usar st.rerun())

