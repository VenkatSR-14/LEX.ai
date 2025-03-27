from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from document_processor import DocumentProcessor
from syllabus_matcher import SyllabusMatcher
from ai_service import AIService


app = Flask(__name__)