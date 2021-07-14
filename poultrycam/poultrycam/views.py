from django.shortcuts import render


def contacts(request):
	return render(request, 'poultrycam/contacts.html')
