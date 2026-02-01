import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import TodoForm


N8N_WEBHOOK_URL = "https://priscila-sinewless-nonexpectantly.ngrok-free.dev/webhook-test/todo-create"

def todo_list(request):
    todos = Todo.objects.all().order_by('-created')
    return render(request, 'todos/todo_list.html', {'todos': todos})

def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save()

            # Send data to n8n
            payload = {
                "title": todo.title,
                "description": todo.description,
                # "status": todo.complete,
            }

            try:
                requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
            except requests.exceptions.RequestException:
                pass  # Never break user flow

            return redirect('todo_list')
    else:
        form = TodoForm()

    return render(request, 'todos/todo_create.html', {'form': form})

def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/todo_create.html', {'form': form})

def todo_delete(request, pk):
    todos = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todos.delete()
        return redirect('todo_list')
    else: 
        todos = todos
    return render(request, 'todos/todo_confirm_delete.html', {'todos': todos})
