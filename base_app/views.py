from contextlib import redirect_stderr
from multiprocessing import context
from pickletools import read_uint1
import re
from sre_parse import CATEGORIES
from unicodedata import name
from django.shortcuts import render, redirect
from . import models
from . import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.


def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    form = forms.UserForm()
    if request.method == "POST":
        name = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=name)
        except:
            return redirect("register")

        in_user = authenticate(username=name, password=password)
        if in_user != None:
            login(request, user)
            return redirect("home")
        else:
            return redirect("register")
    context = {"form": form, "page": page}
    return render(request, "login.html", context)


def register(request):
    page = "register"
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect("home")
    context = {"form": form, "page": page}
    return render(request, "register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def home(request):
    categories = [category for category in models.Category.objects.all()]
    last_category = categories.pop()
    context = {"categories": categories, "last_category": last_category}
    return render(request, "home.html", context)


def category(request, pk):
    category = models.Category.objects.get(id=pk)
    questions = category.question_set.all()
    context = {"questions": questions, "category": category}
    return render(request, "category.html", context)


def results(request):
    questions = []
    try:
        category = request.POST.get("category")
        category = models.Category.objects.get(name=category)
    except:
        return redirect('home')
    questions = category.question_set.all()

    class ResponseSet:
        def __init__(self, question, chosen):
            self.chosen = chosen
            self.question = question
            if self.chosen == question.answer:
                self.is_correct = True
            else:
                self.is_correct = False
            self.q = question.question
            self.correct_answer = question.answer
            if self.is_correct:
                self.points = question.points
            else:
                self.points = 0

            if chosen == "a":
                self.supp = question.a
            elif chosen == "b":
                self.supp = question.b
            elif chosen == "c":
                self.supp = question.c
            elif chosen == "d":
                self.supp = question.d
            elif chosen == "e":
                self.supp = question.e

            if question.answer == "a":
                self.correct_choice = question.a
            elif question.answer == "b":
                self.correct_choice = question.b
            elif question.answer == "c":
                self.correct_choice = question.c
            elif question.answer == "d":
                self.correct_choice = question.d
            elif question.answer == "d":
                self.correct_choice = question.e

    response_sets = []
    for question in questions:
        answer = request.POST.get(str(question.id))
        _ = ResponseSet(
            question,
            answer,
        )
        response_sets.append(_)
    score = 0
    for r in response_sets:
        score += r.points

    if request.user.is_authenticated:
        models.UserResults.objects.create(
            category=category, user=request.user, score=score
        )

    context = {
        "questions": questions,
        "response_sets": response_sets,
        "score": score,
        "category": category,
    }
    return render(request, "results.html", context)


def view_high_scores(request, pk):
    category = models.Category.objects.get(id=pk)
    high_scores = []
    for result_set in category.userresults_set.all():
        high_scores.append((result_set.user.username, result_set.score))

    class PseudoScoreSet:
        def __init__(self, tup):
            self.position = tup[0]
            self.name = tup[1][0]
            self.score = tup[1][1]

    def sort_tuples(tup):
        def sort_tuple_list(tup):
            nums = [b for (a, b) in tup]
            sorted_tuple_list = []
            while len(tup) != 0:
                least = max(nums)
                for tu in tup:
                    if tu[1] == least:
                        tup.remove(tu)
                        nums.remove(least)
                        sorted_tuple_list.append(tu)
            for _ in sorted_tuple_list:
                tup.append(_)
            return sorted_tuple_list

        def sort_tuple_list2(tup):
            nums = [b for (a, b) in tup]
            reps = {re for re in nums if nums.count(re) > 1}
            for rep in reps:
                nums = [b for (a, b) in tup]
                rep_count = nums.count(rep)
                occ1 = nums.index(rep)
                nums.reverse()
                occ2 = nums.index(rep)
                slise = tup[occ1 : len(tup) - occ2]
                slise.sort()
                tup[occ1 : len(tup) - occ2] = slise
            return tup

        tup = sort_tuple_list(sort_tuple_list2(tup))
        final_sorted = []
        nums = [b for (a, b) in tup]
        for num in nums:
            final_sorted.append(nums.index(num) + 1)
        fin = []
        for i in range(len(nums)):
            fin.append((final_sorted[i], tup[i]))
        return fin

    high_scores = list(set(high_scores))
    high_scores = sort_tuples(high_scores)
    pseudo_scores = []
    for score_set in high_scores:
        pseudo_scores.append(PseudoScoreSet(score_set))

    context = {
        "pseudo_scores": pseudo_scores,
        "category": category,
        "count": len(pseudo_scores),
        "name": category.name.upper(),
    }
    return render(request, "high_scores.html", context)


def inter(request):
    if not request.user.is_authenticated:
        return redirect("home")
    categories1 = models.Category.objects.all()
    categories = []

    class High:
        def __init__(self, category):
            self.name = category.name
            if len([_ for _ in category.userresults_set.all()]) > 0:
                self.highest_score = max(
                    [result.score for result in category.userresults_set.all()]
                )
            else:
                self.highest_score = 0
            self.id = category.id

    for category in categories1:
        # if len([ _ for _ in category.userresults_set.all()]) > 0:
        categories.append(High(category))
    return render(request, "inter_high.html", {"categories": categories})


def admin_panel(request):
    if not request.user.is_superuser:
        return redirect("home")
    categories = models.Category.objects.all()

    if request.method == "POST" and request.POST.get("name") != "":
        models.Category.objects.create(name=request.POST.get("name"))

    class PseudoCategory:
        def __init__(self, category):
            self.name = category.name
            self.questions = [question for question in category.question_set.all()]
            self.id = category.id

    pseudo_categories = []
    for category in categories:
        pseudo_categories.append(PseudoCategory(category))
    context = {"pseudo_categories": pseudo_categories}
    return render(request, "admin-panel.html", context)


def delete_question(request, pk):
    if not request.user.is_superuser:
        return redirect("home")
    question = models.Question.objects.get(id=pk)
    if request.method == "POST":
        question.delete()
        return redirect("admin_panel")
    return render(request, "delete.html", {"obj": "question"})


def add_to_category(request, pk):
    if not request.user.is_superuser:
        return redirect("home")
    category = models.Category.objects.get(id=pk)
    form = forms.QuestionForm()
    if request.method == "POST":
        models.Question.objects.create(
            question=request.POST.get("question"),
            a=request.POST.get("a"),
            b=request.POST.get("b"),
            c=request.POST.get("c"),
            d=request.POST.get("d"),
            e=request.POST.get("e"),
            answer=request.POST.get("answer"),
            category=category,
            points=request.POST.get("points"),
        )
        return redirect("admin_panel")
    context = {"form": form}
    return render(request, "specific.html", context)


def edit_question(request, pk):
    if not request.user.is_superuser:
        return redirect("home")
    question = models.Question.objects.get(id=pk)
    form = forms.QuestionForm(instance=question)
    if request.method == "POST":
        question.question = request.POST.get("question")
        question.a = request.POST.get("a")
        question.b = request.POST.get("b")
        question.c = request.POST.get("c")
        question.d = request.POST.get("d")
        question.e = request.POST.get("e")
        question.answer = request.POST.get("answer")
        question.points = request.POST.get("points")
        question.save()
        return redirect("admin_panel")
    return render(request, "edit_question.html", {"form": form})


def delete_category(request, pk):
    if not request.user.is_superuser:
        return redirect("home")
    category = models.Category.objects.get(id=pk)
    if request.method == "POST":
        category.delete()
        return redirect("admin_panel")
    return render(request, "delete.html", {"obj": "category"})


def edit_category(request, pk):
    if not request.user.is_superuser:
        return redirect("home")
    category = models.Category.objects.get(id=pk)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        return redirect("admin_panel")
    return render(request, "edit_category.html", {"category": category})


def reset_highscores(request, pk):
    if not request.user.is_superuser:
        return redirect("home")
    category = models.Category.objects.get(id=pk)
    if request.method == "POST":
        for result in category.userresults_set.all():
            result.delete()
        return redirect("view_high_scores", pk)
    return render(request, "reset.html", {"name": category.name})
