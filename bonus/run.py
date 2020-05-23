#!/usr/bin/env python3
##
## EPITECH PROJECT, 2020
## WEB_epytodo_2019
## File description:
## run
##

from app import app

if __name__ == '__main__':
    app.secret_key = '42fz5e51gjf55zeZ#32FA__zef8F,ZEG'
    app.run()