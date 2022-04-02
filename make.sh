#! /bin/bash
gunicorn -c gunicorn.py main:app
