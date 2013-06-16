'''
Created on 13/06/2013

@author: korvys

Contains classe and functions related to checking the price of a card.

TODO: Add better exception handling for file and url io.
'''


from urllib2 import urlopen, URLError
from decimal import *

import logging
logging.basicConfig(filename='pricecheck.log',
                    format='%(asctime)s: %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG
                    )



class PriceCheck():
    def __init__(self
                 , regular_url='http://supernovabots.com/prices_0.txt'
                 , foil_url='http://supernovabots.com/prices_3.txt'
                 , booster_url='http://supernovabots.com/prices_6.txt'
                 , regular_filename=None
                 , foil_filename=None
                 , booster_filename=None):

        
        self.card_price_list = {}
        
        if regular_filename:
            self.card_price_list.update(self.update_prices(filename=regular_filename))
        else:
            self.card_price_list.update(self.update_prices(url=regular_url))

        if foil_filename:
            self.card_price_list.update(self.update_prices(filename=foil_filename))
        else:
            self.card_price_list.update(self.update_prices(url=foil_url))

        
        self.booster_price_list = {}

        if booster_filename:
            self.booster_price_list.update(self.update_prices(filename=booster_filename))
        else:
            self.booster_price_list.update(self.update_prices(url=booster_url))



    def get_card_price(self, cardname, cardset):
        if (cardname, cardset) in self.card_price_list:
            prices = self.card_price_list[(cardname, cardset)]
            if not prices[0] and not prices[1]:
                return Decimal(0)
            elif not prices[0]:
                return prices[1]
            elif not prices[1]:
                return prices[0]
            else:
                return (prices[0] + prices[1]) / 2
        else:
            return Decimal(0)
    
    
    def get_booster_price(self, boostername, cardset):
        if (boostername, cardset) in self.booster_price_list:
            prices = self.booster_price_list[(boostername, cardset)]
            if not prices[0] and not prices[1]:
                return Decimal(0)
            elif not prices[0]:
                return prices[1]
            elif not prices[1]:
                return prices[0]
            else:
                return (prices[0] + prices[1]) / 2
        else:
            return Decimal(0)


    def update_prices(self, url='http://supernovabots.com/prices_0.txt', filename=None):
        """Gets the current prices of cards or boosters.
        
        Gets the current prices of cards or boosters from supernovabots.com, or from a text file
        formated in the same way, and returns a dictionary for price lookups.
        
        Args:
            url: The url of the file, typically from supernovabots.com
            filename: Filename of a local file formated the same. If this is provided, the url is ignored.
            
        Returns:
            A dict mapping the name and set to the sell and buy prices (decimals).
            Foil cards have a cardname formated as 'Foil <cardname>'.
            Example:
            
            {('Foil Voice of Resurgence', '[DGM]'): (Decimal('37'), Decimal('40.75'))}
        """
        price_list = {}
        
        try:
            if filename:
                price_file = open(filename)
                logging.debug('Load from file: %s' % filename)
            else:
                price_file = urlopen(url)
                logging.debug('Load from url: %s' % url)
        except (URLError, IOError):
            #TODO: Better exception handling.
            logging.error('Failed to open price file.')
            return {}
    
    
        #Skip the start of the file.
        for i in range(7):
            price_file.readline()


        for line in price_file:
            if len(line.strip()) > 0 and line[0] != '=':
                name = ' '.join(line[0:50].strip().split(' ')[:-1])
                cardset = line[0:50].strip().split(' ')[-1]
                
                sell = line[51:56].strip()
                if sell:
                    sell = Decimal(sell)
                else:
                    sell = None
                
                buy = line[61:66].strip()
                if buy:
                    buy = Decimal(buy)
                else:
                    buy = None
                
                price_list[(name, cardset)] = (sell, buy)
    
        logging.debug('New price list returned: %s entries' % len(price_list))
        return price_list

