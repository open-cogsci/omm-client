"""A plugin for announcing participants"""

category = "OMM Client"
aliases = ['OMMAnnounce']
controls = [
  {
    "label": "Participant",
    "name": "line_edit_participant",
    "type": "line_edit",
    "var": "omm_participant"
  },
  {
    "label": "Server",
    "name": "line_edit_server",
    "type": "line_edit",
    "var": "omm_server"
  },
  {
    "label": "Port",
    "name": "spinbox_port",
    "type": "spinbox",
    "min_val": 1,
    "max_val": 10000,
    "var": "omm_port"
  },
  {
    "label": "API",
    "name": "spinbox_api",
    "type": "spinbox",
    "min_val": 1,
    "max_val": 10000,
    "var": "omm_api"
  },
  {
    "label": "Local log file",
    "name": "line_edit_local_logfile",
    "type": "line_edit",
    "var": "omm_local_logfile"
  },
  {
    "label": "Fallback experiment",
    "info": "In case of connection errors etc.",
    "name": "line_edit_fallback_experiment",
    "type": "line_edit",
    "var": "omm_fallback_experiment"
  },
  {
    "label": "YAML data",
    "name": "yaml_data",
    "type": "editor",
    "syntax": False,
    "var": "omm_yaml_data"
  }
]


def supports(exp):
    return exp.var.canvas_backend != 'osweb'
