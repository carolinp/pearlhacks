#!/usr/bin/env python
from django.core.management.base import BaseCommand, CommandError
#from django.db.models import F
from bs4 import BeautifulSoup
from assault_app.models import Schools
#import string
import urllib2
import re

class Command(BaseCommand):
    args = '<url>'
    help = 'Parses and imports latest data'
    
    
    def handle(self, *args, **options):
        try:
            self.stdout.write("scraping stories")
                
            url = 'http://www.diamondbackonline.com/search/?t=article&s=start_time&sd=desc&d1=&q=sexual+assault' # write the url here
            usock = urllib2.urlopen(url)
            html_data = usock.read()
            usock.close()
            #print html_data
                
            soup = BeautifulSoup(html_data)

            #Find the div that all of the articles live in for the given url
            story_content = str(soup.find_all('ol', attrs={'class': 'articles'}));
 
            print story_content
            school_stories = Schools.objects.get(name='University of Maryland')
            school_stories.content = story_content
            school_stories.save(update_fields=['content'])
                
        except Schools.DoesNotExist:
            raise CommandError('didn\'t work')

        self.stdout.write("end of scrape.py")