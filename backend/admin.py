
from flask import Blueprint
from auth import login_required
from db import get_db
from blog import sqlquery_to_array_of_object, load_user
from auth import login_required
import json


bp = Blueprint('admin', __name__, url_prefix='/admin/')

@bp.route('/', methods=['GET'])
# load_user()
# @login_required
def index():

    """Liste tous les utilisateurs avec leurs rôles."""
    db = get_db()
    users = db.execute(
        'SELECT id, username, role FROM user'
    )
    data = sqlquery_to_array_of_object(users)
    return json.dumps(data, indent=4, sort_keys=True, default=str)

@bp.route('/makeadmin/<username>', methods=['POST', 'GET'])
# @login_required
# @admin_required  # Si vous avez déjà un admin
def makeadmin(username):
    db = get_db()
    db.execute('UPDATE user SET role = ? WHERE username = ?', ('admin', username))
    db.commit()
    return json.dumps({'success': True, 'message': f'User {username} is now admin'})
