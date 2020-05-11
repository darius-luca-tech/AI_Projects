from wtforms import Form, FloatField, validators 

class InputForm(Form):
	a = FloatField(label = 'Grosimea Manunchiului', default = 1, validators = [validators.InputRequired()]) 
	b = FloatField(label = 'Uniformitatea marimii celulei', default = 1, validators = [validators.InputRequired()])
	c = FloatField(label = 'Uniformitatea formei celulei', default = 1, validators = [validators.InputRequired()]) 
	d = FloatField(label = 'Aderenta Marginala', default = 1, validators = [validators.InputRequired()]) 
	e = FloatField(label = 'Dimensiune unica a celulei epiteliale', default = 1, validators = [validators.InputRequired()]) 
	z = FloatField(label = 'Nuclee Goale', default = 1, validators = [validators.InputRequired()]) 
	g = FloatField(label = 'Cromatine', default = 1, validators = [validators.InputRequired()]) 
	h = FloatField(label = 'Nucleoli normali', default = 1, validators = [validators.InputRequired()]) 
	i = FloatField(label = 'Mitoze', default = 1, validators = [validators.InputRequired()])  

