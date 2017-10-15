# nba scraper v.0.9
# scrape teams statistic and save them
import bs4 as bs
from selenium import webdriver
from sys import platform
import networkx as nx
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # start (class = columns / small-12 / section-view-overlay)
    player_url = 'https://stats.nba.com/players/list/'
    class_to_scrape = 'columns / small-12 / section-view-overlay'

    # bind the phantomjs
    if platform == 'darwin':
        driver = webdriver.PhantomJS(executable_path=r'/usr/local/bin/phantomjs/')
    elif platform == 'win32' or 'win64':
        driver = webdriver.PhantomJS(executable_path=r'C:\\Users\\Yanu\\Anaconda3\\selenium\\webdriver\\phantomjs\\bin\\phantomjs.exe')

    # get
    driver.get(player_url)

    # soup html
    html_soup = bs.BeautifulSoup(driver.page_source, 'lxml')

    # start search for the class
    div = html_soup.find('div', class_=class_to_scrape)

    # create a graph
    G = nx.Graph()
    G.add_node('All Players')

    # start searching
    count = 0
    for by_alphabet in div.find_all('section', class_='row collapse players-list__section'):
        # group by alphabet starts
        alp = by_alphabet.find('h1', class_='players-list__initial')
        G.add_node(alp.string)
        G.add_edge('All Players', alp.string)

        # print all players based on each group
        for player in by_alphabet.find_all('li', class_='players-list__name'):
            print(' '.join(list(reversed(player.text.split(', ')))))
            G.add_node(count)
            G.add_edge(alp.string, count)
            count += 1

    # plot
    plt.subplot(111)
    nx.draw(G, with_labels=True)
    plt.show()

    # save the html
    html_file = open("outfile.html", "w")
    html_file.write(str(div))
    html_file.close()

    # quit the driver
    driver.quit()
