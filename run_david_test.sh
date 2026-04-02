#!/bin/bash
cd /code
source venv/bin/activate
python bs_translator.py translate --email-file david_email.json
