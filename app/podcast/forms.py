from flask_wtf import Form
from wtforms import TextAreaField, StringField, DateTimeField, IntegerField, BooleanField, FileField, SelectField, SelectMultipleField, RadioField
from wtforms.validators import Required

#add separate form elements for release scheduling, etc.
class PodcastEdit(Form):
    title = StringField('Title', [Required()])
    description = TextAreaField('Description',[Required()])
    language = SelectField('Language',[Required()])
    image = FileField('Thumbnail')
    explicit = BooleanField('Explicit',[Required()])
    category = SelectField('Content category', [Required()])
    sub_categories = SelectMultipleField('Subcategories')#load choices based on main cat
    ep_type = RadioField('Episode type', [Required()], choices=[('ep', 'Episodic'), ('serial', 'Serial')])
    allowed_regions = SelectMultipleField('Allowed regions')
    ep_limit = IntegerField('Episode limit')
    origin = SelectField('Origin', [Required()])

    

class EpisodeEdit(Form):
    title = StringField('Title', [Required()])
    description = TextAreaField('Description', [Required()])
    audio = FileField('Audio', [Required()])
    image = FileField('Thumbnail', [Required()])
    allowed_regions = SelectMultipleField('Allowed regions')
    explicit = BooleanField('Explicit',[Required()])
    episode_type = RadioField('Type', [Required()], choices=[('full','Full'),('trailer','Trailer'),('bonus','Bonus')])
    # keywords = # Custom bootstrap tags input field