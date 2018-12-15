from dreamp.db import get_db
from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, url_for
)
import random
import sys
from werkzeug.exceptions import abort

bp = Blueprint('poem', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        new_poem = ''
        skip = request.form.get('skip')
        repeat = request.form.get('repeat')
        maxlines = request.form.get('maxlines')
        lines_seen = set()
        total_lines = 0
        db = get_db()
        error = None

        if error is not None:
            flash(error)
        else:
            cur = db.cursor()
            with current_app.open_resource('source.txt') as f:
                source = f.readlines()
                while len(source) > 0:
                    # If 'Max number of lines' is specified, break out of the
                    # loop as soon as the max lines have been generated.
                    if maxlines:
                        if total_lines == int(maxlines):
                            break
                    # Randomly select a line and remove it from source.
                    line = random.choice(source)
                    source.remove(line)
                    # If 'Randomly skip lines' is checked, randomly skip the line
                    # and continue the next iteration of the loop.
                    # To increase the chance of skips, add 1s to the list.
                    if skip and random.choice([0, 1]) == 1:
                        print("Skip line", file=sys.stderr)
                        continue
                    # If 'Repeat unique lines' is not checked, check if the line
                    # was seen in a previous iteration. If not, add the line
                    # to new_poem and lines_seen.
                    if not repeat:
                        if line in lines_seen:
                            continue
                        lines_seen.add(line)
                    new_poem += line.decode("utf-8")
                    total_lines += 1
                    # Radomly add 0, 1, 2, 3, or 4 empty lines
                    # to new_poem, with 0 weighted heavier.
                    new_poem += random.choice([
                        "", "", "", "", "\n", "\n\n", "\n\n\n", "\n\n\n\n"])
            print(new_poem, file=sys.stderr)
            cur.execute(
                'INSERT INTO poems (body)'
                ' VALUES (?)',
                (new_poem,)
            )
            db.commit()
            id = cur.lastrowid
            print(id, file=sys.stderr)
            return redirect(url_for('poem.read', id=id))

    return render_template('poem/index.html')


@bp.route('/read', methods=('GET',))
def read():
    db = get_db()
    id = request.args['id']
    poem = db.execute(
        'SELECT body FROM poems WHERE id = ?',
        [id]
    ).fetchone()

    if poem is None:
        abort(404, "Poem id {0} doesn't exist.".format(id))

    return render_template('poem/read.html', poem=poem)
