from simulation.models.agents.RA.RAAgent import RequirementAnalysisAgent
from simulation.models.agents.RA.RAObserver import RequirementAnalysisObserver
from simulation.models.agents.ED.VCAgent import VariableControlAgent
import logging
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from typing import Literal

app = Flask(__name__)
CORS(app)

MODEL_LIST = ['deepseek-r1:32b', 'deepseek-r1:32b-qwen-distill-q8_0', 'gpt-4o']