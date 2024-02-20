default:
    @just --list

run CMD *ARGS:
    python3 main.py {{CMD}} {{ARGS}}
    