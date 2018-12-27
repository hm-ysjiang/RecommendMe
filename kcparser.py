import configparser


def parse_config():
    config = configparser.ConfigParser()
    config.read('akc.ini')
    if not config:
        return None
    return config


def get_google_api_key():
    return parse_config()['ak']['v']


def gen_config():
    config = parse_config()
    config['ak'] = {}
    config['ak']['v'] = ''
    with open('akc.ini', 'w') as cfg:
        config.write(cfg)


if __name__ == '__main__':
    # gen_config()
    pass