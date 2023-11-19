from flask import Flask, request, make_response, jsonify
import simplejson as json

from components.dynamicComponents import DynamicComponents

app = Flask(__name__)

dynamicComponents = DynamicComponents()

