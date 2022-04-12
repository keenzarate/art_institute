import requests
import json 
import os
import logging
import time
from datetime import date


class ArtInstituteApi():
    
    def __init__(self, 
        url,
        resources,
        page_pace,
        out_path 
    ):
        
        self.url = url,
        self.resources = resources
        self.page_pace = page_pace,
        self.out_path = out_path


    # define a function 
    def api_connect(self):

        page_n = self.page_pace
        resource = self.resources
        in_url = self.url

        # keep iterating until we hit the page_n limit
        while page_n == self.page_pace:

            # append the url  with limit args and page args
            full_url = in_url + resource + '?limit=' + str(page_n)

            print(f"requesting", full_url)

            # make the api call
            resp = requests.get(full_url)

            # retrieve the json
            json_out = resp.json()['data']

            return json_out


    # function to pull data from api and store to disk 
    def api_to_disk(self):
    
        # store in different list 
        artwork_list = []
        artist_list = []
        place_list = []

        # begin loop
        for res in self.resources:

            # create output path template
            output_template = os.path.join(self.out_path, date.today().strftime("%Y%m%d"),  f'{res}.jsonl')

            os.makedirs(os.path.dirname(output_template), exist_ok=True)

            # create a message so that we know which one we are pulling
            logging.info(f'pulling {res} from api')

            # call function that pulls data 
            out = self.api_connect(self.url, res, self.page_pace)
            
            # open the path to write on it
            with open(output_template, 'w') as f:
                # loop for each row from the output file 
                for row in out:
                    # what happens if the there isn't any data, raise a flag
                    if row is None:
                        print('empty')
                    # write the row by row
                    f.write(json.dumps(row) + '\n')
                # store list of path in the empty storage lists
                if res == 'artworks':
                    artwork_list = out
                elif res == 'artists':
                    artist_list = out
                elif res == 'places':
                    place_list = out

                # pause a bit so that api doesnt break connection 
                time.sleep(1)

        # spits out list of paths
        return(artwork_list, artist_list, place_list)
