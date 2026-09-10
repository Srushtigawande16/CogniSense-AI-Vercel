from flask import Blueprint, request, jsonify
from database import get_db

auth_bp = Blueprint('auth', __name__)

# ── LOGIN ─────────────────────────────────────────────────
@auth_bp.route('/login', methods=['POST'])
def login():
    data     = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'success': False,
                        'message': 'Username and password required'}), 400

    conn = get_db()
    user = conn.execute(
        'SELECT id, username FROM users WHERE username=? AND password=?',
        (username, password)
    ).fetchone()
    conn.close()

    if user:
        return jsonify({
            'success':  True,
            'user_id':  user['id'],
            'username': user['username'],
            'message':  'Login successful'
        })
    return jsonify({'success': False,
                    'message': 'Invalid username or password'}), 401


# ── REGISTER ──────────────────────────────────────────────
@auth_bp.route('/register', methods=['POST'])
def register():
    data     = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'success': False,
                        'message': 'Username and password required'}), 400

    if len(username) < 3:
        return jsonify({'success': False,
                        'message': 'Username must be at least 3 characters'}), 400

    if len(password) < 4:
        return jsonify({'success': False,
                        'message': 'Password must be at least 4 characters'}), 400

    conn = get_db()

    # Check if username already exists
    existing = conn.execute(
        'SELECT id FROM users WHERE username=?', (username,)
    ).fetchone()

    if existing:
        conn.close()
        return jsonify({'success': False,
                        'message': 'Username already taken. Try another.'}), 409

    # Insert new user
    cur = conn.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (username, password)
    )
    user_id = cur.lastrowid
    conn.commit()
    conn.close()

    print(f"[AUTH] New user registered: {username} (id={user_id})")

    return jsonify({
        'success':  True,
        'user_id':  user_id,
        'username': username,
        'message':  'Account created successfully!'
    })
ENDOFFILE
echo "Done auth.py"