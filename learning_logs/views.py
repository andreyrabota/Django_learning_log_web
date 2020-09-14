from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your views here.

def check_topic_owner(topic_owner, request_user):
    if topic_owner != request_user:
        raise Http404


def index(request):
    return render(request, 'learning_logs/index.html')

@login_required()
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date') # variable with query to database

    context = {'topics': topics} # context  {'thing_in_template': variable_in_view}
    return render(request, 'learning_logs/topics.html', context)


@login_required()
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id) # select * from Topic where id=topic_id
    check_topic_owner(topic.owner, request.user)
    entries = topic.entry_set.order_by() # query to select items via foreign key | join
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required()
def new_topic(request):
    """diescribes new topic"""
    if request.method != 'POST':
        # data isnt sent - new empty form is created
        form = TopicForm()
    else:
        # send data POST
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user  # check if current user is requesting this url
            new_topic.save()
            return redirect('learning_logs:topics') # redirect to previous page after form had been sent

    #show empty or nonfunctional form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required()
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # data isnt sent - new empty form is created
        form = EntryForm()
    else:
        # send data POST
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False) # just save form in variable but not commit
            new_entry.topic = topic # key to topic
            new_entry.save() # now save normally
            return redirect('learning_logs:topic', topic_id=topic_id)

    # show empty or nonfunctional form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required()
def edit_entry(request, entry_id):
    # view to edit entry
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic.owner, request.user)
    if request.method != "POST":
        form = EntryForm(instance=entry) # creates form filled with particular entry = entry_id
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

