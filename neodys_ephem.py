#! /usr/bin/python3

from bs4 import BeautifulSoup
import urllib.request
import configparser as cfg
import os
import sys


cli_args = sys.argv


def main_query_form(config):
    ra_beg = config.get('MainQuery', 'ra_beg_deg')
    ra_end = config.get('MainQuery', 'ra_end_deg')
    de_beg = config.get('MainQuery', 'de_beg_deg')
    de_end = config.get('MainQuery', 'de_end_deg')
    vmag_beg = config.get('MainQuery', 'vmag_beg')
    vmag_end = config.get('MainQuery', 'vmag_end')
    sole_beg = config.get('MainQuery', 'sole_beg_deg')
    sole_end = config.get('MainQuery', 'sole_end_deg')
    ph_beg = config.get('MainQuery', 'ph_beg_deg')
    ph_end = config.get('MainQuery', 'ph_end_deg')
    galat_beg = config.get('MainQuery', 'galat_beg_deg')
    galat_end = config.get('MainQuery', 'galat_end_deg')
    dfe_beg = config.get('MainQuery', 'dfe_beg_au')
    dfe_end = config.get('MainQuery', 'dfe_end_au')
    dfs_beg = config.get('MainQuery', 'dfs_beg_au')
    dfs_end = config.get('MainQuery', 'dfs_end_au')
    motion_beg = config.get('MainQuery', 'motion_beg_degpday')
    motion_end = config.get('MainQuery', 'motion_end_degpday')
    sp_unc_beg = config.get('MainQuery', 'sp_unc_beg_arcmin')
    sp_unc_end = config.get('MainQuery', 'sp_unc_end_arcmin')
    days_unobs_beg = config.get('MainQuery', 'days_unobs_beg')
    days_unobs_end = config.get('MainQuery', 'days_unobs_end')
    arclen_beg = config.get('MainQuery', 'arclen_beg_days')
    arclen_end = config.get('MainQuery', 'arclen_end_days')
    sortby = config.get('MainQuery', 'sortby')
    
    webquery = 'http://newton.spacedys.com/neodys/index.php?pc=3.2.1&pc0=3.2' + \
               '&lra=' + ra_beg + '&ura=' + ra_end + \
               '&lde=' + de_beg + '&ude=' + de_end + \
               '&lvm=' + vmag_beg + '&uvm=' + vmag_end + \
               '&lel=' + sole_beg + '&uel=' + sole_end + \
               '&lph=' + ph_beg + '&uph=' + ph_end + \
               '&lgl=' + galat_beg + '&ugl=' + galat_end + \
               '&ldfe=' + dfe_beg + '&udfe=' + dfe_end + \
               '&ldfs=' + dfs_beg + '&udfs=' + dfs_end + \
               '&lmo=' + motion_beg + '&umo=' + motion_end + \
               '&lspu=' + sp_unc_beg + '&uspu=' + sp_unc_end + \
               '&ldu=' + days_unobs_beg + '&udu=' + days_unobs_end + \
               '&lal=' + arclen_beg + '&ual=' + arclen_end + '&sb=' + sortby
    return webquery


def body_query_form(body, config):
    obs_code = config.get('BodyQuery', 'obs_code')
    year0 = config.get('BodyQuery', 'utc_beg_year')
    year1 = config.get('BodyQuery', 'utc_end_year')
    month0 = config.get('BodyQuery', 'utc_beg_month')
    month1 = config.get('BodyQuery', 'utc_end_month')
    day0 = config.get('BodyQuery', 'utc_beg_day')
    day1 = config.get('BodyQuery', 'utc_end_day')
    hour0 = config.get('BodyQuery', 'utc_beg_hour')
    hour1 = config.get('BodyQuery', 'utc_end_hour')
    min0 = config.get('BodyQuery', 'utc_beg_min')
    min1 = config.get('BodyQuery', 'utc_end_min')
    tint_val = config.get('BodyQuery', 'tint_val')
    tint_unit = config.get('BodyQuery', 'tint_unit')
    
    webquery = 'http://newton.spacedys.com/neodys/index.php?pc=1.1.3.1' + \
               '&n=' + body + '&oc=' + obs_code + \
               '&y0=' + year0 + '&m0=' + month0 + '&d0=' + day0 + \
               '&h0=' + hour0 + '&mi0=' + min0 + \
               '&y1=' + year1 + '&m1=' + month1 + '&d1=' + day1 + \
               '&h1=' + hour1 + '&mi1=' + min1 + \
               '&ti=' + tint_val + '&tiu=' + tint_unit
    return webquery


################################ Main Code ####################################

fn = 'neodys_lst.html'

config = cfg.RawConfigParser()
config.read('neodys.ini')

topdir = cli_args[1]          #config.get('Parameters', 'savedir')
if os.path.exists(topdir) == False:
    os.makedirs(topdir)

w = main_query_form(config)
urllib.request.urlretrieve(url=w, filename=fn)

with open(fn) as fp:
    soup = BeautifulSoup(fp, 'lxml')
    href = soup.find_all('a', {'class': 'colorNeaLink'})
    for i in range(len(href)):
        body_name = href[i].contents[0].split()[0].strip('()')
        body_fn = href[i].contents[0].split()[-1]
        print('loading ephemeris for ', body_name, body_fn)
        bw = body_query_form(body_name, config)
        b_path = os.path.join(topdir, body_fn + '.html')
        urllib.request.urlretrieve(url=bw, filename=b_path)
        with open(b_path) as bfp:
            bsoup = BeautifulSoup(bfp, 'lxml')
            bhref = bsoup.find_all('a', {'class': 'downloadButton'})
            # print(bhref[0]['href'])
            urllib.request.urlretrieve(url= 'http://newton.spacedys.com/neodys/' + \
                                       bhref[0]['href'],
                                       filename=os.path.join(topdir, body_fn + '.neo'))
            os.remove(b_path)
            print('Done')

