#-----------------------------------------------------------------------
# testregdetails.py
# Author: Bob Dondero, Amel Osman, Mohemeen Ahmed
#-----------------------------------------------------------------------

import sys
import time
import argparse
import playwright.sync_api

#-----------------------------------------------------------------------

MAX_LINE_LENGTH = 72
UNDERLINE = '-' * MAX_LINE_LENGTH

#-----------------------------------------------------------------------

def get_args():

    parser = argparse.ArgumentParser(
        description='Test the ability of the reg application to '
            + 'handle "primary" (class overviews) queries')

    parser.add_argument(
        'serverURL', metavar='serverURL', type=str,
        help='the URL of the reg application')

    parser.add_argument(
        'browser', metavar='browser', type=str,
        choices=['firefox', 'chrome'],
        help='the browser (firefox or chrome) that you want to use')

    args = parser.parse_args()

    return (args.serverURL, args.browser)

#-----------------------------------------------------------------------

def print_flush(message):

    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def run_test(server_url, browser_process, classid):

    print_flush(UNDERLINE)

    try:
        page = browser_process.new_page()
        page.goto(server_url)

        link = page.get_by_text(classid).first
        link.click()

        page.wait_for_selector('#classDetailsTable')
        class_details_table = page.locator('#classDetailsTable')
        print_flush(class_details_table.inner_text())

        page.wait_for_selector('#courseDetailsTable')
        course_details_table = page.locator('#courseDetailsTable')
        print_flush(course_details_table.inner_text())

    except Exception as ex:
        print(str(ex), file=sys.stderr)


#-----------------------------------------------------------------------

def main():

    server_url, browser = get_args()

    with playwright.sync_api.sync_playwright() as pw:

        if browser == 'chrome':
            browser_process = pw.chromium.launch()
        else:
            browser_process = pw.firefox.launch()

        run_test(server_url, browser_process, '8321')

        # Add more tests here.

        #running with missing classid
        run_test(server_url, browser_process, '')

        #testing long description
        run_test(server_url, browser_process, '8749')

        #testing multiple professors
        run_test(server_url, browser_process, '8749')

        #testing no professors
        run_test(server_url, browser_process, '10030')

        #testing multiple cross-listed classes
        run_test(server_url, browser_process, '8749')

        #testing with a lot of cross-listings and professors
        run_test(server_url, browser_process, '9032')

        #testing with a class that has no prerequisites
        run_test(server_url, browser_process, '8293')

        #testing with nonexistent class code
        run_test(server_url, browser_process, '9999')

        #testing with non-integer classid
        run_test(server_url, browser_process, 'abcd')

if __name__ == '__main__':
    main()
