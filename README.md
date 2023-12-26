# AUTO Agency (Autonomous Utilization and Task Organization)

## Project Description

Welcome to the AUTO Agency, an advanced Python-based command-line application that epitomizes the next step in human-computer interaction. AUTO Agency utilizes the OpenAI Assistant API in a multi-agent system where each agent independently plans, coordinates, and self-organizes, bringing a new level of autonomy and efficiency in task execution.
This unique system allows users to interact with their local computing environment and beyond through intuitive, plain English commands. From generating local files based on web content to crafting complex documents like a cookbook, AUTO Agency can perform a wide range of tasks that extend far beyond the capabilities of traditional AI systems like ChatGPT. As the project evolves, integration with REST APIs will open even more possibilities for seamless, natural language interactions.

Whether you're a developer looking for an intelligent script execution tool, or someone interested in the cutting-edge application of AI in everyday tasks, AUTO Agency offers a glimpse into the future of human-computer interaction.

## Prerequisites

Before setting up AUTO Agency, ensure you have the following installed:

- **IDE**: Visual Studio Code (VS Code)
- **Python**: A recent version of Python (preferably Python 3.8 or above)
- **Git**: For version control and cloning the repository

## Setup

To set up AUTO Agency on your local machine, follow these steps:

1. Clone the repository using Git.
2. Open the project in VS Code.
3. Create a virtual environment:

   ```bash
   python -m venv env
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     .\env\Scripts\activate
     ```

   - On Unix or MacOS:

     ```bash
     source env/bin/activate
     ```

5. Install the required dependencies:

   ```bash
   pip install -r .\requirements.txt
   ```

## Get Started

To start using AUTO Agency, you can:

- Run the main script and wait for AUTO to prompt you for a command:

  ```bash
  python main.py
  ```

- Directly provide a command or query as an argument:

  ```bash
  python main.py "your prompt here"
  ```

## Sample Usage

Here are some examples of how you can use AUTO Agency:

1. **Stock Comparison**:
   
   ```bash
   python main.py "compare Google and Apple stocks over the past week"
   ```

2. **Create a Local File**:
   
   ```bash
   python main.py "create a file with content from the OpenAI Wikipedia page"
   ```

3. **Draft a Document**:
   
   ```bash
   python main.py "draft a recipe for a chocolate cake"
   ```

Remember, AUTO Agency is designed to understand and execute a wide range of tasks, so feel free to experiment with different prompts!

# Capabilities

## Agents

AUTO Agency is powered by a team of independent and collaborative specialized agents, each with unique skills and roles.

- **User Agent**: Central coordinator, orchestrates task flow, formulates and adapts strategic plans, and delegates tasks.
- **Coder Agent**: Specializes in programming and technical matters, responsible for creating and modifying code.
- **Quality Assurance Agent**: Ensures the quality and reliability of solutions, reviews code, and conducts tests.
- **Culinary Agent**: Expert in food and recipes, capable of finding, creating, and suggesting recipes.

## Tools

AUTO Agency's tools are available at the disposal of each agents. They decide when the right tool is required for the job.

### Organizational Tools
- **Plan**: Generates actionable workflows.
- **Delegate**: Appoints an agent as the active agent for task handling.
- **Inquire**: Obtains information from other agents.

### File Management Tools
- **ReadFile**: Reads contents of a local file.
- **CreateFile**: Creates a file with specified content.
- **MoveFile**: Moves or renames files within the local system.
- **GetDirectoryContents**: Lists files in a specified directory.

### Programming Tools
- **ExecutePyFile**: Safely runs local Python files, with internet access and standard Python packages.
- **DownloadFile**: Downloads files from the internet using a URL.

### Agent-Specific Tools
- **RecipeScraper** (Culinary Agent): Scrapes the internet for recipes, returning a JSON array of relevant results.

## Agency

### Session Management
- Ability to automatically restore the conversational state simply by using the same initial prompt

### Capabilitity Roadmap
- Continuous introduction of new agents & tools
- API system integration (at the agency level, agents can perform this)
- Persistent storage for messages (prompts, responses & tool output)
- Built-in Cache (reduce cost on repeated tasks & conversations)
- Robust execution of quality-expected deliverables (such as a complete cookbook)
- File management enhancements (introduce chunking to handle large files)
- Long term memory (implementation of vector database)
- User interface