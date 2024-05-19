#!/usr/bin/env bash

pytest tests --cov=nutrition_app --cov-fail-under=90 --cov-report=term-missing