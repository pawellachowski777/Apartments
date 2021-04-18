#!/usr/bin/env python


def adverts(pages=1):
    """
    This function downloads tabular data about flats for rent in Warsaw from oxl.pl web side.
    """

    from urllib.request import urlopen 
    from bs4 import BeautifulSoup
    
    my_url = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/'
    links = []

    for i in range(pages+1):
        
        if pages == 0:
            break
            
        elif i >= 1:
            url = my_url + '?page=' + str(i)
            client = urlopen(url)
            page_html = client.read()
            page_soup = BeautifulSoup(page_html, 'html.parser')
            containers = page_soup.find_all('tr', {'class': 'wrap'})
            for cont in containers:
                link = cont.tr.td.a['href']
                if 'olx' in link:
                    links.append(link)
                    
    rows = []
    for link in list(set(links)):
        try:
            ad = urlopen(link).read()
            ad_soup = BeautifulSoup(ad, features="html.parser")
            
            added_class = ad_soup.find_all('li', {'class': 'offer-bottombar__item'})
            added = added_class[0].text.strip().split(', ')[1]
            
            localization_class = ad_soup.find_all('div', {'class': 'offer-user__address'})
            city = localization_class[0].text.split()[0]
            district = localization_class[0].text.split()[2]

            price_class = ad_soup.find_all('div', {'class': 'pricelabel'})
            price = price_class[0].text.strip().split('\n')[0]
            price = int(price.replace(' ', '').replace('zł', ''))

            by_class = ad_soup.find_all('ul', {'class': 'offer-details'})
            by = by_class[0].a.strong.text

            level_class = ad_soup.find_all('li', {'class': 'offer-details__item'})
            level = level_class[1].a.text.strip().split('\n')[1]

            furniture_class = ad_soup.find_all('li', {'class': 'offer-details__item'})
            furniture = furniture_class[2].a.text.strip().replace('\n', ' ').split()[1]
            if furniture == 'Tak':
                furniture = 1
            else:
                furniture = 0

            building_class = ad_soup.find_all('li', {'class': 'offer-details__item'})
            building = building_class[3].a.text.split()[2]

            surface_class = ad_soup.find_all('li', {'class': 'offer-details__item'})
            surface = int(surface_class[4].text.strip().replace('\n', ' ').split()[1])

            rooms_class = ad_soup.find_all('li', {'class': 'offer-details__item'})
            rooms = rooms_class[5].text.strip().replace('\n', ' ').split()[2]

            rent_class = ad_soup.find_all('li', {'class': 'offer-details__item'})
            rent = int(rent_class[6].text.strip().replace('\n', ' ').split()[2])
            
            rows.append([link, added, city, district, price, by, level, furniture,
                         building, surface, rooms, rent])
        except Exception:
            pass
    print('pobrano dane z', len(rows), 'ogłoszeń.')
    return rows


def drop_value(df, column, value):
    """ funkcja do usuwania wybranych wartości """
    index = df[df[column] == value].index
    df.drop(index=index, inplace=True)
    df.reset_index(drop=True, inplace=True)
