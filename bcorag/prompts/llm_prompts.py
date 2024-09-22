LLM_PROMPT = """Can you give me a BioCompute Object (BCO) {} domain using the provided information from a bioinformatics workflow documentation. The return response must be valid JSON and must validate against the JSON schema I am providing you. If the information for a field is not provided, leave it blank, do not make up any information. Do not repeat the JSON schema in your response, just make sure your response conforms against the schema. Please check your work before finalizing your response. The style of writing for the free text response fields should be similar to the style of a scientific paper, it should be written in past tense and not use any first person references. {}"""

USABILITY_DOMAIN_LLM = """The usability domain is a high level, plain langauge description of the purpose and overall goal of the project workflow. It is analogous to an abstract. Keep the information high level and representative of the provided project paper and documentation excerpts.

The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/ieee/ieee-2791-schema/usability_domain.json",
    "type": "array",
    "title": "Usability Domain",
    "description": "Author-defined usability domain of the IEEE-2791 Object. This field is to aid in search-ability and provide a specific description of the function of the object.",
    "items": {
        "type": "string",
        "description": "Free text values that can be used to provide scientific reasoning and purpose for the experiment",
        "examples": [
            "Identify baseline single nucleotide polymorphisms SNPs [SO:0000694], insertions [so:SO:0000667], and deletions [so:SO:0000045] that correlate with reduced ledipasvir [pubchem.compound:67505836] antiviral drug efficacy in Hepatitis C virus subtype 1 [taxonomy:31646]",
            "Identify treatment emergent amino acid substitutions [so:SO:0000048] that correlate with antiviral drug treatment failure",
            "Determine whether the treatment emergent amino acid substitutions [so:SO:0000048] identified correlate with treatment failure involving other drugs against the same virus"
        ]
    }
}
"""

IO_DOMAIN_LLM = """The input output (io) domain is represents the list of global input and output files created by the computational workflow of the project. The input subdomain lists the project's input files and corresponding metadata. The output subdomain lists the project's corresponding output files and metadata. Essentially, if someone were to re-create the project workflow, they would check this domain in order to see what the expected global input files are and their corresponding output files (this is not including intermediate steps of the project).

The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/ieee/ieee-2791-schema/io_domain.json",
    "type": "object",
    "title": "Input and Output Domain",
    "description": "The list of global input and output files created by the computational workflow, excluding the intermediate files. Custom to every specific IEEE-2791 Object implementation, these fields are pointers to objects that can reside in the system performing the computation or any other accessible system.",
    "required": [
        "input_subdomain",
        "output_subdomain"
    ],
    "properties": {
        "input_subdomain": {
            "type": "array",
            "title": "input_domain",
            "description": "A record of the references and input files for the entire pipeline. Each type of input file is listed under a key for that type.",
            "items": {
                "additionalProperties": false,
                "type": "object",
                "required": [
                    "uri"
                ],
                "properties": {
                    "uri": {
                        "$ref": "2791object.json#/definitions/uri"
                    }
                }
            }
        },
        "output_subdomain": {
            "type": "array",
            "title": "output_subdomain",
            "description": "A record of the outputs for the entire pipeline.",
            "items": {
                "type": "object",
                "title": "The Items Schema",
                "required": [
                    "mediatype",
                    "uri"
                ],
                "properties": {
                    "mediatype": {
                        "type": "string",
                        "title": "mediatype",
                        "description": "https://www.iana.org/assignments/media-types/",
                        "default": "application/octet-stream",
                        "examples": [
                            "text/csv"
                        ],
                        "pattern": "^(.*)$"
                    },
                    "uri": {
                        "$ref": "2791object.json#/definitions/uri"
                    }
                }
            }
        }
    }
}
"""

DESCRIPTION_DOMAIN_LLM = """The description domain describes the project workflow. It has a section that describes keywords, similar to a publication. It also has an external references section that describes other resources that are referenced in the workflow. The description domain also has a platform section that describes what or which platforms the workflow was run on. Finally, the pipeline steps describes the details of each specific step in executing the workflow. The pipeline steps are very important. If someone wanted to recreate the project workflow, they would view this section to see what steps to take and in what order. The pipeline steps can include various metadata such as prerequisites (or dependencies), name, description, and input and output files relating to the particular step.

The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/ieee/ieee-2791-schema/description_domain.json",
    "type": "object",
    "title": "Description Domain",
    "description": "Structured field for description of external references, the pipeline steps, and the relationship of I/O objects.",
    "required": [
        "keywords",
        "pipeline_steps"
    ],
    "properties": {
        "keywords": {
            "type": "array",
            "description": "Keywords to aid in search-ability and description of the object.",
            "items": {
                "type": "string",
                "description": "This field should take free text value using common biological research terminology.",
                "examples": [
                    "HCV1a",
                    "Ledipasvir",
                    "antiviral resistance",
                    "SNP",
                    "amino acid substitutions"
                ]
            }
        },
        "xref": {
            "type": "array",
            "description": "List of the databases or ontology IDs that are cross-referenced in the IEEE-2791 Object.",
            "items": {
                "type": "object",
                "description": "External references are stored in the form of prefixed identifiers (CURIEs). These CURIEs map directly to the URIs maintained by Identifiers.org.",
                "reference": "https://identifiers.org/",
                "required": [
                    "namespace",
                    "name",
                    "ids",
                    "access_time"
                ],
                "properties": {
                    "namespace": {
                        "type": "string",
                        "description": "External resource vendor prefix",
                        "examples": [
                            "pubchem.compound"
                        ]
                    },
                    "name": {
                        "type": "string",
                        "description": "Name of external reference",
                        "examples": [
                            "PubChem-compound"
                        ]
                    },
                    "ids": {
                        "type": "array",
                        "description": "List of reference identifiers",
                        "items": {
                            "type": "string",
                            "description": "Reference identifier",
                            "examples": [
                                "67505836"
                            ]
                        }
                    },
                    "access_time": {
                        "type": "string",
                        "description": "Date and time the external reference was accessed",
                        "format": "date-time"
                    }
                }
            }
        },
        "platform": {
            "type": "array",
            "description": "reference to a particular deployment of an existing platform where this IEEE-2791 Object can be reproduced.",
            "items": {
                "type": "string",
                "examples": [
                    "hive"
                ]
            }
        },
        "pipeline_steps": {
            "type": "array",
            "description": "Each individual tool (or a well defined and reusable script) is represented as a step. Parallel processes are given the same step number.",
            "items": {
                "additionalProperties": false,
                "type": "object",
                "required": [
                    "step_number",
                    "name",
                    "description",
                    "input_list",
                    "output_list"
                ],
                "properties": {
                    "step_number": {
                        "type": "integer",
                        "description": "Non-negative integer value representing the position of the tool in a one-dimensional representation of the pipeline."
                    },
                    "name": {
                        "type": "string",
                        "description": "This is a recognized name of the software tool",
                        "examples": [
                            "HIVE-hexagon"
                        ]
                    },
                    "description": {
                        "type": "string",
                        "description": "Specific purpose of the tool.",
                        "examples": [
                            "Alignment of reads to a set of references"
                        ]
                    },
                    "version": {
                        "type": "string",
                        "description": "Version assigned to the instance of the tool used corresponding to the upstream release.",
                        "examples": [
                            "1.3"
                        ]
                    },
                    "prerequisite": {
                        "type": "array",
                        "description": "Reference or required prereqs",
                        "items": {
                            "type": "object",
                            "description": "Text value to indicate a package or prerequisite for running the tool used.",
                            "required": [
                                "name",
                                "uri"
                            ],
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Public searchable name for reference or prereq.",
                                    "examples": [
                                        "Hepatitis C virus genotype 1"
                                    ]
                                },
                                "uri": {
                                    "$ref": "2791object.json#/definitions/uri"
                                }
                            }
                        }
                    },
                    "input_list": {
                        "type": "array",
                        "description": "URIs (expressed as a URN or URL) of the input files for each tool.",
                        "items": {
                            "$ref": "2791object.json#/definitions/uri"
                        }
                    },
                    "output_list": {
                        "type": "array",
                        "description": "URIs (expressed as a URN or URL) of the output files for each tool.",
                        "items": {
                            "$ref": "2791object.json#/definitions/uri"
                        }
                    }
                }
            }
        }
    }
}
"""

EXECUTION_DOMAIN_LLM = """The execution domain describes the global execution metadata for the project workflow. This includes things like how the scripts in the project are run, the environment variables set, software prerequisites and dependencies, and any external data endpoints needed to recreate the execution environment.

The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/ieee/ieee-2791-schema/execution_domain.json",
    "type": "object",
    "title": "Execution Domain",
    "description": "The fields required for execution of the IEEE-2791 Object are herein encapsulated together in order to clearly separate information needed for deployment, software configuration, and running applications in a dependent environment",
    "required": [
        "script",
        "script_driver",
        "software_prerequisites",
        "external_data_endpoints",
        "environment_variables"
    ],
    "additionalProperties": false,
    "properties": {
        "script": {
            "type": "array",
            "description": "points to a script object or objects that was used to perform computations for this IEEE-2791 Object instance.",
            "items": {
                "additionalProperties": false,
                "properties": {
                    "uri": {
                        "$ref": "2791object.json#/definitions/uri"
                    }
                }
			}
        },
        "script_driver": {
            "type": "string",
            "description": "Indication of the kind of executable that can be launched in order to perform a sequence of commands described in the script in order to run the pipelin",
            "examples": [
                "hive",
                "cwl-runner",
                "shell"
            ]
        },
        "software_prerequisites": {
            "type": "array",
            "description": "Minimal necessary prerequisites, library, tool versions needed to successfully run the script to produce this IEEE-2791 Object.",
            "items": {
                "type": "object",
                "description": "A necessary prerequisite, library, or tool version.",
                "required": [
                    "name",
                    "version",
                    "uri"
                ],
                "additionalProperties": false,
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Names of software prerequisites",
                        "examples": [
                            "HIVE-hexagon"
                        ]
                    },
                    "version": {
                        "type": "string",
                        "description": "Versions of the software prerequisites",
                        "examples": [
                            "babajanian.1"
                        ]
                    },
                    "uri": {
                        "$ref": "2791object.json#/definitions/uri"
                    }
                }
            }
        },
        "external_data_endpoints": {
            "type": "array",
            "description": "Minimal necessary domain-specific external data source access in order to successfully run the script to produce this IEEE-2791 Object.",
            "items": {
                "type": "object",
                "description": "Requirement for network protocol endpoints used by a pipeline’s scripts, or other software.",
                "required": [
                    "name",
                    "url"
                ],
                "additionalProperties": false,
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Description of the service that is accessed",
                        "examples": [
                            "HIVE",
                            "access to e-utils"
                        ]
                    },
                    "url": {
                        "type": "string",
                        "description": "The endpoint to be accessed.",
                        "examples": [
                            "https://hive.biochemistry.gwu.edu/dna.cgi?cmd=login"
                        ]
                    }
                }
            }
        },
        "environment_variables": {
            "type": "object",
            "description": "Environmental parameters that are useful to configure the execution environment on the target platform.",
            "additionalProperties": false,
            "patternProperties": {
                "^[a-zA-Z_]+[a-zA-Z0-9_]*$": {
                    "type": "string"
                }
            }
        }
    }
}
"""

PARAMETRIC_DOMAIN_LLM = """The parametric domain contains all of the parameters and arguments that were set for each pipeline step. A particular set of parameters should be connected to a specific pipeline step from the description domain. This domain is optional is optional and if the content is not provided you can return an empty JSON response.

The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/ieee/ieee-2791-schema/parametric_domain.json",
    "type": "array",
    "title": "Parametric Domain",
    "description": "This represents the list of NON-default parameters customizing the computational flow which can affect the output of the calculations. These fields can be custom to each kind of analysis and are tied to a particular pipeline implementation",
    "items":{
        "required": [
            "param",
            "value",
            "step"
        ],
        "additionalProperties": false,
        "properties": {
            "param": {
                "type": "string",
                "title": "param",
                "description": "Specific variables for the computational workflow",
                "examples": [
                    "seed"
                ]
            },
            "value": {
                "type": "string",
                "description": "Specific (non-default) parameter values for the computational workflow",
                "title": "value",
                "examples": [
                    "14"
                ]
            },
            "step": {
                "type": "string",
                "title": "step",
                "description": "Refers to the specific step of the workflow relevant to the parameters specified in 'param' and 'value'",
                "examples": [
                    "1"
                ],
                "pattern": "^(.*)$"
            }
        }
    }
}
"""

ERROR_DOMAIN_LLM = """The error domain specifies ranges of input returns and outputs that are not within the tolerance level of the project output expectations. The errors are split into two categories. The first category is empirical errors. Empirical errors describe empirically determined values such as limits of detectability, false positives, false negatives, statistical confidence of outcomes, etc. The second category is algorithmic errors. Algorithmic errors are descriptive of errors that originate by fuzziness of the algorithms, driven by stochastic processes, in dynamically parallelized multi-threaded executions, or in machine learning methodologies where the state of the machine can affect the outcome. This domain is optional is optional and if the content is not provided you can return an empty JSON response.

The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/2791/error_domain.json",
    "type": "object",
    "title": "Error Domain",
    "description": "Fields in the Error Domain are open-ended and not restricted nor defined by the IEEE-2791 standard. It is RECOMMENDED that the keys directly under empirical_error and algorithmic_error use a full URI. Resolving the URI SHOULD give a JSON Schema or textual definition of the field. Other keys are not allowed error_domain",
    "additionalProperties": false,
    "required": [
        "empirical_error",
        "algorithmic_error"
    ],
    "properties": {
        "empirical_error": {
            "type": "object",
            "title": "Empirical Error",
            "description": "empirically determined values such as limits of detectability, false positives, false negatives, statistical confidence of outcomes, etc. This can be measured by running the algorithm on multiple data samples of the usability domain or through the use of carefully designed in-silico data."
        },
        "algorithmic_error": {
            "type": "object",
            "title": "Algorithmic Error",
            "description": "descriptive of errors that originate by fuzziness of the algorithms, driven by stochastic processes, in dynamically parallelized multi-threaded executions, or in machine learning methodologies where the state of the machine can affect the outcome."
        }
    }
}
"""

_TOP_LEVEL_SCHEMA = """
{
  "uri": {
    "type": "object",
    "description": "Any of the four Resource Identifers defined at https://tools.ietf.org/html/draft-handrews-json-schema-validation-01#section-7.3.5",
    "additionalProperties": false,
    "required": [
      "uri"
    ],
    "properties": {
      "filename": {
        "type": "string"
      },
      "uri": {
        "type": "string",
        "format": "uri"
      },
      "access_time": {
        "type": "string",
        "description": "Time stamp of when the request for this data was submitted",
        "format": "date-time"
      },
      "sha1_checksum": {
        "type": "string",
        "description": "output of hash function that produces a message digest",
        "pattern": "[A-Za-z0-9]+"
      }
    }
  }
}
"""

SUPPLEMENT_PROMPT = f"The `uri` object is described in the top level 2791object JSON schema. Here is the definition to reference for those fields: {_TOP_LEVEL_SCHEMA}"
