import sys
from json import dumps

from PyQt5 import QtWidgets

from pyqtschema.builder import WidgetBuilder

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    schema = {
        "type": "object",
        "title": "Number fields and widgets",
        "properties": {
            "experiment.id": {
                "label": "Experiment ID",
                "description": "id assigned to each experiment relevant to the data package; prefix is 'exp-' followed by a number starting with 1 for the first experiment, and iterating by 1 for each successive experiment (i.e. exp-1, exp-2, etc.)",
                "type": "string",
                "pattern": "^exp-+-*[0-9]*[1-9][0-9]*$"
            },
            "experiment.type": {
                "label" : "Experiment Type",
                "description": "discovery|materials and methods development",
                "type": "string",
                "enum": ["discovery","materials and methods development"]
            },
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
            "data_release_status": {
                "description": "If the study will collect/produce data and make at least some of the data available, indicate whether the study has not started, has started, or has finished data release activities",
                "type": "string",
                "label": "Has data release started?",
                "enum": ["not started","started","finished"]
            },
            "data_collection_start_date": {
                "description": "If the study will collect/produce data, indicate the anticipated date when data collection/production will begin",
                "type": "string",
                #"format": "date",
                "label": "Date when first data will be collected/produced (Anticipated)"
            },
            "other_study_websites": {
                "description": "any other websites officially associated with this study that provide additional information about the study",
                "type": "array",
                "label": "Other Study Websites",
                "items": {
                    "type": "string",
                    #"$ref": "#/definitions/saneUrl"
                    #"format": "uri"
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
        "experiment.id": "exp-1",
        "schema_path": "some_file.py",
        "integerRangeSteps": 60,
        "sky_colour": "#8f5902"
    }
    form.show()
    form.widget.on_changed.connect(lambda d: print(dumps(d, indent=4)))

    app.exec_()