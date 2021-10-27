#!/bin/bash
source /home/robo/venv/bin/activate
export DB_CONNECTION_STRING="postgresql://filing:filing@34.150.146.117/sec-edgar"
parser_main >>/var/log/filing_parser.log 2>>/var/log/filing_parser.err.log
