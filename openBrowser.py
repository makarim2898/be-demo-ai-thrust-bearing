import webbrowser
import os


def openBrowser():
    # Path relatif ke file HTML
    #/home/komputer/Desktop/thrust_bearing_app/frontend/html-old/Home-page/Homepage.html
    relative_path = '../frontend/html-old/Home-page/Homepage.html'

    # Mengubah path relatif menjadi path absolut
    file_path = os.path.abspath(relative_path)

    # Mengubah path file menjadi format URL
    file_url = 'file://' + file_path

    # Membuka file HTML di Google Chrome
    webbrowser.get('google-chrome').open(file_url)

openBrowser()