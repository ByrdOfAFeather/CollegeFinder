from django import forms


class MatcherForm(forms.forms.Form):
	unweighted_gpa = forms.FloatField(max_value = 9.0, widget = forms.TextInput(attrs = {"placeholder": "3.0"}))
	sat_score = forms.IntegerField(max_value = 1600, required = False, widget = forms.TextInput(attrs = {"placeholder": "1010"}))
	act_score = forms.IntegerField(max_value = 36, required = False,widget = forms.TextInput(attrs = {"placeholder": "21"}))

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
