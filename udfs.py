
# to-do: move the function:read_cred_from_file to a new .py(creds.py)file

# UDFs imported by other files:
# json_to_mysql.ipynb -> get_mysql_connection

from sqlalchemy import create_engine


from typing import Tuple



def read_cred_from_file() -> Tuple[str, str]:
    """
    Description:
        Reads the MySQL credentials from a secrets file.
    Usage Example:
        username, password = read_cred_from_file()
    Returns:
        A tuple containing the MySQL username and password.
    """
    try:
        with open('secrets.txt', 'r') as f:
            lines = f.readlines()

        secrets = {}
        for line in lines:
            key, value = line.strip().split('=')
            secrets[key] = value

        db_username = secrets.get('DB_USERNAME')
        db_password = secrets.get('DB_PASSWORD')

        if db_username is None or db_password is None:
            raise ValueError("Missing credentials in secrets file.")

        return db_username, db_password

    except FileNotFoundError:
        raise FileNotFoundError("Secrets file not found.")

    except Exception as e:
        raise Exception("Error occurred while reading credentials: " + str(e))
    

    


SERVER_IP = '127.0.0.1'
DB_CONNECT_PORT = 3306
DB_USERNAME, DB_PASSWORD = read_cred_from_file()


from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

def get_mysql_connection(username: str = DB_USERNAME, password: str = DB_PASSWORD,
                         server_ip: str = SERVER_IP, server_connect_port: int = DB_CONNECT_PORT,
                         connect_to_database = False, db_name = '') -> Engine:
    """
    Create a MySQL database connection using the provided credentials.

    Args:
        username (str, optional): The username for the MySQL database. Defaults to 'root'.
        password (str, optional): The password for the MySQL database. Defaults to 'password'.
        server_ip (str, optional): The IP address of the MySQL server. Defaults to '127.0.0.1'.
        server_connect_port (int, optional): The connection port for the MySQL server. Defaults to 3306.

    Returns:
        sqlalchemy.engine.Engine: A MySQL database connection engine.
    """
    connection_string = f'mysql+pymysql://{username}:{password}@{server_ip}'
    if connect_to_database:
        connection_string = connection_string + '/{db_name}'
    try:
       
            
        sqlEngine = create_engine(connection_string, pool_recycle=server_connect_port)
        return sqlEngine.connect()

    except Exception as e:
        raise ConnectionError(f"Failed to connect to the MySQL database: {e}")




def flatten_dict(dictionary, parent_key='', sep='_'):
    """
    Flattens a nested dictionary into a single-level dictionary.

    Args:
        dictionary (dict): The dictionary to be flattened.
        parent_key (str): The key of the parent dictionary.
        sep (str): Separator used to concatenate keys.

    Returns:
        dict: The flattened dictionary.
    """
    flattened_dict = {}
    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            flattened_dict.update(flatten_dict(value, new_key, sep=sep)) # recursion
        else:
            flattened_dict[new_key] = value
    return flattened_dict