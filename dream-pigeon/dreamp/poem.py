from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from dreamp.db import get_db
import random
import sys

bp = Blueprint('poem', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            new_poem = ""
            with current_app.open_resource('source.txt') as f:
                source = f.readlines()
            #     lines_seen = set()
            #     total_lines = 0
                # for n in range(5):
                while len(source) > 0:
                    # Randomly select a line and remove it from source.
                    line = random.choice(source)
                    source.remove(line)
                    # If --random_skip is passed, randomly skip the line
                    # and continue the next iteration of the loop.
                    # To increase the chance of skips, add 1s to the list.
                    # if args.random_skip and random.choice([0, 1]) == 1:
                    #     print("Skip line")
                    #     continue
                    # If --unique_lines is passed, check if the line was
                    # seen in a previous iteration. If not, write the line
                    # to new_file and add it to lines_seen.
                    # if args.unique_lines:
                    #     if line in lines_seen:
                    #         continue
                    #     lines_seen.add(line)
                    new_poem += str(line)
                    # total_lines += 1
                    # Radomly write 0, 1, 2, 3, or 4 empty lines
                    # to new_file, with 0 weighted heavier.
                    new_poem += random.choice([
                        "", "", "", "", "\n", "\n\n", "\n\n\n", "\n\n\n\n"])
            print(new_poem, file=sys.stderr)
            db.execute(
                'INSERT INTO poems (body)'
                ' VALUES (?)',
                (new_poem,)
            )
            db.commit()
            return redirect(url_for('poem.read'))

    return render_template('poem/index.html')


@bp.route('/read', methods=('GET', 'POST'))
def read():

    return render_template('poem/read.html')
