from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from polls.models import Poll, Choice
from django.core.urlresolvers import reverse
from django.template import RequestContext

# Create your views here.
"""
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('index.html',
                            {'latest_poll_list': latest_poll_list})

def detail(request, poll_id):
    p = get_object_or_404(Poll, pk = poll_id)
    return render_to_response('detail.html', {'poll': p},
                            context_instance = RequestContext(request))

def results(request, poll_id):
    p = get_object_or_404(Poll, pk = poll_id)
    return render_to_response('results.html', {'poll': p})
"""
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk = poll_id)
    try:
        selected_choice = p.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Poll 投稿フォームを再表示します。
        return render_to_response('detail.html', {
            'poll': p,
            'error_message': '選択肢を選んでいません',
            }, context_instance = RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        """
        ユーザーがbackボタンを押して同じフォームを提出するのを防ぐ為、
        POSTデータを処理できた場合には必ずHttpResponseRedirectを返すようにする。
        """
        return HttpResponseRedirect(reverse('poll_results', args = (p.id,)))
