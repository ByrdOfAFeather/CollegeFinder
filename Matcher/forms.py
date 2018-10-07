from django import forms


class MatcherForm(forms.forms.Form):
	unweighted_gpa = forms.FloatField(max_value=9.0, widget=forms.TextInput(attrs={"placeholder": "3.0"}),
	                                  label="Unweighted GPA")

	sat_score = forms.IntegerField(max_value=1600, required=False,
	                               widget=forms.TextInput(attrs={"placeholder": "1010"}),
	                               label="SAT Score")

	act_score = forms.IntegerField(max_value=36, required=False, widget=forms.TextInput(attrs={"placeholder": "21"}),
	                               label="ACT Score")

	intended_major = forms.CharField(max_length=500, label="Intended Major")

	CHOICES = (
		("CMTYSRVCE", "Honor Society (Beta Club / National Honors Society)"),
		("CMTYSRVCE", "Academic Honor Society"),
		("STEM", "Applied STEM Related Clubs"),
		("MUSIC", "Marching Band"),
		("DBAT", "Debate Team"),
		("GOVRN", "Student Government"),
		("THETR", "Theatre"),
		("ATHLETE", "Varsity Athletics"),
		("EDIT", "Newspaper"),
		("RELGI", "Religious Studies")
	)

	extra_circ = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple,
	                                       label="Extra-Circulars", required=False)

	personal_statement = forms.FileField(required=False)

	def clean(self):
		super(MatcherForm, self).clean()
		cleaned = self.cleaned_data
		sat_score = cleaned.get("sat_score")
		act_score = cleaned.get("act_score")

		if not sat_score and not act_score:
			sat_act_error = "Either SAT or ACT has to be filled data"
			self.add_error("sat_score", sat_act_error)
			self.add_error("act_score", sat_act_error)

		return cleaned
