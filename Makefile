# Makefile for the UMinho Schedule Automation Project
# Author: Miguel Caçador Peixoto

# This will have 6 targets:
# help                 💬 This help message
# install              📦 Install dependencies, download and pre-process data.
# download             📥 Download data from the web.
# test                 🎯 Unit tests
# clean       🧹 Clean up project

# Variables
CURRENT_DIR = $(shell pwd)
SHELL = /bin/bash

# Help message
help:
	@echo "Makefile for the UMinho Schedule Automation Project"
	@echo " "
	@echo "Usage:"
	@echo "    make install        📦 Install dependencies, download and pre-process data."
	@echo "    make download       📥 Download data from the web."
	@echo "    make test           🎯 Unit tests"
	@echo "    make clean          🧹 Clean up project"

install:
	@echo "Creating virtual enviroment..."
	python -m venv .env
	source .env/bin/activate
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "The rest of the installation process is not automated yet."

