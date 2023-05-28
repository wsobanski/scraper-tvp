import os
import pickle
import argparse
from time import time
from time import sleep
from random import random, randrange

import pandas as pd

from utils import obtain_info



def job(page_link : str, start_page : int, end_page : int, domain : str):
    """
    Main function for obtaining links to the articles.
    Function saves the output to .pkl file as tuple of lists.
    
    If function failed 5 times during execution then it stops the execution.
    
    params:
    
    page_link (str): formatable string
    domain (str): string representing section on tvp.info
    start_page (int): starting page
    end_page (int): last page to obtain
    
    returns:
    
    tuple of lists containg metadata about articles
    
    """
    result_links, result_leads, result_titles = [], [], []
    failed_counter = 0
    for page in range(int(start_page), int(end_page)+1):
        try:
            page_links, page_leads, page_titles = obtain_info(page_link,
                                                              domain = domain,
                                                              page = page)
            result_links.extend(page_links)
            result_leads.extend(page_leads)
            result_titles.extend(page_titles)
        except:
            if failed_counter == 5:
                print('Failed 5 times. Breaking loop')
                print(f'Last page obtained: {page}')
                break
            else:
                print(f'Failed obtaining page: {page} from domain: {domain}')
                failed_counter += 1
                pass
        # After obtaining data from one page wait for a while between 1-3 sec    
        sleep(random()*randrange(1,3))
    
    res = (result_links, result_leads, result_titles)
    save_path = f'{os.pardir}/results/results_{domain}_{start_page}-{end_page}.csv'
    
    # with open(save_path, 'wb') as f:
    #     pickle.dump(res, f)
    out = pd.DataFrame({'link' : res[0],
                        'title' : res[1],
                        'lead' : res[2]})
    out.to_csv(save_path, sep = ',', header=True)
    
    print('-' * 89)
    print('Output file saved in /results')
    
    return result_leads, result_links, result_titles



def main():
    
    start_time = time()
    parser = argparse.ArgumentParser(description="Scrapes linkt ot articles")
    parser.add_argument( "-d", "--domain",type = str,
                        default = 'biznes', help="section on tvp.info page")
    parser.add_argument("-s", "--start_page", type = int,
                        default = 1, help="starting page")
    parser.add_argument("-e", "--end_page", type = int,
                        default = 1, help = "last page")
    args = parser.parse_args()
    
    tvp_link = 'https://www.tvp.info/{domain}?page={page}'

    save_path = os.pardir + '../results'
    if os.path.exists(save_path) == False:
        os.makedirs(save_path)

    job(page_link = tvp_link,
        start_page=args.start_page,
        end_page=args.end_page,
        domain = args.domain)
    
    end_time = time()
    n_pages = args.end_page - args.start_page + 1
    exec_time = (end_time - start_time)/60
    print(f"Obtaining {n_pages} pages took:")
    print(f"{(exec_time):.3f} minutes")
    print(f"average time per page: {(exec_time/n_pages):.3f} min")
    
if __name__ == '__main__':
    main()