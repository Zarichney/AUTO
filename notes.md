# Vision

  An AI platform as the central entity, designed to service user needs through acquiring information and executing tasks, autonomously yet iteratively fine-tuned via feedback. 

  ## Expanded Concept

  ### AI-Driven Business Transformation
  - Embracing a shift to an AI-centric business model, this platform is poised to revolutionize traditional operations, catering efficiently to the dynamic needs of the modern business landscape.

  ### Efficiency Through Automation
  - Core to this vision is leveraging AI agents for precision-driven task execution. The integration of these agents is anticipated to substantially diminish manual labor while streamlining diverse business processes.

  ## User Interaction and Employee Empowerment

  ### Personalized AI Assistants
  - Each employee will engage with a bespoke AI assistant, echoing their unique role within the organization. These assistants, bridging employees with the AI agency, promise context-sensitive support and optimized task facilitation.

  ### Streamlined Command-and-Review Mechanism
  - Focusing on a user-friendly workflow, the platform will enable employees to interact using natural language. This system is designed to reflect commands in real-time for subsequent review and confirmation, enhancing both ease and efficiency.

  ## Safety and Forward Thinking

  ### Secure Automation in Drafting Processes
  - Prioritizing safety in automation, especially in the creation and modification of system documents and entities, this approach ensures reversible and secure automated actions, upholding high standards of data integrity.

  ### Vision of a Streamlined Future
  - This platform is not just about pioneering solutions for today's business challenges but also about evolving continuously. It aims to stay ahead in the realm of business efficiency and employee engagement by harnessing advancements in AI and technology.

  ## Expectation

  Capable of handling any request that is within the agency's scope of operation

  That it's to be good in both a general way:
    To be able to handle whatever is thrown at it

  , but also excels in a specific way:
    To produce high quality deliverables by executing complex tasks

  ## Capability Scaling Strategy

  - The more **agents** are added to the agency:
    - The more quality is expected to it's generality
      - By becoming more specialized

  - The more **tools** are added to the agency:
    - The more quality is expected to the deliverables
      - By adding more precision to execution
    - The more execution efficiency increases
      - By adding more automation to execution
      - By adding more control on execution expectations

  - The more **processes** are defined in the agency:
    - The more quality is expected out of the deliverables
    - The more execution efficiency increases

____________________________________________________________________

# System Entities & Concept Definitions:

  ## Agency
    - The singular and central entity that encapsulates the concept of the entire system

  ## Agent
    - The entity that carries out actions
      - Makes independent decision on tool usage and choice of response
      - Expected to be fully compliant in agency's supplied instructions 

    - Defined with: 
      - Name         : Succinct way to identify agent with indication of their specialization
      - Description  : Short text that describes the agent's specialization
      - Services     : Examples of reasons to engage the agent
      - Background   : Contextual information that activates the agent's specialization 
      - Methodology  : The agent's suggested approach of conducting
      - Tools        : A description of tool usage expectations related to their specialization

    - System design reasoning
      - A fundamental part of the design because it acknowledges that diversity of contextual roles is an assumed tactic for producing higher quality of outputs & deliverables.
      - Higher quality is fabricated by the build up of the various niches and specializations that assisted in the break down of the given context (into the respected manageable parts).
      - The more specific the relevant agents are to the mission, the more the agency engages in breaking down a given context into the specified specializations, hence the incentive to create more agents to increase output quality.
      - Reflects the natural design of human organization, the backbone of society and business.
    
  ## Tool
  - An action taken by an agent that interacts with the environment.
    - **External** interactions: Executing code to interact with the digital environment
      - File Management
      - Data management
      - Internet Access
      - External System Integrations
      - Communication Management (via supported protocols such as email, slack, etc) 
    - **Internal** interactions: Performing orchestration actions in the agency that conducts the overall cognitive process
      - Assess - used to critically think about a prompt
      - Plan - used to receive a step by step workflow from the agency
      - InitiateProcess - used to execute a predefined process
      - Inquire - used to request information from the agency (the agency will defer the request to the appropriate agent)
      - Interrogate - used to get engaged in a conversation with the user or another agent. Used for clarifying expectations or to get feedback
      - Delegate - used to handoff the mission to another agent

  - Defined with:
    - Name        : Tool identifier
    - Description : Short text that describes the tool's purpose
    - Inputs      : List of inputs that the tool requires to operate
    - Output      : Description of what is expected from the tool result

  - Execution is explictly programatically defined using python code in agency project

  ## Intake
    - The process of engaging with the agency
    - The initial user prompt that activates the agency's operation
    - Series of initial interactions in respect to the user's prompts to establish a mission
    - To be aborded by the user at any time
    - Explicitly programmatically defined in the agency's code
        
  ## Process
    - A Predefined Plan (inherits the plan definition)
      - A plan generated during run time are autonoumously created and executed, dynamically influenced by the context
      - A predefined process is designed, defined, developed, tested using human developer decisions
    - An agency's approved workflow that can be executed by an agent
    - Assumes the agency is in a prerequired state when execution begins

    - Defined by:
      - Name         : Process identifier
      - Description  : Short text that describes the process's purpose
      - Requirements : A list of prerequirements that the agency must be in before the process can be executed
      - State        : Dynamic data structure that holds the process's state
      - Checks       : A list of logical checks used to identify where in the flow the process is at

    - The last step of a process is to run the user feedback loop
    
  ## Plan
    - An intention to operate with a purpose to achieve a goal
    - A generated sequential step by step worflow

    - Defined by:
      - Inputs
        - Goal        : The purpose of the plan
        - Expectation : The user's expectation of the deliverable
      - Output
        - Steps       : A list of sequential steps that the process is expected to execute

    - User feedback is required when the deliverable has an influence on user expectation(s)
    - Approval is required unless the plan is a predefined process
      
  ## Goal
    - The purpose of the mission
    - Defined by:
      - Inputs
        - Deliverable : A description of what the goal is seeking to accomplish or produce
        - Expectation : The user's expectation of the deliverable(s)
      - Output
        - Artifacts   : A list of possible artifacts that make the deliverable(s)

  ## Mission
    - An execution of the agency's operation
    - An instance of a plan
    - Defined by:
      - Goal   : The purpose of the mission
      - Plan   : The plan to achieve the goal
      - Status : The current step of the plan

  ## Task
    - A plan step
    - An action to be carried out by an agent via tool usage

  ## Artifact
    - Something that is iteratively frabricated using digital means
    - It can be in the form of something that:
      - Occupies storage (such as a single file or a repository of files), or 
      - Can be represented using data (such as an idea or a concept)
    - Defined by:
      - Name        : Artifact identifier
      - Type        : The type of artifact
      - Description : Short text that describes the artifact's purpose

    ### Artifact Type
      - A predefined set of instructions on how to create the artifact
      - Defined by:
        - Name         : Artifact type identifier
        - Description  : Short text that describes the artifact type's purpose
        - Instructions : A list of instructions on how to create the artifact

____________________________________________________________________

# Processes

  ## Operate
    - Prerequirement: prompt is relevant to the agency's operation
    - The external process that is offered to the user
    - The initial trigger to engage the agency

  0. Instantiate Agency, Runtime Environment, and set up User Agent

  1. Receive User Prompt

  Feature Toggle
    2. Gate keeper assesses
    Matched Scenario: Not a request for agency's operation
      3. Gate keeper responds
      99. Run User Feedback Loop

  3. Run Intake Process
  99. Run User Feedback Loop 


  ## Intake
    - Prerequirements: 
      - Agency has user prompt
      - Agency has no mission set
    - The process of assessing the user's prompt and identify an execution plan

  1. Determine if prompt can be fulfilled in a single action? Assess whether a plan is not needed
  Matched Scenario:
    2. Get User Agent to handle prompt
    99. Run User Feedback Loop

  2. Determine whether the prompt is a request that a predefined process fulfills
  Matched Scenario:
    3. Run InitiateProcess Tool
    99. Run User Feedback Loop

  3. Determine if prompt is relevant to agency's supported speciality
  Matched Scenario:
    4. Run Delegate Tool to relevant agent with instruction to run intake process
    99. Run User Feedback Loop

  4. Run Assess Tool to identify whether the prompt is a query or command

  5. Run Plan tool using understanding of whether user request is for information or for work

  6. Get feedback or approval from user
  Matched Scenario: User approved of plan
    7. Run Execute Process
    99. Run User Feedback Loop

  7. User respond with feedback
  Matched Scenario: User approved of plan
    8. Run Execute Process
    99. Run User Feedback Loop

  99. Run User Feedback Loop


  ## Execute
    - Prerequirements: 
      - Agency has a mission (and plan) set
    - The process of executing a plan

    1. Delegate to relevant agent according to step 1 of plan

    2. Evaluate plan status
    Matched Scenario: Plan is not complete
      3. Engage User Agent to execute next step

    3. Evaluate goal against artifacts
    Matched Scenario: Goal is not complete
      4. Engage User Agent to execute next step

    4. Respond to user with deliverable


  ## Cookbook Building
    - Prerequirements:
      - User prompt is for a cookbook
    - Purpose: To create a personalized cookbook by compiling a series of recipes based on user preferences.

    1. **Gather User Preferences**
      - Agent: Culinary Agent
      - Tool: CreateUserProfile
      - Description: Collect dietary preferences and cookbook expectations to build a detailed user profile.

    2. **Create Cookbook Index Artifact**
      - Agent: Culinary Agent
      - Tool: CreateArtifact (Cookbook Index)
      - Description: Create an artifact representing the cookbook index based on the user profile.

    3. **User Review and Approval of Index**
      - Agent: Culinary Agent
      - Tool: ReviewAndApprove
      - Description: Present the cookbook index to the user for review and revisions. Obtain user approval before proceeding.

    4. **Execute Looped Subprocess: Recipe Generation**
      - Agent: Culinary Agent
      - Tool: LoopManager
      - Parameters:
        - Process: Recipe Creation
        - Loop: List of recipes
        - Context: UserProfile artifact
      - Description: Run the recipe generation loop, creating each recipe using the defined process.

    5. **Compile Cookbook**
      - Agent: Culinary Agent
      - Tool: PDFCompiler
      - Description: Assemble the created recipes into a well-formatted cookbook PDF.

    6. **Final Quality Check**
      - Agent: QA Agent
      - Tool: ReviewAndApprove
      - Description: Conduct a final review of the compiled cookbook to ensure it meets quality standards.

  ## Recipe Creation
    - Prerequirements:
      - User prompt is for a recipe
    - Purpose: To create a recipe inspired by user preferences and quality standards.

    1. **Scrape Recipe**
      - Agent: Culinary Agent
      - Tool: InitiateProcess
      - Parameters:
        - Process: Recipe Scraping
        - Input: Recipe (process input aka user prompt)
        - Context: UserProfile artifact
        - Output: RecipeData artifact
      - Description: Execute process 'Recipe Scraping'

    2. **Ingest Artifacts**
      - Agent: Culinary Agent
      - Tool: IngestArtifacts
      - Description: Ingest the user profile, the recipe template and the scrapped recipe data for recipe creation

    3. **Generate Recipe**
      - Agent: Culinary Agent
      - Tool: RecipeGenerator
      - Description: Use the recipe data to generate a new recipe, adhering to a specified template and incorporating prompt engineering instructions.

  ## Recipe Scraping
    - Prerequirements:
      - User prompt is for a recipe
    - Purpose: To create a recipe inspired by user preferences and quality standards.

    1. **Scrape Recipe**
      - Agent: Culinary Agent
      - Tool: RecipeScraper
      - Description: Retrieve a collection of recipes from the internet
      - Input: recipe (string param)
      - Output: File name

    2. **Review Recipes**
      - Agent: Culinary Agent
      - Tool: ReadFile
      - Description: Review the scraped recipe data that was retrieved from the internet
      - Input: file name (string param)
      - Output: None (file ingested)

    3. **Clean and Sanitize Scraped Data**
      - Agent: Culinary Agent
      - Tool: CreateArtifact
      - Description: Review the scraped recipe data for relevancy, creating a clean and relevant dataset for recipe generation.
      - Notes: the idea here is that CreateArtifact will refer to the artifact type to pull predefined instructions on how to create the artifact aka the clean up rules
      - Input:
        - Artifact type: Recipe Data
        - Context: Scrapped recipes
      - Output: File name

    4. **Process Complete**
      - Output: File name of cleaned recipe data


























<!-- 
____________________________________________________________________

# Tools

  ## Assess:
    Goal: Use critical thinking to understand the prompt and generate a well thought out response
    Input: Prompt
    Process:
      0. Active agent has their background instructions set up
      1. Start thread
        1.1 Add user message of initial instruction "You are assessing:"
        1.2 Add user message of supplied prompt
      2. Understand prompt nature
        2.1 Add user message  
        1.1 Determine if the prompt is a query (request for information) or command (request for deliverable)
        1.2 Determine assumption of user's expectation
      2. Determine train of thought
        2.1 Use prompt, 1.1 & 1.2 to prompt engineer an instruction to create train of thought
      3. Generate response
    
    
  ## Plan: -->
