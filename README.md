# Autonomous Utilization and Task Organization (AUTO)

## Introduction

Welcome to the AUTO project, a sophisticated ensemble of specialized AI agents designed to function in unison, providing a seamless integration of various expertise. This project's purpose is to demonstrate the capabilities of an advanced AI system that can autonomously organize and collaborate to achieve complex tasks through its comprehensive toolset. Each agent within the system possesses unique talents, ranging from data analysis to natural language processing, and from software development to creative design. This README serves as a guide to the project's functionalities, usage, and to introduce you to our multi-agent structure.

### Project's Purpose
The primary aim of AUTO is to offer an agile and flexible solution for tackling a variety of challenges across multiple domains. By harnessing the collective intelligence and specialized abilities of each agent, the system can adapt to new tasks rapidly and execute them with expert precision.

### Capabilities
Our system boasts a wide array of capabilities, including but not limited to:
- Autonomous use of specialized tools
- Real-time collaboration and decision-making
- Generation of custom technical utilities
- High-level problem solving in various fields

### Usage
Users can interact with the AUTO by providing tasks in natural language. The system analyzes the requirements, divides the work among agents based on their specializations, and collectively delivers the desired outcome.

### Self-Organized Multi-Agent System
Each agent in the AUTO has been engineered to operate both independently and as a unit. With a self-organized approach to problem-solving, the agents synchronize their actions to make full use of the system's capabilities, all without the need for centralized control. This level of autonomy ensures efficiency and effectiveness in a breadth of scenarios.

Enjoy exploring the capacities of our AI-driven initiative, where innovation and collaboration are at the core.

# Prereqs

TODO add this
- IDE: VS Code
- Python
- Git

# Set up

1. `python -m venv env`
2. `.\env\Script\activate`
3. `pip install -r .\requirements.txt`

# Get Started 

- `python main.py` and AUTO will wait for your prompt, or
- `python main.py "my prompt"` to get AUTO to respond to your command or query

# Samples

- Fetch the content of https://en.wikipedia.org/wiki/OpenAI and transpose this wikipedia page to a local markdown file

- I'd like some analysis help on creating a web scraper as a python utility. I intent on developing web scraping tool specifically for food recipes. I've heard of the python package 'beautifulsoup' is useful, but I've also found 'https://raw.githubusercontent.com/hhursev/recipe-scrapers/main/README.rst' and would like to know how to properly build a flawless web scraper for food recipes.

- Create a Python script that can flawlessly scrape the internet for food recipes based on a user-provided input of a food item name (e.g., 'French Onion Burger'). The script retrieves a minimum of 5 matching recipes from various sites, extracting image URLs, ingredients, servings, prep time, cooking time, directions, and optionally, any notes. All extracted data for each recipe is saved into a JSON file, organized as an array of recipe objects, encapsulating the respective information fields