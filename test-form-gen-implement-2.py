import sys
from json import dumps

from PyQt5 import QtWidgets

from pyqtschema.builder import WidgetBuilder

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    schema = {
    #"$schema": "http://json-schema.org/draft-04/schema#",
    #"$id": "vlmd-fields",
    "title": "HEAL Variable Level Metadata Fields",
    "description": "Variable level metadata individual fields integrated into the variable level\nmetadata object within the HEAL platform metadata service.\n",
    "type": "object",
    "required": [
        "name",
        "description"
    ],
    "properties": {
        "schema_path": {
                "title": "Schema path",
                "type": "string"
            },
        "integerRangeSteps": {
                "title": "Integer range (by 10)",
                "type": "integer",
                "minimum": 55,
                "maximum": 100,
                "multipleOf": 10
            },
        "sky_colour": {
                "type": "string"
            },
        "module": {
            "type": "string",
            "title": "Module (i.e., section,form,category)",
            "description": "Module (a place to put the section, form, or other broad category used \nto group variables.\n",
            "examples": [
                "Demographics",
                "PROMIS",
                "Substance use",
                "Medical History",
                "Sleep questions",
                "Physical activity"
            ]
        },
        "name": {
            "type": "string",
            "title": "Variable Name",
            "description": "The name of a variable (i.e., field) as it appears in the data.\n"
        },
        "title": {
            "type": "string",
            "title": "Variable Label (ie Title)",
            "description": "The human-readable title of the variable."
        },
        "description": {
            "type": "string",
            "title": "Variable Description",
            "description": "An extended description of the variable.",
            "examples": [
                "Definition",
                "Question text (if a survey)"
            ]
        },
        "type": {
            "title": "Variable Type",
            "description": "A classification allowing the user (analyst, researcher or computer) to\nknow how to use the variable\n",
            "type": "string",
            "enum": [
                "number",
                "integer",
                "string",
                "any",
                "boolean",
                "date",
                "datetime",
                "time",
                "year",
                "yearmonth",
                "duration",
                "geopoint"
            ]
        },
        "format": {
            "title": "Variable Format",
            "description": "Indicates the format of the type specified in the `type` property. This\nmay describe the type of unit (such as for time fields like year or month)\nor the format of a date field (such as %y%m%d).\n",
            "type": "string",
            "enum": [
                "uri",
                "email",
                "binary",
                "uuid",
                "any",
                "array",
                "object",
                "topojson"
            ]
        },
        "constraints": {
            "type": "object",
            "properties": {
                "maxLength": {
                    "type": "integer",
                    "title": "Maximum Length",
                    "description": "Indicates the maximum length of an iterable (e.g., array, string, or\nobject). For example, if 'Hello World' is the longest value of a\ncategorical variable, this would be a maxLength of 11.\n"
                },
                "enum": {
                    "type": "array",
                    "title": "Variable Possible Values",
                    "description": "Constrains possible values to a set of values."
                },
                "pattern": {
                    "type": "string",
                    "title": "Regular Expression Pattern",
                    "description": "A regular expression pattern the data MUST conform to."
                },
                "maximum": {
                    "type": "integer",
                    "title": "Maximum Value",
                    "description": "Specifies the maximum value of a field (e.g., maximum -- or most\nrecent -- date, maximum integer etc). Note, this is different then\nmaxLength property.\n"
                }
            }
        },
        "encodings": {
            "title": "Variable Value Encodings (i.e., mappings; value labels)",
            "description": "Encodings (and mappings) allow categorical values to be stored as\nnumerical values. IMPORTANT: the ==key should be the value represented IN\nthe data== and the ==value should be the to-be-mapped label==. Many\nanalytic software programs use numerical encodings and some algorithms\nonly support numerical values. Additionally, this field provides a way to\nstore categoricals that are stored as  \"short\" labels (such as\nabbreviations)\n",
            "type": "object",
            "examples": [
                "{0:\"No\",1:\"Yes\"}",
                "{\"HW\":\"Hello world\",\"GBW\":\"Good bye world\",\"HM\":\"Hi, Mike\"}"
            ]
        },
        "ordered": {
            "title": "An ordered variable",
            "description": "Indicates whether a categorical variable is ordered. This variable  is\nrelevant for variables that have an ordered relationship but not\nnecessarily  a numerical relationship (e.g., Strongly disagree < Disagree\n< Neutral < Agree).\n",
            "type": "boolean"
        },
        "missingValues": {
            "title": "Missing Values",
            "description": "A list of missing values specific to a variable.",
            "type": "array"
        },
        "falseValues": {
            "title": "Boolean False Value Labels",
            "description": "For boolean (false) variable (as defined in type field), this field allows\na physical string representation to be cast as false (increasing\nreadability of the field) that is not a standard false value. It can include one or more values.\n",
            "type": "array"
        },
        "repo_link": {
            "type": "string",
            "title": "Variable Repository Link",
            "description": "A link to the variable as it exists on the home repository, if applicable\n"
        },
        "univar_stats": {
            "type": "object",
            "properties": {
                "median": {
                    "type": "number"
                },
                "mean": {
                    "type": "number"
                },
                "std": {
                    "type": "number"
                },
                "min": {
                    "type": "number"
                },
                "max": {
                    "type": "number"
                },
                "mode": {
                    "type": "number"
                },
                "count": {
                    "type": "integer",
                    "minimum": 0
                },
                "twenty_five_percentile": {
                    "type": "number"
                },
                "seventy_five_percentile": {
                    "type": "number"
                }
            }
        }
    }
}

    ui_schema = {
        "schema_path": {
            "ui:widget": "filepath"
        },
        "sky_colour": {
            "ui:widget": "colour"
        }

    }

    builder = WidgetBuilder(schema)
    form = builder.create_form(ui_schema)
    form.widget.state = {
        "schema_path": "some_file.py",
        "integerRangeSteps": 60,
        "sky_colour": "#8f5902"
    }
    form.show()
    form.widget.on_changed.connect(lambda d: print(dumps(d, indent=4)))

    app.exec_()