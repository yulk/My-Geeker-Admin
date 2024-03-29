from flask import Flask

from .cmd_init_table import register_script_init_table

from .cmd_sql import register_script_sql


def register_cmdlines(app: Flask):
    register_script_init_table(app)
    register_script_sql(app)
