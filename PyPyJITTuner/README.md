COMPONENTS:
======================
    LoadGenerator:
-----------------
        LoadGenerator will generate workload to the target server. The LoadGenerator need to deploy on servers whose performance would not bottleneck the generator.

    TestDriver:
----------------
        TestDriver will take command from TestScheduler. It will start the server under given configuration and invoke LoadGenerator to generate corresponding workload to the server. TestDriver needs to be deployed on a number of unique and clear servers. In our case, we deployed three TestDrivers.
 

    TestScheduler:
-----------------
        TestScheduler provides configurations that needs to be evaluated to the TestDriver. And it will get the server performance under each configuration with which it can make comparison and optimize the configurations with genetic algorithm.

SETUP:
====================
    Get a number of servers to build up the testing environment. The IP of different servers are as follows:
    LoadGenerator: LG_IP1, LG_IP2, LG_IP3
    TestDriver: TD_IP1, TD_IP2, TD_IP3
    TestScheduler: TS_IP
    Note: each of the servers should accessable with no password SSH.

    Setup LoadGenerator:
----------------------
        1. Copy the LoadGenerator to three different servers.
        2. Change the jmeter testing plan in the folder of three applications. (saleor, wagtail, quokka)
            a. change the parameter 'ip_addr' to the address of corresponding TestDriver. (e.g. LG_IP1 to LG_IP3)
            b. change the parameter, 'response_time_output' to the folder that you want to keep the imtermediate results.
        3. keep note of the absolute path to the LoadGenerator as LG_Path.

    Setup TestDriver:
--------------------
        1. Copy 'pypy2-v5.7.1-linux64_with_dependencies.zip' to three test driver servers and unzip them. This package contains PyPy2-v5.7.1 with corresponding dependencies for the server. And keep note of the path to pypy as PYPY_PATH.

        2. Deploy the applications that are under testing. And we donate the path to the application as APP_PATH. For each of the application, the detailed approach to deploy the application can be found:
            a. Saleor: https://github.com/mirumee/saleor
            b. Wagtail: https://github.com/wagtail/wagtaildemo
            c. Quokka: https://github.com/rochacbruno/quokka
       
        2. Copy the TestDriver to three test driver servers.
        3. Change the configurations in 'load_test.cfg':
            a. replace the 'LG_Path' with LG_Path for LoadGenerator.
            b. config the 'client_ip' with corresponding IP address of LoadGenerator.
            c. config the 'client_user' to the corresponding user in the server of LoadGenerator.
            d. config the 'pypy_path' and 'app_path' accrodingly.

    Setup TestScheduler:
---------------------
        1. Setup R:
            a. install R in ubuntu: https://www.digitalocean.com/community/tutorials/how-to-install-r-on-ubuntu-18-04
            b. install package 'effectsize'.with R command: install.packages('effectsize')
        2. Copy 'TestScheduler' to a server. And copy 'pypy2-v5.7.1-linux64_with_dependencies.zip' and setup pypy envrionment with same approach as TestDriver.
        3. Change the configuration in 'load_test.cfg' accroding to the LoadGenerators and TestDrivers that we have configed previously.

TUNE CONFIGURATION:
========================
    After we have setup the environment for JIT parameter tuning, we can start the TestScheduler to tune the JIT configuration. 

    1. run 'pypy GA.py'.
    2. run 'pypy sort_pop.py'.

    The top configs can be found in the folder 'results/top_configs'.
