from task.models import Task

def notifications(request):
    allnotifications = Task.objects.all()

    return {'notifications':allnotifications}