Python 3.9

# alohadbf module

Goal: read data from 'NCR Aloha POS' dbf-files, filter and prepare to using in external systems (for example in 'UCS Storehouse')

Structure:

1. \aloha_db - 'Aloha' database sample;
2. \aloha_shifts - 'Aloha' shifts sample;
3. \pdf\aloha_DBF.pdf - aloha dbf-files (tables) description;
4. dbf_res.py - module functionality.

# Instruction

1. from dbf_res import AlohaPOSDbf
2. DBF = AlohaPOSDbf
3. Use this object in your project (as example, see AlohaSH4 or AlohaSH5 projects here)
