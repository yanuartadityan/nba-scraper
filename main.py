# nba scraper v.0.9
# scrape teams statistic and save them
import bs4 as bs
from selenium import webdriver


# start (class = columns / small-12 / section-view-overlay)
url_to_scrape = 'https://stats.nba.com/players/list/'
class_to_scrape = 'columns / small-12 / section-view-overlay'

# bind the phantomjs
driver = webdriver.PhantomJS(executable_path=r'/usr/local/bin/phantomjs/')

# get
driver.get(url_to_scrape)

# soup html
html_soup = bs.BeautifulSoup(driver.page_source, 'lxml')

# start search for the class
div = html_soup.find('div', class_=class_to_scrape)

for by_alphabet in div.find_all('section', class_='row collapse players-list__section'):
    # group by alphabet starts
    for alp in by_alphabet.find('h1', class_='players-list__initial'):
        print('------{}------'.format(alp.string))

    # print all players based on each group
    for player in by_alphabet.find_all('li', class_='players-list__name'):
        print(' '.join(list(reversed(player.text.split(', ')))))

    # new line
    print()

# save the html
html_file = open("outfile.html", "w")
html_file.write(str(div))
html_file.close()

# quit the driver
driver.quit()
