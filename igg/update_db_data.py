#!/usr/bin/python3
from igg.db import conn, cur

""" Updates the email and contribution id to the database """

def update_db(email, contribution_id):
    # add a field to the db with email and contribution_id

    email = email
    contribution_id = contribution_id

    try:
        with conn:
            cur.execute('INSERT INTO voltaGo(email, contribution) VALUES (?, ?)', (email, contribution_id))
            print('successful')
    except Exception as e:
        print(e)
        conn.rollback()
        raise
