from flask import Flask, render_template, request, abort, send_from_directory, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, or_
import random
import os
from utils.nav import get_nav_items
from utils.quiz_db import get_random_questions, get_question_by_id

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'example.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # For flash messages
db = SQLAlchemy(app)

@app.context_processor
def inject_nav():
    try:
        nav_items = get_nav_items()
    except Exception:
        nav_items = []
    return {'nav_items': nav_items}

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# ============ EXISTING MODELS ============
class STUDENT(db.Model):
    ID = db.Column(db.String(255), primary_key=True, nullable=False)
    NAME = db.Column(db.String(25), nullable=False)
    CLASS = db.Column(db.String(25))
    Score = db.Column(db.Integer)

class Thesis(db.Model):
    ID = db.Column(db.String(25), primary_key=True, nullable=False)
    Author = db.Column(db.String(25), nullable=False)
    Category = db.Column(db.String(25), nullable=False)
    Supervisor = db.Column(db.String(25), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    File_name = db.Column(db.String(25), nullable=False)

class question(db.Model):
    ID = db.Column(db.String(255), primary_key=True, nullable=False)
    QName = db.Column(db.String(255), nullable=False)
    CorrectA = db.Column(db.String(25), nullable=False)
    DecoyB = db.Column(db.String(25), nullable=False)
    DecoyC = db.Column(db.String(25), nullable=False)
    DecoyD = db.Column(db.String(25), nullable=False)

# ============ NEW MUSIC INSTRUMENT MODEL ============
class Instrument(db.Model):
    __tablename__ = 'instruments'
    
    ID = db.Column(db.String(50), primary_key=True, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    Vietnamese_Name = db.Column(db.String(255), nullable=False)
    Category = db.Column(db.String(100))  # String, Wind, Percussion, etc.
    Region = db.Column(db.String(100))  # North, Central, South Vietnam
    Description = db.Column(db.Text)
    History = db.Column(db.Text)
    Playing_Technique = db.Column(db.Text)
    
    # Audio and Video
    Audio_File = db.Column(db.String(255))  # Path to audio file
    Video_URL = db.Column(db.String(500))  # YouTube URL
    
    # Images
    Image_Main = db.Column(db.String(255))  # Main instrument image
    Image_Gallery = db.Column(db.Text)  # JSON array of additional images
    
    # Metadata
    Created_At = db.Column(db.DateTime, default=db.func.current_timestamp())
    Updated_At = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# ============ EXISTING ROUTES ============
@app.route('/')
def main_home():
    return render_template('home.html')

@app.route('/learning')
def to_learning():
    return render_template('quiz/learning.html')

@app.route('/thesis')
def to_thesis():
    return render_template('thesis_archive/thesis.html')

@app.route('/vnmap')
def to_vnmap():
    return render_template('vnmap.html')

@app.route('/gallery/')
def to_gallery():
    return render_template('home.html')

@app.route('/gallery/infographic')
def to_infographic():
    return render_template('thesis_archive/thesis_search_result.html')

# ============ MUSIC LIBRARY ROUTES (CRUD) ============

# READ - List all instruments (Library Homepage)
@app.route('/library/')
def to_library():
    # Ensure table exists and is populated
    db.create_all()
    if not db.session.query(Instrument).first():
        instruments_data = [
            {
                'ID': 'dan-bau',
                'Name': 'Monochord',
                'Vietnamese_Name': 'Đàn bầu',
                'Category': 'String Instrument',
                'Region': 'Northern Vietnam',
                'Description': 'The đàn bầu is a Vietnamese monochord (one-string zither) with a unique, ethereal sound.',
                'History': 'Dating back to the 10th century, the đàn bầu has been an integral part of Vietnamese folk music.',
                'Playing_Technique': 'The player plucks the string with one hand while bending the flexible rod with the other hand.',
                'Audio_File': '/static/audio/dan-bau.mp3',
                'Video_URL': 'https://www.youtube.com/watch?v=example1',
                'Image_Main': '/static/images/instruments/dan-bau.jpg',
                'Image_Gallery': '[]'
            },
            {
                'ID': 'dan-tranh',
                'Name': 'Vietnamese Zither',
                'Vietnamese_Name': 'Đàn tranh',
                'Category': 'String Instrument',
                'Region': 'Southern Vietnam',
                'Description': 'The đàn tranh is a 16-string zither that is one of the most popular traditional Vietnamese instruments.',
                'History': 'Introduced to Vietnam from China around the 16th century.',
                'Playing_Technique': 'Players pluck the strings with their right hand while using their left hand to press down on the strings.',
                'Audio_File': '/static/audio/dan-tranh.mp3',
                'Video_URL': 'https://www.youtube.com/watch?v=example2',
                'Image_Main': '/static/images/instruments/dan-tranh.jpg',
                'Image_Gallery': '[]'
            }
        ]
        for data in instruments_data:
            existing = db.session.get(Instrument, data['ID'])
            if not existing:
                instrument = Instrument(**data)
                db.session.add(instrument)
        db.session.commit()
    
    instruments = db.session.query(Instrument).order_by(Instrument.Vietnamese_Name).all()
    return render_template('music_library/library.html', instruments=instruments)

# READ - Search instruments
@app.route('/library/search', methods=['GET', 'POST'])
def search_library():
    if request.method == 'POST':
        search_term = request.form.get('Search', '')
    else:
        search_term = request.args.get('q', '')
    
    search_pattern = f"%{search_term}%"
    results = db.session.execute(
        db.select(Instrument).where(or_(
            Instrument.Name.like(search_pattern),
            Instrument.Vietnamese_Name.like(search_pattern),
            Instrument.Category.like(search_pattern),
            Instrument.Region.like(search_pattern),
            Instrument.Description.like(search_pattern)
        ))
    ).scalars().all()
    
    return render_template('music_library/library_search_result.html', results=results, search_term=search_term)

# READ - View single instrument detail (Dictionary-style)
@app.route('/library/instrument/<instrument_id>')
def view_instrument(instrument_id):
    instrument = db.session.get(Instrument, instrument_id)
    if not instrument:
        abort(404)
    return render_template('music_library/instrument_detail.html', instrument=instrument)

# CREATE - Show form to add new instrument
@app.route('/library/add', methods=['GET'])
def add_instrument_form():
    return render_template('music_library/instrument_form.html', instrument=None, action='add')

# CREATE - Handle form submission
@app.route('/library/add', methods=['POST'])
def add_instrument():
    try:
        new_instrument = Instrument(
            ID=request.form.get('ID'),
            Name=request.form.get('Name'),
            Vietnamese_Name=request.form.get('Vietnamese_Name'),
            Category=request.form.get('Category'),
            Region=request.form.get('Region'),
            Description=request.form.get('Description'),
            History=request.form.get('History'),
            Playing_Technique=request.form.get('Playing_Technique'),
            Audio_File=request.form.get('Audio_File'),
            Video_URL=request.form.get('Video_URL'),
            Image_Main=request.form.get('Image_Main'),
            Image_Gallery=request.form.get('Image_Gallery')
        )
        db.session.add(new_instrument)
        db.session.commit()
        flash('Instrument added successfully!', 'success')
        return redirect(url_for('view_instrument', instrument_id=new_instrument.ID))
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding instrument: {str(e)}', 'error')
        return redirect(url_for('add_instrument_form'))

# UPDATE - Show edit form
@app.route('/library/edit/<instrument_id>', methods=['GET'])
def edit_instrument_form(instrument_id):
    instrument = db.session.get(Instrument, instrument_id)
    if not instrument:
        abort(404)
    return render_template('music_library/instrument_form.html', instrument=instrument, action='edit')

# UPDATE - Handle form submission
@app.route('/library/edit/<instrument_id>', methods=['POST'])
def edit_instrument(instrument_id):
    instrument = db.session.get(Instrument, instrument_id)
    if not instrument:
        abort(404)
    
    try:
        instrument.Name = request.form.get('Name')
        instrument.Vietnamese_Name = request.form.get('Vietnamese_Name')
        instrument.Category = request.form.get('Category')
        instrument.Region = request.form.get('Region')
        instrument.Description = request.form.get('Description')
        instrument.History = request.form.get('History')
        instrument.Playing_Technique = request.form.get('Playing_Technique')
        instrument.Audio_File = request.form.get('Audio_File')
        instrument.Video_URL = request.form.get('Video_URL')
        instrument.Image_Main = request.form.get('Image_Main')
        instrument.Image_Gallery = request.form.get('Image_Gallery')
        
        db.session.commit()
        flash('Instrument updated successfully!', 'success')
        return redirect(url_for('view_instrument', instrument_id=instrument_id))
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating instrument: {str(e)}', 'error')
        return redirect(url_for('edit_instrument_form', instrument_id=instrument_id))

# DELETE - Delete instrument
@app.route('/library/delete/<instrument_id>', methods=['POST'])
def delete_instrument(instrument_id):
    instrument = db.session.get(Instrument, instrument_id)
    if not instrument:
        abort(404)
    
    try:
        db.session.delete(instrument)
        db.session.commit()
        flash('Instrument deleted successfully!', 'success')
        return redirect(url_for('to_library'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting instrument: {str(e)}', 'error')
        return redirect(url_for('view_instrument', instrument_id=instrument_id))

# API endpoint to serve audio files
@app.route('/library/audio/<filename>')
def serve_audio(filename):
    audio_dir = os.path.join(app.root_path, 'static', 'audio')
    return send_from_directory(audio_dir, filename)

# ============ EXISTING ROUTES CONTINUED ============
@app.route('/music_library/library')
def to_music_library_alias():
    return redirect(url_for('to_library'))

@app.route('/music_world/')
def to_musicworld():
    return render_template('music_world.html')

@app.route('/music_world/3dpreview/')
def to_3dpreview():
    return render_template('3d_model_viewer/3dpreview.html')

@app.route('/music_world/3dpreview/<string:inname>')
def render_3d(inname):
    filename = inname + ".glb"
    return render_template('3d_model_viewer/3d_view.html', modelname=filename)

@app.route('/testdb')
def test_db():
    profiles = db.session.query(STUDENT).all()
    return render_template('quiz/testdb.html', profiles=profiles)

@app.route('/thesis/search')
def search_thesis():
    q = request.args.get("q", "")
    search_pattern = f"%{q}%"
    result = db.session.execute(db.select(Thesis).where(or_(
        Thesis.Name.like(search_pattern),
        Thesis.ID.like(search_pattern),
        Thesis.Author.like(search_pattern),
        Thesis.Supervisor.like(search_pattern),
        Thesis.Category.like(search_pattern)
    ))).scalars()
    return render_template('thesis_archive/thesis_search_result.html', result=result)

@app.route('/thesis/<thesisname>')
def serve_thesis_pdf(thesisname):
    filename = f"{os.path.basename(thesisname)}.pdf"
    directory = os.path.join(app.root_path, 'templates')
    return send_from_directory(directory, filename, as_attachment=False)

@app.route('/quiz/')
def to_quiz():
    return render_template('quiz/quiz.html')

@app.route('/quiz/question')
def to_quest():
    data = get_random_questions(db, limit=3)
    return render_template('quiz/question.html', questions=data)

def fetch_all_relevant_questions(form_keys):
    question_ids = list(form_keys)
    questions_db = db.session.execute(db.select(question).where(question.ID.in_(question_ids))).scalars().all()
    return {q.ID: q for q in questions_db}

def compare_user_answer(user_answer, correct_answer):
    return user_answer == correct_answer

def save_details_for_result_page(actual_question, user_answer, is_correct):
    return {
        'question': actual_question.QName,
        'your_answer': user_answer,
        'correct_answer': actual_question.CorrectA,
        'is_correct': is_correct
    }

@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    score = 0
    total_questions = 0
    results_summary = []
    
    question_map = fetch_all_relevant_questions(request.form.keys())

    for q_id, user_answer in request.form.items():
        actual_question = question_map.get(q_id)

        if actual_question:
            total_questions += 1
            is_correct = compare_user_answer(user_answer, actual_question.CorrectA)
            if is_correct:
                score += 1
            
            results_summary.append(save_details_for_result_page(actual_question, user_answer, is_correct))

    return render_template('quiz/quiz_result.html', 
                           score=score, 
                           total=total_questions, 
                           summary=results_summary)

@app.route('/<path:subpath>')
def spa_catch_all(subpath: str):
    return render_template('home.html')

# Alias routes
@app.route('/thesis_archive/thesis')
def thesis_archive_alias():
    return render_template('thesis_archive/thesis.html')

@app.route('/quiz/learning')
def quiz_learning_alias():
    return render_template('quiz/learning.html')

@app.route('/quiz/quest')
def quiz_quest_alias():
    return render_template('quiz/quest.html')

@app.route('/quiz/quiz')
def quiz_quiz_alias():
    return render_template('quiz/quiz.html')

@app.route('/quiz/testdb')
def quiz_testdb_alias():
    return render_template('quiz/testdb.html')

@app.route('/3d_model_viewer/3dpreview')
def modelviewer_preview_alias():
    return render_template('3d_model_viewer/3dpreview.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.Model.metadata.reflect(db.engine)
        print("Reflected tables:", db.Model.metadata.tables.keys())
        print("Database file URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(host='0.0.0.0', port=3000, debug=True)
