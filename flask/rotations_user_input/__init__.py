from flask import (
    current_app, Flask, flash, redirect, render_template, request, url_for
)
import os
import psycopg2
import random
import sys
from werkzeug.exceptions import abort

def create_app():
    # Create and configure the app.
    app = Flask(__name__, instance_relative_config=True)

    conn = psycopg2.connect(
        database='several_rotations',
        user='app',
        sslmode='require',
        sslrootcert='certs/ca.crt',
        sslkey='certs/client.app.key',
        sslcert='certs/client.app.crt',
        port='26257',
        host='localhost',
        application_name='rotations'
)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

   # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=('GET', 'POST'))
    def index():
        if request.method == 'POST':
            # max_lines = request.form.get('max_lines')
            # if max_lines == "":
            #     max_lines = None
            max_sections = request.form.get('max_sections')
            if max_sections == "":
                max_sections = None
            lines_per_section = request.form.get('lines_per_section')
            if lines_per_section == "":
                lines_per_section = None
            repeat = request.form.get('repeat')
            error = None

            if error is not None:
                flash(error)
            else:
                # Create row for the new poem in the poems table.
                cur.execute(
                    'INSERT INTO poems (body)'
                    ' VALUES (%s)'
                    ' RETURNING id',
                    ('',)
                )
                row = cur.fetchone()
                id = row[0]
                # Store the user's generation options for the poem in the state table.
                cur.execute(
                    'INSERT INTO state (poem_id, max_sections, lines_per_section, repeat)'
                    ' VALUES (%s, %s, %s, %s)'
                    ' RETURNING id',
                    (id, max_sections, lines_per_section, repeat)
                )
                row = cur.fetchone()
                state_id = row[0]
                # print(id, file=sys.stderr)
                # print(state_id, file=sys.stderr)

                return redirect(url_for('create', id=id))

        return render_template('poem/index.html')

    @app.route('/create/<id>', methods=('GET', 'POST'))
    def create(id):
        new_poem = ''
        lines_seen = set()
        total_lines = 0
        lines_in_section = 0
        section = 1
        error = None

        if error is not None:
            flash(error)
        else:
            # Read the source text into memory and retrieve the user's generation
            # options for the new poem.
            with current_app.open_resource('source.txt') as f:
                source = f.readlines()
                cur.execute(
                    'SELECT max_sections, lines_per_section, repeat from state'
                    ' WHERE poem_id = %s',
                    (id,)
                )
                row = cur.fetchone()
                max_sections = row[0]
                lines_per_section = row[1]
                repeat = row[2]
                # remove_words_gradual = row[3]
                new_poem += str(section) + "\n\n\n"
                while len(source) > 0:
                    # Break out of the loop once the max lines have been generated.
                    # if max_lines != None:
                    #     if total_lines == max_lines:
                    #         break
                    # Create new section after specified number of lines.
                    if lines_in_section == lines_per_section:
                        if section == max_sections:
                            break
                        section += 1
                        new_poem += "\n\n" + str(section) + "\n\n\n"
                        lines_in_section = 0
                    # Randomly select a line and remove it from source.
                    line = random.choice(source)
                    source.remove(line)
                    if not line.isspace():
                        if len(line) > 70:
                            continue
                        # Randomly skip the line and continue the next iteration.
                        # To increase the chance of skips, add 1s to the list.
                        if random.choice([0, 1]) == 1:
                            # print("Skip line", file=sys.stderr)
                            continue
                        line = line.decode('utf-8')
                        # Unless user wants repeat lines, check if the line was seen
                        # in a previous iteration. If so, continue the next iteration.
                        if repeat == False:
                            if line in lines_seen:
                                continue
                            lines_seen.add(line)
                        new_poem += line
                        total_lines += 1
                        # Radomly add 0, 1, 2, 3, or 4 empty lines to new_poem.
                        # 0 is weighted heavier.
                        new_poem += random.choice([
                            "", "", "", "", "\n", "\n\n", "\n\n\n", "\n\n\n\n"])
                        lines_in_section += 1

                cur.execute(
                    'UPDATE poems SET body = %s'
                    'WHERE id = %s',
                    (new_poem, id)
                )

            return redirect(url_for('read', id=id))

    @app.route('/read/<id>', methods=('GET',))
    def read(id):
        cur.execute(
            'SELECT body, created FROM poems WHERE id = %s',
            (id,)
        )
        poem = cur.fetchone()
        # print(poem, file=sys.stderr)

        if poem is None:
            abort(404, "Poem id {0} doesn't exist.".format(id))

        return render_template('poem/read.html', poem=poem[0], created=poem[1])

    return app

# if __name__ == '__main__':
#     app.run()
