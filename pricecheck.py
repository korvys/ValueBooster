'''
Created on 13/06/2013

@author: korvys

Contains functions related to checking the price of a card.

TODO: Fix the seek at the start of the price file update.
TODO: Add exception handling for file and url io.
'''


from urllib2 import urlopen
from decimal import *

import logging
logging.basicConfig(filename='pricecheck.log',
                    format='%(asctime)s: %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG
                    )



class PriceCheck():
    def __init__(self, regular_url='http://supernovabots.com/prices_0.txt', foil_url='http://supernovabots.com/prices_3.txt', regular_filename=None, foil_filename=None):
        self.card_price_list = {}
        if regular_filename:
            self.card_price_list.update(self.update_card_prices(filename=regular_filename))
        else:
            self.card_price_list.update(self.update_card_prices(url=regular_url))

        if foil_filename:
            self.card_price_list.update(self.update_card_prices(filename=foil_filename))
        else:
            self.card_price_list.update(self.update_card_prices(url=foil_url))


    def get_price(self, cardname, cardset):
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


    def update_card_prices(self, url='http://supernovabots.com/prices_0.txt', filename=None):
        """Gets the current prices of cards.
        
        Gets the current prices of cards from supernovabots.com, or from a text file
        formated in the same way, and returns a dictionary for price lookups.
        
        Args:
            url: The url of the file, typically from supernovabots.com
            filename: Filename of a local file formated the same. If this is provided, the url is ignored.
            
        Returns:
            A dict mapping the cardname and set to the sell and buy prices (decimals).
            Foil cards have a cardname formated as 'Foil <cardname>'.
            Example:
            
            {('Foil Voice of Resurgence', '[DGM]'): (Decimal('37'), Decimal('40.75'))}
         
        """
        card_price_list = {}
        
        #TODO: Add exception handling for file and url io.
        if filename:
            price_list = open(filename)
            logging.debug('Load from file: %s' % filename)
        else:
            price_list = urlopen(url)
            logging.debug('Load from url: %s' % url)
    
        #TODO: This should be done better. If the bot list changes, then this seek will be wrong.
        price_list.read(288)
        for line in price_list:
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
                
                card_price_list[(name, cardset)] = (sell, buy)
    
        logging.debug('New card price list returned: %s cards' % len(card_price_list))
        return card_price_list

