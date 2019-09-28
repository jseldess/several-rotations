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


    # Retrieve the most recent poem and the IDs of the previous and next poems
    # and pass it all to the index template. This endpoint is called when a user
    # lands on the homepage or selects "Latest" from the topnav (all templates).
    @app.route('/', methods=('GET',))
    def index():
        error = None

        if error is not None:
            flash(error)
        else:
            cur.execute(
                'SELECT body, created, id FROM poems ORDER BY created DESC LIMIT 1'
            )
            poem = cur.fetchone()
            id = poem[2]
            # print(poem, file=sys.stderr)

            cur.execute(
                'SELECT previous FROM (SELECT lag(id, 1) OVER w AS previous, id AS current FROM poems WINDOW w AS (ORDER BY created ASC)) WHERE current = %s',
                (id,)
            )
            previous = cur.fetchone()
            previous = previous[0]

        return render_template('poem/index.html', poem=poem[0], created=poem[1], id=id, previous=previous)


    # Generate a new poem. This endpoint is called by a cronjob once a day.
    @app.route('/create', methods=('GET', 'POST'))
    def create():
        max_sections = 1
        lines_per_section = 10
        repeat = True
        new_poem = ''
        lines_seen = set()
        total_lines = 0
        lines_in_section = 0
        section = 1

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
                new_poem += "--" + "\n\n\n"
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
                        new_poem += "\n\n" + "--" + "\n\n\n"
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

        return ('', 204)


    # Retrieve the ID, creation timestamp, and first line of the 20 most recent
    # poems and pass it all to the select template. This endpoint is called
    # when a user selects "Recent" from the topnav (all templates).
    @app.route('/select', methods=('GET', 'POST'))
    def select():
        # Get the ID, creation date, and first line of the 10 most recent poems.
        cur.execute(
            "SELECT id, created, regexp_extract(body, '^([^\n]*\n){4}([^\n]*)\n.*') FROM poems ORDER BY created DESC LIMIT 10",
        )
        rows = cur.fetchall()
        r1, r2, r3, r4, r5, r6, r7, r8, r9, r10 = rows

        # Get the creation date of the oldest poem. This is used to make earlier
        # dates unselectable in the date selector on the select template.
        cur.execute(
            "SELECT created FROM poems ORDER BY created ASC LIMIT 1",
        )
        earliest = cur.fetchall()[0][0]
        # print(earliest, file=sys.stderr)

        # Get the creation date of the latest poem. This is used to make later
        # dates unselectable in the date selector on the select template.
        cur.execute(
            "SELECT created FROM poems ORDER BY created DESC LIMIT 1",
        )
        latest = cur.fetchall()[0][0]
        # print(latest, file=sys.stderr)

        # When the date selector on the select template is used, get the
        # corresponding poem.
        message = ''
        if request.method == 'POST':
            day_select = request.form.get('day')
            # print(day_select, file=sys.stderr)
            cur.execute(
                'SELECT id FROM poems WHERE created > %s ORDER BY created ASC LIMIT 1;',
                (day_select,)
            )
            row = cur.fetchone()
            # print(row, file=sys.stderr)
            if row is None:
                message = 'No poem generated on that date. Choose another.'
            else:
                return redirect(url_for('read', id=row[0]))

        return render_template('poem/select.html', r1=r1, r2=r2, r3=r3, r4=r4, r5=r5, r6=r6, r7=r7, r8=r8, r9=r9, r10=r10, earliest=earliest, latest=latest, message=message)


    # Retrieve a specific poem and the IDs of the previous and next poems and
    # pass it all to the read template. This endpoint is called when a user
    # selects a poem on the "Recent" page (select template).
    @app.route('/read/<id>', methods=('GET',))
    def read(id):
        cur.execute(
            'SELECT body, created FROM poems WHERE id = %s',
            (id,)
        )
        poem = cur.fetchone()
        # print(poem, file=sys.stderr)

        cur.execute(
            'SELECT previous,next FROM (SELECT lag(id, 1) OVER w AS previous, id AS current, lead(id, 1) OVER w AS next FROM poems WINDOW w AS (ORDER BY created ASC)) WHERE current = %s',
            (id,)
        )
        previous_next = cur.fetchone()
        previous = previous_next[0]
        next = previous_next[1]

        return render_template('poem/read.html', poem=poem[0], created=poem[1], id=id, previous=previous, next=next)


    # Show information about the site. This endpoint is called when a user
    # selects "About" from the topnav (all templates).
    @app.route('/about', methods=('GET',))
    def about():
        return render_template('poem/about.html')

    return app
