from django.shortcuts import render, redirect


def main(request):
    if request.user.is_authenticated:
        return redirect('/carplates')

    else:
        return render(request, 'main.html')
