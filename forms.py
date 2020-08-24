# forms.py
from wtforms import Form, StringField, SelectField, SelectMultipleField, RadioField
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
from datetime import date, timedelta


# class StarRatingForm(Form):
#     choices = [(1, '1'),
#                (2, '2'),
#                (3, '3'),
#                (4, '4'),
#                (5, '5')]
#     # select = SelectMultipleField('Stars', choices=choices)
#     radio_group = RadioField('Star rating', choices=choices)


# class AmenitiesForm(Form):
#     choices = [('Free parking', 'Free parking'),
#                 ('Pool', 'Pool'),
#                 ('Airport transfer', 'Airport transfer'),
#                 ('Bar', 'Bar'),
#                 ('Pet-friendly', 'Pet-friendly'),
#                 ('Gym', 'Gym'),
#                 ('Kitchen', 'Kitchen'),
#                 ('Air ', 'Air '),
#                 ('Conditioning', 'Conditioning'),
#                 ('Bathtub', 'Bathtub'),
#                 ('Kitchenette', 'Kitchenette'),
#                 ('Parking available', 'Parking available')]
#     # select = SelectMultipleField('Stars', choices=choices)
#     radio_group = RadioField('Amenities', choices=choices)


class SearchForm(Form):
    # Star rating
    star_rating_choices = [(1, '1'),
               (2, '2'),
               (3, '3'),
               (4, '4'),
               (5, '5')]
    star_rating = RadioField('', choices=star_rating_choices, default=3)

    # Amenities
    amenitie_choices = [('Free parking', 'Free parking'),
                ('Pool', 'Pool'),
                ('Airport transfer', 'Airport transfer'),
                ('Bar', 'Bar'),
                ('Pet-friendly', 'Pet-friendly'),
                ('Gym', 'Gym'),
                ('Kitchen', 'Kitchen'),
                ('Air ', 'Air '),
                ('Conditioning', 'Conditioning'),
                ('Bathtub', 'Bathtub'),
                ('Kitchenette', 'Kitchenette'),
                ('Parking available', 'Parking available')]
    amenities = RadioField('Amenities', choices=amenitie_choices)

    # Search field
    search = StringField('', default="Las Vegas")

    # Datepicker field
    checkin_date = DateField('', validators=[DateRange(min=date.today())], 
                             default=date.today()+timedelta(days=80))
    checkout_date = DateField('', validators=[DateRange(min=date.today())])