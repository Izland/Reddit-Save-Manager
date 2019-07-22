import configparser

def getParserObj():
    config = configparser.ConfigParser()
    config.read('credentials.ini')

    return config

def getConfigItems(config):
    values = []
    configObj = config['credentials'].items()
    for item in configObj:
        values.append(item[1])

    return values

def main():

    config = getParserObj()
    credentialItems = getConfigItems(config)

    global client_id 
    client_id = credentialItems[0]

    global client_secret 
    client_secret = credentialItems[1]

    global username
    username = credentialItems[2]

    global password 
    password = credentialItems[3]

# client_id = ''
# client_secret = ''
# username = ''
# password = ''

main()

