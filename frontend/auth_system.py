import hashlib
from database import cursor, conn

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

def register_user(username, password, question, answer):
    try:
        cursor.execute(
            "INSERT INTO users (username,password,question,answer) VALUES (?,?,?,?)",
            (username, hash_pass(password), question, answer)
        )
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    data = cursor.fetchone()
    if not data:
        return False
    return data[0] == hash_pass(password)

def get_security_question(username):
    cursor.execute("SELECT question FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    return row[0] if row else None

def reset_password(username, answer, new_pass):
    cursor.execute("SELECT answer FROM users WHERE username=?", (username,))
    row = cursor.fetchone()

    if row and row[0].lower() == answer.lower():
        cursor.execute(
            "UPDATE users SET password=? WHERE username=?",
            (hash_pass(new_pass), username)
        )
        conn.commit()
        return True
    return False