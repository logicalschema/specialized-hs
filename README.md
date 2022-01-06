# NYC Specialized High School Offers By Middle School: 2016-2021


## Purpose
Every year students throughout the NYC public middle schools take the SHSAT exam to determine whether or not they will enter the city's specialized high schools. One test and it is increibly competitve. This code helps to provide a readable map and data for middle schools to see how many students tested and how many were given offers to attend a specialized high school. Note one limitation is that 0s are not recorded. The data is stored as 0-5 which throws off calculating any meaningful percentage.

The data sets I used are from the following sources:

* [NYC OpenData SHSAT Admissions Test Offers By Sending School: 2016-2021](https://data.cityofnewyork.us/browse?q=shsat)
* [NYC OpenData 2021 DOE Middle School Directory](https://data.cityofnewyork.us/Education/2021-DOE-Middle-School-Directory/f6s7-vytj)


## Getting Started

The Dash app is hosted at [https://sslee-specializedhs.azurewebsites.net/](https://sslee-specializedhs.azurewebsites.net/). You can go here to access the app. 

Click on the marker on the map to see information for the school. Select the year dropdown to see how the school did in comparison to others for that year.

### Dependencies

* Python
* Math
* Dash
* Plotly
* Venv
* Pip
* Platform to host: Azure was used as a cloud platform service, but Heroku or others can be used.

### Installing

* [GitHub repository](https://github.com/logicalschema/specialized-hs)

No installation is needed. You only need an active internet connection and a web browser.

### Executing program

* [https://sslee-specializedhs.azurewebsites.net/](https://sslee-specializedhs.azurewebsites.net/)

## Authors

Sung Lee 
[@logicalschema](https://twitter.com/logicalschema)

## Version History
* 0.5
    * Editing README, cleaning files, and fixing typos

* 0.4
    * Added Google Analytics code
    * Tested on desktop instance

* 0.3 
    * Committed to Azure
    * Launch
    * Edited css for divs not aligning properly on mobile devices
* 0.2
    * Cleaned data and combined OpenData NYC 2016 to 2021 for NYC DOE Middle Schools
* 0.1
    * Development

## License

This project is licensed under the [mit] License - see the LICENSE file for details

## Acknowledgments

Code snippets and tutorials:
* [Deploy on Azure](https://resonance-analytics.com/blog/deploying-dash-apps-on-azure)

