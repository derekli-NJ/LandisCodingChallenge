import sqlite3
import json

def format_data(filename):
    """
    Formats the data of a jsonl file containing account information
    Arguments: filename- name of the file in the same directory or the absolute path
    Return: List of tuples containing all account information
    """
    data = []
    with open(filename, 'r') as read_file:
        json_list = list(read_file)

    for json_str in json_list:
        json_object = json.loads(json_str)
        
        data.append((json_object['id'], json_object['balance'], int(json_object['credit']), json_object['picture'], json_object['name_first'], json_object['name_last'], json_object['employer'], json_object['email'], json_object['phone'], json_object['address'], json_object['comments'], json_object['created'], str(json_object['tags'])))

    return data 

def create_database(data, sql_create_accounts_table):
    """
    Creates database using account data
    Arguments: data - List of tuples containing all account information
    sql_create_accounts_table - String with SQL command and data fields of the table
    Side Effects: Creates a database called accounts.db that contains all account information 
    """
    connection = sqlite3.connect('accounts.db')
    cursor = connection.cursor()
    cursor.execute(sql_create_accounts_table)
    cursor.executemany('''INSERT INTO accounts (id, balance, credit, picture, name_first, name_last, employer, email, phone, address, comments, created, tags) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    connection.commit()
    connection.close()

data = format_data("accounts.jsonl")

#SQL command to make a table
sql_create_accounts_table= """ CREATE TABLE IF NOT EXISTS accounts(
                                        id text PRIMARY KEY,
                                        balance text,
                                        credit integer,
                                        picture text,
                                        name_first text,
                                        name_last text,
                                        employer text,
                                        email text,
                                        phone integer,
                                        address text,
                                        comments text,
                                        created text,
                                        tags text
                                    ); """

create_database(data, sql_create_accounts_table)
