from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
# Create your views here.
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Question, Choice
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#template = loader.get_template('polls/index.html')
	#context = RequestContext(request, {
	#			'latest_question_list': latest_question_list,
	#		})
	#output = ',<br> '.join(["%s:%s" %(p.question_text,p.pub_date.year)  for p in latest_question_list])
	#return HttpResponse(template.render(context))
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html', context)


def results(request, question_id):
#	response = "your looking at the results of question %s"
#	return HttpResponse(response % question_id)
	question = get_object_or_404(Question,pk=question_id)
	return render(request,'polls/results.html',{'question':question})


def details(request, question_id):
	#response = "details about question %s"
#	question_obj = Question.objects.get(id=question_id)
	#output = ', '.join([p.choice_text for p in Choice.objects.filter(question__id=question_id)])
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/details.html',{'question':question})
#	return HttpResponse(output)

def vote(request, question_id):
	#response = "votes for question %s"
	#return HttpResponse(response % question_id)

	p = get_object_or_404(Question,pk=question_id)
	# receive data from post. choice=id
	# if we could not get the data, than load the details template again
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/details.html',{'question':p,'error_msg':"you didn't provide a choice"})
	else:
		selected_choice.votes+=1
		#commiting the data
		selected_choice.save()
		#best practice is to redirect after POST
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
