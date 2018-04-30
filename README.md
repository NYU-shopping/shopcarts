[![Build Status](https://travis-ci.org/NYU-Shopcarts/shopcarts.svg?branch=master)](https://travis-ci.org/NYU-Shopcarts/shopcarts)

# shopcarts
Shopcarts RESTful service allows user to create, delete and modify items in their shopcarts.

Team: Pranay Pareek, Kedar Gangopadhyay, Weiwei Xu, Sisi Li



## Setup

For easy setup, you need to have Vagrant and VirtualBox installed. Then all you have to do is clone this repo and invoke vagrant:

```shell
    git clone https://github.com/NYU-Shopcarts/shopcarts.git
    cd shopcarts
    vagrant up && vagrant ssh
    cd /vagrant
```

You can now run behave and nosetests to run the BDD and TDD tests respectively.


## Manually running the Tests

These tests require the service to be running becasue unlike the the TDD unit tests that test the code locally, these BDD intagration tests are using Selenium to manipulate a web page on a running server.

Run the tests using behave

```shell
    $ python run.py &
    $ behave
```

Note that the & runs the server in the background. To stop the server, you must bring it to the foreground and then press Ctrl+C

Stop the server with

```shell
    $ fg
    $ <ctrl+c>
```

This repo also has unit tests that you can run nose

```shell
    $ nosetests
```





