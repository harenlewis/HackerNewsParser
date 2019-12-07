## HackerNewsParser

#### Parses this website: https://news.ycombinator.com/ and extracts data from top page
---------

#### Problem Statement

1) List all stories on top page of https://news.ycombinator.com/ and write the data to a csv file.

2) Get user name and his karma points from top page.


#### To run the script

`./hn_parser.sh`


Parses the top page of Hacker News.
    Creates two csv files
    1) Stories sorted by comments.
       - filename: sorted_by_comments_{current_datetime}.csv
    2) List of all the stories rank wise
       - filename: hn_top_page_{current_datetime}.csv