import os
import json
import threading
from flask import Blueprint, request, jsonify, current_app, g
from werkzeug.utils import secure_filename
from model import db, Document
from utils import allowed_file, login_required
from rag import extract_text_from_file, segment_text, generate_explanation

bp = Blueprint('documents', __name__)

@bp.route('/test', methods=['GET'])
def test_endpoint():
    print("Test endpoint was called!")
    import sys; sys.stdout.flush()
    return "Test endpoint reached", 200

def process_document(document_id, app):
    """Run the RAG pipeline asynchronously and update the Document record."""
    with app.app_context():
        current_app.logger.info(f"Processing document ID: {document_id}")
        doc = Document.query.get(document_id)
        if not doc:
            current_app.logger.error("Document not found for processing.")
            return

        # Step 1: Extract text from file.
        try:
            extracted_text = extract_text_from_file(doc.file_path)
            current_app.logger.info("Text extracted successfully.")
        except Exception as e:
            current_app.logger.error(f"Error extracting text: {e}")
            extracted_text = ""

        # Step 2: Segment text into chapters.
        chapters = segment_text(extracted_text)
        current_app.logger.info(f"Text segmented into chapters: {list(chapters.keys())}")

        # Step 3: Generate explanations for each chapter.
        detailed_explanations = {}
        for chapter_title, content in chapters.items():
            explanation = generate_explanation(chapter_title, content)
            detailed_explanations[chapter_title] = explanation
        current_app.logger.info("Explanations generated for chapters.")

        # Step 4: Read the file in binary mode and update file_blob.
        try:
            with open(doc.file_path, "rb") as f:
                doc.file_blob = f.read()
            current_app.logger.info("File blob updated successfully.")
        except Exception as e:
            current_app.logger.error(f"Error reading file as binary: {e}")

        # Step 5: Save the generated explanations (as JSON) into file_contents_generated.
        doc.file_contents_generated = json.dumps(detailed_explanations)
        current_app.logger.info("Generated contents updated.")

        # Step 6: Commit changes.
        try:
            db.session.commit()
            current_app.logger.info(f"Document {document_id} processed and committed.")
        except Exception as e:
            current_app.logger.error(f"Error committing processed document: {e}")
            db.session.rollback()

@bp.route('/upload', methods=['POST'])
@login_required
def upload_document():
    print("upload_document endpoint called")
    import sys; sys.stdout.flush()
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        document = Document(filename=filename, file_path=file_path, user_id=g.user_id)
        db.session.add(document)
        db.session.commit()
        current_app.logger.info(f"Document {document.id} uploaded successfully.")

        # Get the actual Flask app object and pass it to the thread.
        app_obj = current_app._get_current_object()
        threading.Thread(target=process_document, args=(document.id, app_obj)).start()

        return jsonify({'message': 'File uploaded successfully', 'filename': filename})
    return jsonify({'error': 'Invalid file type'}), 400

@bp.route('/documents', methods=['GET'])
@login_required
def list_documents():
    docs = Document.query.filter_by(user_id=g.user_id).all()
    document_list = []
    for d in docs:
        document_list.append({
            'id': d.id,
            'filename': d.filename,
            'file_path': d.file_path,
            # For binary data, we encode in base64 (if desired)
            'file_blob': d.file_blob.decode('utf-8', errors='replace') if d.file_blob else None,
            'file_contents_generated': d.file_contents_generated
        })
    return jsonify(document_list)
