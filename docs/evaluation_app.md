# Evaluation Application

- [Starting the Application](#starting-the-application)
- [View Page](#view-page)
  - [Sidebar](#sidebar)
  - [Tab View](#tab-view)
    - [Compare JSON](#compare-json)
    - [Source Nodes](#source-nodes)
    - [Parameter Set](#parameter-set)
    - [Evaluate](#evaluate)
      - [Score Evaluation](#score-evaluation)
      - [Error Evaluation](#error-evaluation)
      - [Reference Evaluation](#reference-evaluation)
      - [General Evaluation](#general-evaluation)
      - [Miscellaneous Evaluation](#miscellaneous-evaluation)

---

In order to accurately and consistently evaluate generated domains, such as those created with parameter searches, the BcoRag tool has an accompanying evaluation application that provides a more user friendly GUI.

## Starting the Application

The evaluation application can be run from the `main.py` entrpoint using the `evaluate` positional argument like so:

```bash
(env) python main.py evaluate
```

On startup, you will be presented with the login screen. The login mechanism is a naive first and last name login that just keeps track of which domains you have already evaluated and what scores you submitted for each domain. If you are a new user, you'll be prompted to start from the beginning. If you are a returning user, you will be prompted whether you want to start from the beginning or resume from your last session.

## View Page

The view page consists of the tab view and a sidebar.

### Sidebar

The top of the sidebar contains the navigation buttons. The `Previous` button will navigate back one generated domain and the `Next` button will navigate to the next generated domain. If you are at the first run the `Previous` button will be greyed out, and similarily when you are at the last available run the `Next` button will be greyed out. If you have already submitted an evaluation for that particular run, a red notice label will appear below the run counter showing the message `Already Evaluated`.

The `Save` button will save your evaluation results to disk. The `Exit` button will exit the application.

At the bottom of the sidebar you can switch between `Light` and `Dark` mode. Underneath the appearance dropdown there is a scaling dropdown for UI scaling.

### Tab View

#### Compare JSON

The compare JSON tab allows you to inspect the generated domain against a human curated domain for the same paper. If the JSON serialization failed after generating the domain, the raw text file will be displayed with a note at the top saying `Failed JSON serialization. Raw text output:`.

#### Source Nodes

The source node tab will display the nodes that were retrieved during the retrieval process and sent as context with the domain query. Depending on the `similarity_top_k` parameter chosen for the run, the number of reference nodes will be marked with the delimiting lines `----------------- Source Node x/n -----------------`.

#### Parameter Set

The parameter set tab will display the exact parameter set that was used to generate the target domain.

#### Evaluate

The evaluate tab is where reviewers will input there evaluation ratings. 

##### Score Evaluation

The score evaluation window contains evaluation options for the domain score. The `Score` label displays the calculated BCO score based on the BCO score API endpoint. The `Score version` label displays the score version according to the BCO score API endpoint. The segmented button should 

##### Error Evaluation

##### Reference Evaluatio

##### General Evaluation

##### Miscellaneous Evaluation
