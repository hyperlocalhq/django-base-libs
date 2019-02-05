#!/usr/bin/env bash

yapf --verbose --in-place --parallel --style facebook --recursive . --exclude **/migrations/* --exclude **/south_migrations/*
