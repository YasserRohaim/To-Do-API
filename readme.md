# ToyShop readme
### Introduction
A comprehensive backend API for a TO-DO web application with authentication and user management, task and category management to boost productivity.
### Project Support Features

* Users can signup and signin to their accounts 
* Authenticated users can access their tasks, categories.
* Authenticated users can create new categories and new tasks and assigning deadlines, priorities and categories
* Authenticated users can edit or delete task and category details 
  
### Installation Guide
To run this project you will need python installed on your machine first then:

* Clone the repo:

        git clone https://github.com/YasserRohaim/To-Do-API

* Install the app's dependencies:

          pip install -r requirements.txt
         
### Usage

*Run python manage.py runserver to start the server.
*open the website on port 8000


### API Endpoints
| HTTP Verbs | Endpoints | Action |

| POST | /to-do/signup | To sign up a new user account |

| POST | /to-do/signin | To login an existing user account |


| GET | /to-do/tasks | retrieve all the user tasks |

| GET | /to-do/tasks/:task_id | retrieves the data of a specific task belonging to the logged in user |

| POST | /to-do/tasks/create-task | create a new task |

| PUT | /to-do/tasks/update-task/:task_id | edits the data of a specific task belonging to the logged in user |

| DELETE | /to-do/tasks/update-task/:task_id | deletes a specific task belonging to the logged in user |

| DELETE | /to-do/tasks/delete-finished | deletes all finished tasks of the user |

| DELETE | /to-do/tasks/clear-tasks | deletes all tasks of the user |



| GET | /to-do/categories | retrieve all the categories created by the user |

| GET | /to-do/categories/:category_id | retrieve data of a specific category created by the user |

| POST | /to-do/categories/create-category | create a new category |

| PUT | /to-do/categories/update-category/:category_id | edits the data of a specific category belonging to the logged in user |

| DELETE | /to-do/categories/update-category/:category_id | deletes a specific category belonging to the logged in user |





### Technologies Used
* [Django](https://www.djangoproject.com/) This is a python open-source web framework with support for RESTful API development using Django REST framework


### License
This project is available for use under the MIT License.