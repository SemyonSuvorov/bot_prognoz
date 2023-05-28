import sqlite3 as sq



def sql_start():
    global cur, base
    base = sq.connect('clothes.db')
    cur = base.cursor()
    
    if base:
        print('Data base connected!')

async def sql_add_command(state):
    async with state.proxy() as data:
        values = tuple(data.values())
        cur.execute('SELECT MAX(id) FROM shoes')
        id = cur.fetchall()[0][0] + 1
        values = id, *values
        cur.execute('INSERT INTO shoes VALUES (?, ?, ?, ?, ?, ?)', values)
        base.commit()

async def sql_select(state):
    try:
        async with state.proxy() as data:    
            values = tuple(data.values())       
            cur.execute(f'SELECT photo FROM shoes WHERE ? >= min_temp AND ? <=max_temp AND color LIKE ? \
                        ORDER BY RANDOM() LIMIT 1', (values[1], values[1], values[3]))
            img = cur.fetchall()[0][0]
            return img
    except:
        pass