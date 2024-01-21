# SQLite_Grammar_Fuzzer

# Setting up the Docker Framework
Docker is one of the most popular containerization software and has become one of the most widely used industry standards. In this project, Docker will serve to encapsulate all project dependencies as well as provide the same operational layer for all students. If you do not have Docker installed on your computer, refer to the get-started guide Docker provides. Once you have installed Docker, you can get started with your project by following these steps:

### 1. Build the Docker Image:
First, you need to build the Docker image using the provided Dockerfile. Open your terminal and navigate to the directory containing the Dockerfile and the project1 folder. 
Use the following command to build the image. 
  `docker build -t sectest .` 
The `-t` flag allows you to specify a name (in this case, "sectest") for the image.

### 2. Run the Docker Container:
Once the image is built, you can run the Docker container with the following command: 
  `docker run -d --name sectest_container -v sectest:/app -p 6080:80 sectest`
This command maps port 6080 on your host to port 80 inside the container and names the container "sectest_container", using the "sectest" image.
  - The `-d` flag runs the container in detached mode, allowing you to use the terminal for other tasks. 
  - The `--name` flag sets up a name for the container. 
  - The `-v` flag creates and maps the volume named "sectest" on the host system to the directory "/app" inside the Docker container. 

### 3. Stop and restart the Docker Container
If you want to stop a running container without losing progress, use the docker stop command, specifying the container's name or ID:
`docker stop sectest_container`
If you've stopped the container and want to restart it, use the docker start command. This command will ensure the same volume is executed, so you will not lose the progress you have made:
`docker start sectest_container`


### 4. Accessing the GUI and Tools:
After starting the Docker container, you can access the GUI (http://localhost:6080/) and various tools as follows:
  a. Terminal: Open a terminal within the Docker environment by navigating to "Start," "System Tools," and selecting "LXTerminal."
  b. File Explorer: Open the file explorer by going to "Start", "System Tools", and selecting "File Manager PCManFM"
  c. Web Browser: Open your web browser by going to "Start," "Internet," and selecting either Mozilla Firefox or Google Chrome.
  d.JupyterLab: To work with Jupyter notebooks, you can open a terminal within the Docker environment and run the following command:
    `python3.10 -m jupyterlab --allow-root`
    This command will start JupyterLab, and you can access it through your web browser by visiting the URL provided in the terminal.


# Project Tasks
There are two tasks in this project:
1. Implement a diverse SQLite grammar in grammar.py which is able to generate all commands understood by SQLite. The grammar should be general: For instance, a CREATE TABLE command should be able to generate diverse table names. The page at https://www.sqlite.org/lang.html provides very detailed information about all commands of SQLite.

2. Implement the function fuzz_one_input in fuzzer.py. The signature of this function must not be changed. The function should implement a grammar-based black box input generation for SQLite. You may add arbitrary code and functions in this file, but the entry point must be fuzz_one_input. Be creative in this task, and come up with ways to generate interesting inputs!


# Evalution:
### 1. Branch coverage in sqlite3.c (5 points)
We will measure how much branch coverage your fuzzer achieves in sqlite3.c. During the evaluation, we will use your fuzzer to generate 100.000 inputs and measure the branch coverage achieved in SQLite. We will repeat this measurement five times and use the mean branch coverage. This part contributes to your final project grade as follows: 5 * (your_mean_branch_coverage / goal_branch_coverage)

### 2. Bug finding capability (3 points)
If your fuzzer is able to trigger an error or crash in SQLite, you will get extra points. Note that finding a bug in SQLite might be difficult. Hence, when we grade your submission, we will introduce several bugs into the SQLite implementation and evaluate the ability of your fuzzer to discover them. During this measurement, we will seed one bug at a time, and check whether your fuzzer can trigger it with a budget of generated inputs. This part contributes to your final project grade as follows: 3 * (#your_found_bugs / #goal_found_bugs)

### 3. Input diversity (2 points)
We will assess how diverse the inputs that your fuzzer generates are. To measure this, we will define a number of interesting input features (e.g. a specific edge case of the CREATE TABLE command), and check if your fuzzer can generate an input that includes this feature, with a budget of 100.000 generated inputs. This part contributes to your final project grade as follows: 
2 * (#your_interesting_input_features / #goal_interesting_input_features)


# Goals:
- Dimension 1: The goal branch coverage is 45%. Reaching at least 45% gives you 5/5 points in this dimension.

- Dimension 2: We introduced 30 bugs into SQLite. If your fuzzer could trigger at least 20 of them, you get 3/3 points.

- Dimension 3: We measured how many syntactically different inputs your fuzzer produces. If your fuzzer could generate at least 1000 syntactically different inputs, you get 2/2 points.


# Points Acquired
- Branch coverage:  	3.9222 / 5		
- Bugs:			          2.85 / 3		
- Input diversity:		2 / 2
