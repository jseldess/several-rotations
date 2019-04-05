from flask import (
    current_app, Flask, flash, redirect, render_template, request, url_for
)
import jinja2
import psycopg2
import random
import re
import sys
from werkzeug.exceptions import abort


db = "postgres://root@localhost:26257/several_rotations?sslmode=disable"
conn = psycopg2.connect(db)
conn.set_session(autocommit=True)
cur = conn.cursor()
app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        max_lines = request.form.get('max_lines')
        if max_lines == "":
            max_lines = None
        repeat = request.form.get('repeat')
        # remove_words_gradual = request.form.get('remove_words_gradual')
        remove_words = request.form.get('remove_words')
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
                'INSERT INTO state (poem_id, repeat, max_lines, remove_words)'
                ' VALUES (%s, %s, %s, %s)'
                ' RETURNING id',
                (id, repeat, max_lines, remove_words)
            )
            row = cur.fetchone()
            state_id = row[0]
            print(id, file=sys.stderr)
            print(state_id, file=sys.stderr)

            return redirect(url_for('create', id=id))

    return render_template('poem/index.html')

@app.route('/create/<id>', methods=('GET', 'POST'))
def create(id):
    new_poem = ''
    lines_seen = set()
    total_lines = 0
    # remove_words_index = 0
    error = None

    if error is not None:
        flash(error)
    else:
        # Read the source text into memory and retrieve the user's generation
        # options for the new poem.
        with current_app.open_resource('source.txt') as f:
            source = f.readlines()
            cur.execute(
                'SELECT repeat, max_lines, remove_words from state'
                ' WHERE poem_id = %s',
                (id,)
            )
            row = cur.fetchone()
            repeat = row[0]
            max_lines = row[1]
            remove_words = row[2]
            # remove_words_gradual = row[3]
            while len(source) > 0:
                # Break out of the loop once the max lines have been generated.
                if max_lines != None:
                    if total_lines == max_lines:
                        break
                # Randomly select a line and remove it from source.
                line = random.choice(source)
                source.remove(line)
                # Randomly skip the line and continue the next iteration.
                # To increase the chance of skips, add 1s to the list.
                if random.choice([0, 1]) == 1:
                    print("Skip line", file=sys.stderr)
                    continue
                line = line.decode('utf-8')
                # if remove_words_gradual == True:
                #     seq = [i for i in range(1,max_lines + 1)]
                #     remove_pacing = [seq[i:i + 7] for i in range(0, len(seq), 7)]
                #     for i in remove_pacing:
                #         if total_lines in i:
                #             if remove_pacing.index(i) > remove_words_index:
                #                 remove_words_index += 1
                #                 remove_words += 1
                #     remove_expr = '^' + ('\W*\w+' * remove_words) + '\W*'
                #     line = re.sub(remove_expr, '', line)
                # Remove the specified number of words from the start of the line.
                if remove_words != 0:
                    remove_expr = '^' + ('\W*\w+' * remove_words) + '\W*'
                    line = re.sub(remove_expr, '\n', line)
                # Unless user wants repeat lines, check if the line was seen
                # in a previous iteration. If so, continue the next iteration.
                if repeat == False:
                    if line in lines_seen:
                        continue
                    lines_seen.add(line)
                new_poem += line
                # Radomly add 0, 1, 2, 3, or 4 empty lines to new_poem.
                # 0 is weighted heavier.
                new_poem += random.choice([
                    "", "", "", "", "\n", "\n\n", "\n\n\n", "\n\n\n\n"])
                if not line.isspace():
                    total_lines += 1

            cur.execute(
                'UPDATE poems SET body = %s'
                'WHERE id = %s',
                (new_poem, id)
            )

        return redirect(url_for('read', id=id))

@app.route('/read/<id>', methods=('GET',))
def read(id):
    cur.execute(
        'SELECT body FROM poems WHERE id = %s',
        (id,)
    )
    poem = cur.fetchone()
    # poem = poem[0].split('\n')
    print(poem, file=sys.stderr)

    if poem is None:
        abort(404, "Poem id {0} doesn't exist.".format(id))

    return render_template('poem/read.html', poem=poem[0])

if __name__ == '__main__':
    app.run()
