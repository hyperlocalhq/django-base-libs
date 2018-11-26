#!/usr/bin/env bash

yapf --verbose --in-place --parallel --style facebook --recursive ../../../ruhrbuehnen/ --exclude **/migrations/*
