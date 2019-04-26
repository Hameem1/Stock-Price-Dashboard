# Historic Stock Price Dashboard

An interactive stock price dashboard which displays upto 5 years of historic stock data.
The user can select one or more stock symbols to view at once.
The dropdown shows all stock symbols supported for trading by the Investor’s Exchange.
Functionality such as zooming, hovering, toggling and dynamic updating is supported for all plots.

## Installation

#### Using a virtual environment

- Clone the repository.

- Create a virtual environment using the 'requirements.txt' file.

    <b>Note</b>: <i>`requirements_unversioned.txt` can also be used to get the latest versions of the required packages, 
    however, this is not guaranteed to work.</i>

- Run `python app.py`.

- In the browser, open `localhost:5000`

#### Using Docker

- Have Docker up and running.
    - Instructions for setting up docker can be found in the 
    [Step Detection using Machine Learning](https://github.com/Hameem1/Step-Detection-using-Machine-Learning#setting-up-docker) 
    repository.

- Run the following commands to start the application:
    - `docker pull hameem/stock-price-dashboard:prod`
    - `docker run -p 5000:5000 --name stock-price-dashboard --rm hameem/stock-price-dashboard:prod`

- To stop the application/container:
 
    `docker container stop stock-price-dashboard`
    
- To remove all dangling docker images (optional):

    `docker image prune -a`
    
- To remove all unused objects (optional):
    
    `docker system prune`
    
    OR
    
    `docker system prune --volumes`
    

## Demo

![](https://i.imgur.com/eGwD3AF.gif)