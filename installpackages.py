import os

packages = ['bs4', 'googlemaps', 'haversine', 'requests', 'wxPython==4.0.3']

if __name__ == '__main__':
    for package in packages:
        os.system(f'pip install {package}')
    input('\nInstalled the required site-packages to global python. \n'
          'If you are using a virtual environment, make sure it inherits the global site-packages!\n'
          'Press any key to leave...')
