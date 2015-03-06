Windows Phone Store Appx Apps Crawler
===============

Crawler that gathers links for .appx Apps from Windows Phone Store (to download apps, use download.py `./download.py -i [/path/to/linksfile]`)

To run:
`scrapy crawl appx -a outputfile=[/path/and/name_of_output_file]`

How?
-----

Bing search engine indexes Windows Phone Store, making it easy to find appx applications by using the following query string:
`site:windowsphone.com AppxManifest.xml`

The crawler gets all the links resulting from the above query and downloads the application package found at that location



Dependencies
-------

- [scrapy](http://scrapy.org/)
- [wget](https://www.gnu.org/software/wget/)
