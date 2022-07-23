from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileRequired
from wtforms import TextAreaField, StringField, DateTimeField, IntegerField, BooleanField, SelectField, SelectMultipleField, RadioField, SubmitField, FileField
from wtforms.validators import InputRequired


with open('app/static/regions.csv','r') as f:
    rows = f.read().split('\n')
    region_choices = []
    for row in rows:
        name, code = row.split(',')
        region_choices.append((code,name))

with open('app/static/languages.csv','r') as f:
    rows = f.read().split('\n')
    language_choices = []
    for row in rows:
        code, name = row.split(',')
        language_choices.append((code,name))

with open('app/static/categories.txt','r') as f:
    cats = f.read().split('\n')
    category_choices = [(cat,cat) for cat in cats]


#add separate form elements for release scheduling, etc.
class PodcastEdit(FlaskForm):
    title = StringField('Title', [InputRequired('Enter the title.')])
    description = TextAreaField('Description',[InputRequired('Enter the description.')])
    language = SelectField('Language',[InputRequired(message='Choose the language.')], choices=language_choices, validate_choice=False)
    image = FileField('New Thumbnail')
    explicit = BooleanField('Explicit')
    category = SelectField('Content category', [InputRequired(message='Choose the category.')], choices=category_choices, validate_choice=False)
    ep_type = SelectField('Episode type', [InputRequired('Choose the episode type.')], choices=[('episodic', 'Episodic'), ('serial', 'Serial')], validate_choice=False)
    allowed_regions = SelectMultipleField('Allowed regions', choices=region_choices)
    ep_limit = IntegerField('Episode limit')
    origin = SelectField('Origin', [InputRequired('Choose the origin country.')], choices=region_choices)
    submit = SubmitField('Update')
    

class EpisodeEdit(FlaskForm):
    title = StringField('Title', [InputRequired('Enter the title.')])
    description = TextAreaField('Description', [InputRequired('Enter the description.')])
    audio = FileField('New Audio')
    image = FileField('New Thumbnail')
    allowed_regions = SelectMultipleField('Allowed regions', choices=region_choices)
    explicit = BooleanField('Explicit')
    episode_type = SelectField('Type', [InputRequired('Choose the episode type.')], choices=[('full','Full'),('trailer','Trailer'),('bonus','Bonus')])
    submit = SubmitField('Update')