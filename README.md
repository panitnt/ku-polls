## Online Polls for Kasetsart University

An application for conducting a poll or survey, written in Python using Django. It is based on the [Django Tutorial project](https://docs.djangoproject.com/en/4.1/intro/tutorial01/), with additional functionality.

This application is part of the [Individual Software Process](https://cpske.github.io/ISP/) course at [Kasetsart University](https://www.ku.ac.th/th).

## Install and Run

- To install this program

    ```git clone https://github.com/panitnt/ku-polls.git```

- Go to this project's directory

    ```cd ku-polls```

- Create `.env` file. Content same as sample.env file

- Create a new environment

    ```python -m venv env```

- Start the virtual env in bash or zsh

    ```. env/bin/activate```

- To install requirements of this projects in environment

    ```pip install -r requirements.txt```

- Create a new database by running migrations.

    ```python manage.py migrate```

- Import data using loaddata.

    ```python manage.py loaddata data/filename.json```

- To run this program

    ```python manage.py runserver```

## Project Documents

All project documents are in the [Project Wiki](https://github.com/panitnt/ku-polls/wiki).

- [Vision Statement](https://github.com/panitnt/ku-polls/wiki/Vision-Statement)
- [Requirements](https://github.com/panitnt/ku-polls/wiki/Requirements)
- [Development Plan](https://github.com/panitnt/ku-polls/wiki/Development-Plan)
- [Iteration 1 Plan](https://github.com/panitnt/ku-polls/wiki/Iteration-1-Plan) | [Iteration 1 Board](https://github.com/users/panitnt/projects/2/views/5)
- [Iteration 2 Plan](https://github.com/panitnt/ku-polls/wiki/Iteration-2-Plan) | [Iteration 2 Board](https://github.com/users/panitnt/projects/2/views/8)
- [Iteration 3 Plan](https://github.com/panitnt/ku-polls/wiki/Iteration-3-Plan) | [Iteration 3 Board](https://github.com/users/panitnt/projects/2/views/9)
- [Iteration 4 Plan](https://github.com/panitnt/ku-polls/wiki/Iteration-4-Plan) | [Iteration 4 Board](https://github.com/users/panitnt/projects/2/views/10)

## User-demo
| Username  | Password  |
|-----------|-----------|
|   isp-1   | isp1-test |
|   isp-2   | isp2-test |
|   isp-3   | isp3-test |
