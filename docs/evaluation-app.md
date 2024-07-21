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

The source node tab will display the nodes that were retrieved during the retrieval process and sent as context with the domain query. Depending on the `similarity_top_k` parameter chosen for the run, the number of reference nodes will be marked with delimiting lines in the format of: 

```bash
----------------- Source Node x/n -----------------
```

#### Parameter Set

The parameter set tab will display the exact parameter set that was used to generate the target domain.

#### Evaluate

The evaluate tab is where reviewers will input there evaluation ratings. All evaluation sections have corresponding `Notes` sections that allow for free text notes regarding that evaluation category. All numeric segmented buttons have a range from `0` to `2` (with `0` being the worst, `1` being satisfactory, and 2 being the best score). The default score of `-1` is just a placeholder value used to filter out potentially un-finished or erroneously pre-maturly submitted evaluations. 

The bottom right `Submit` button will save the evaluation to the session in memory. If you click on the `Next` or `Previous` buttons before submitting the evaluation it will be lost.

##### Score Evaluation

The score evaluation frame contains evaluation options for the BCO domain score. The `Score` label displays the calculated BCO score returned from the BCO score API endpoint (on API error a default value of -1.0 is shown). The `Score version` label displays the score version according to the BCO score API endpoint (on API error a default value of 0.0 is shown). Depending on the quality of the generated domain, the evaluator should mark whether the score should actually be higher, lower, or if it is about right using the segmented button. 

##### Error Evaluation

The error evaluation frame allows the user to indicate any errors in the generated domain. The types of errors are: 

- **Inferred Knowledge Errors**: Fields that require **inferred knowledge** can result in undefined behavior. For example, multiple domains make use of the *uri* object that is defined in the top level [BCO JSON schema](https://opensource.ieee.org/jgay/ieee-2791-schema-soiland-reyes/-/blob/8dd78d25f85117e7bee47b17a9866c179bb591e3/biocomputeobject.json#L26). The *uri* object has a field for *access_time*, which expects a fully JSON compliant `date-time`. An exact timestamp is very likely to not be explicitly listed in the source material. In early testing, the tool seems to use a default value of *2023-11-01T12:00:00Z* for these fields.
- **External Knowledge Error**: External knowledge errors result in non-specific information when the field requires knowledge from **external dependencies**. A common scenario is for the authors of the paper to include links to the Github repository that contains the source code and corresponding input/output files. In the Description domain, each pipeline step includes a target field for output files generated by the particular step. Since the specific location of the scripts and output files are usually not explicitly described in the paper, the tool will fill the output file field with a generated link to the repository, not the specific location of the file within the repository. For example, a link to the repository such as https://github.com/biocompute-objects/bco-rag/tree/main, versus a link to the specific file within the repository such as https://github.com/biocompute-objects/bco-rag/blob/main/docs/evaluation_app.md. 
- **JSON Formatting Error**: JSON formatting errors occur when the generated domain either 1) is not valid JSON or 2) when the generated domain does not validate against the BCO JSON schema.
- **Other Error**: Other errors can be any other errors not caught by the previous three categories.

##### Reference Evaluation

The reference evaluation frame allows for the user to rate the reference nodes. The reference nodes are arguably the most important part of the domain generation process as they provide the LLM with the context required to complete the domain request. Ideally, all reference nodes should be relevant to the domain purpose and should logically make sense. For example, the Usability domain "is a plain language description of what was done in the workflow". Most often, much of that information would be present in the paper abstract, and not in the paper citations section.

##### General Evaluation

The general evaluation frame allows for the user to rate the generated domain directly. Ideally, generated domains should be relevant to the domain purpose, human readable, and comprehensible by someone with less knowledge of the source material.

##### Miscellaneous Evaluation

The miscellaneous evaluation frame allows for the user to include some metadata for the evaluation not relating directly to the generated domain. In evaluation of scoring data, it should be noted how confident and familiar with the source material the evaluator was. In doing so, isolating high quality reviews will be clearer. The user can also evaluate the quality of the human curated domain.
