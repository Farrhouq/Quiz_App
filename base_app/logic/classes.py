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


class PseudoScoreSet:
    def __init__(self, tup):
        self.position = tup[0]
        self.name = tup[1][0]
        self.score = tup[1][1]


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


class PseudoCategory:
    def __init__(self, category):
        self.name = category.name
        self.questions = [question for question in category.question_set.all()]
        self.id = category.id
