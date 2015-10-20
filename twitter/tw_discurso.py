CUENTAS = [
    "mauriciomacri",
    "danielscioli",
    "Stolbizer",
    "NicolasdelCano",
    "SergioMassa",
]

from dbmodels import *

if __name__ == '__main__':
    initialize_db()
    
    users = []

    TW = API_HANDLER.get_fresh_connection()
    for username in CUENTAS:
        try:
            u = TW.get_user(username)
            users.append(User(id=u.id, username=u.name))
        except TweepError:
            continue

    session = open_session()
    session.add_all(users)
    session.close()

    for user in users:
        user.fetch_timeline(session)
        user.fetch_favorites(session)
