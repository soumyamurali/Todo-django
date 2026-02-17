from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo

def todo_list(request):
    filter_value = request.GET.get("filter", "all")

    todos = Todo.objects.all().order_by("-id")
    if filter_value == "pending":
        todos = todos.filter(is_completed=False)
    elif filter_value == "completed":
        todos = todos.filter(is_completed=True)

    if request.method == "POST" and request.POST.get("action") == "add":
        text = request.POST.get("text", "").strip()
        if text:
            Todo.objects.create(text=text, is_completed=False)
        return redirect(request.path + f"?filter={filter_value}")

    context = {
        "todos": todos,
        "filter": filter_value,
        "edit_form": None,
        "edit_id": None,
    }
    return render(request, "todo_list.html", context)

def toggle_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect(request.META.get("HTTP_REFERER", "todo_list"))

def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect(request.META.get("HTTP_REFERER", "todo_list"))


def update_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        new_text = request.POST.get("text", "").strip()
        if new_text:
            todo.text = new_text
            todo.save()
        return redirect("todo_list")
    return render(request, "todo_update.html", {"todo": todo})
