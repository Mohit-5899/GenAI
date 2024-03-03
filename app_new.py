from flask import Flask, jsonify,request
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv
import google.generativeai as genai
from utils.utils import input_pdf_setup,get_gemini_response,api_authetication
from enums.enums import INPUT_PROMPT_1,INPUT_PROMPT_2

load_dotenv()
app = Flask(__name__)
CORS(app)
genai.configure(api_key=getenv("GOOGLE_API_KEY"))

@app.route('/resume_detail', methods=['GET'])
def resume_detail():
    auth = api_authetication(request.form.get('key'))
    if auth:
        file = request.files['resume'].read()
        description = request.form.get('job_description')
        if file is not None:
            pdf_content = input_pdf_setup(file)
            response=get_gemini_response(INPUT_PROMPT_1,pdf_content,description)
            return jsonify({'response':response})
        else:
            return jsonify({'file not received':400}),400
    else:
        return jsonify({'Key not authorized':400}),400

@app.route('/resume_scorer', methods=['GET'])
def resume_scorer():
    auth = api_authetication(request.form.get('key'))
    if auth:
        file = request.files['resume'].read()
        description = request.form.get('job_description')
        if file is not None:
            pdf_content = input_pdf_setup(file)
            response=get_gemini_response(INPUT_PROMPT_2,pdf_content,description)
            return jsonify({'response':response})
        else:
            return jsonify({'file not received':404})
    else:
        return jsonify({'Key not authorized':400}),400


if __name__ == "__main__":
    app.run(host='localhost',port=8000)