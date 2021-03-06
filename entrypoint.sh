#!/bin/sh

gunicorn app:application --bind 0.0.0.0:7000