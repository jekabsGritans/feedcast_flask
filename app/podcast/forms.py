from flask_wtf import Form
from wtforms import TextAreaField, StringField, DateTimeField, IntegerField, BooleanField, FileField, SelectField, SelectMultipleField, RadioField
from wtforms.validators import InputRequired

#add separate form elements for release scheduling, etc.
class PodcastEdit(Form):
    title = StringField('Title', [InputRequired('Enter the title.')])
    description = TextAreaField('Description',[InputRequired('Enter the description.')])
    language = SelectField('Language',[InputRequired(message='Choose the language.')])
    image = FileField('Thumbnail')
    explicit = BooleanField('Explicit',[InputRequired(message='Choose whether the podcast contains explicit content.')])
    category = SelectField('Content category', [InputRequired(message='Choose the category.')])
    sub_categories = SelectMultipleField('Subcategories')#load choices based on main cat
    ep_type = RadioField('Episode type', [InputRequired('Choose the episode type.')], choices=[('ep', 'Episodic'), ('serial', 'Serial')])
    allowed_regions = SelectMultipleField('Allowed regions')
    ep_limit = IntegerField('Episode limit')
    origin = SelectField('Origin', [InputRequired('Choose the origin country.')])

    

class EpisodeEdit(Form):
    title = StringField('Title', [InputRequired('Enter the title.')])
    description = TextAreaField('Description', [InputRequired('Enter the description.')])
    audio = FileField('Audio', [InputRequired('Upload the audio file.')])
    image = FileField('Thumbnail')
    allowed_regions = SelectMultipleField('Allowed regions')
    explicit = BooleanField('Explicit',[InputRequired(message='Choose whether the episode contains explicit content.')])
    episode_type = RadioField('Type', [InputRequired('Choose the episode type.')], choices=[('full','Full'),('trailer','Trailer'),('bonus','Bonus')])
    # keywords = # Custom bootstrap tags input field