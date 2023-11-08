fist_list = ['Radagon', 'Maliketh', ' Radahn', 'Margit', 'Morgott', 'Mogh', 'Godfrey']


def golan():
    return "The VIP"


def dae():
    return "2nd hitless runner in here"


def migas():
    return "The texan"


def all_commands():
    return (' !dadjoke' + ' ' + ' !discord' + ' ' + ' !runs ' + ' ' + ' !LOPruns' + ' ' + ' !DSruns' + ' ' + '!addrun '
                                                                                                             'nameOfRun' +
            ' ' + ' !removerun nameofRun' + ' ' + '!addrunDS nameofRun' + ' ' + ' !addrunLOP nameOfRun' + ' ' + '!points' + ' ' + ' !fist' + ' ' + ' !roll ')


def jake():
    return "Its Jake. W Jake"


def fist():
    return str(', '.join(fist_list))

# @bot.command(name='quiz')
# active_question = {
#     "question": None,
#     "answer": None,
#     "asked_by": None
# }
# async def quiz(ctx, *, user_answer=None):
#     if user_answer is None:
#         await send_question(ctx)
#     else:
#         await check_answer(ctx, user_answer)
#
#
# async def send_question(ctx):
#     global is_question_active
#
#     if is_question_active:
#         # Send the active question to the new user
#         await ctx.send("Question: " + active_question["question"] + "asked by " + active_question["asked_by"])
#     else:
#         try:
#             question_data = all_quiz.find({"answered": False}, {"question": 1})
#             all_questions = [data["question"] for data in question_data]
#             if all_questions:
#                 random_question = random.choice(all_questions)
#                 quiz_answer_data = all_quiz.find_one({"question": random_question}, {"answer": 1})
#                 quiz_answer = quiz_answer_data["answer"]
#                 active_question["question"] = random_question
#                 active_question["answer"] = quiz_answer.lower().strip()
#                 active_question["asked_by"] = ctx.author.name
#                 is_question_active = True
#                 await ctx.send("Question: " + random_question + " *do !quiz answer* to answer")
#             else:
#                 await ctx.send("No questions available at the moment.")
#                 # Here write a method to make all the questions in the database set to false.
#         except Exception as e:
#             await ctx.send("An error occurred while retrieving the question. Please try again later.")
#
#
# # Checks if the answer is correct when the user answers
# async def check_answer(ctx, user_answer):
#     global is_question_active
#
#     if not is_question_active:
#         await ctx.send("No question is currently active.")
#         return
#
#     user_answer = user_answer.strip().lower()
#     user_answer_words = user_answer.split()
#
#     is_correct_answer = any(word in active_question["answer"] for word in user_answer_words)
#     if is_correct_answer:
#         await update_user_points(ctx.author.name, 10)
#         await ctx.send("@" + ctx.author.name + " Correct answer! Added 10 points.")
#         await mark_question_answered(active_question["question"])
#     else:
#         await ctx.send("@" + ctx.author.name + " Incorrect answer.")
#
#     is_question_active = False
#     active_question["question"] = None
#     active_question["answer"] = None
#     active_question["asked_by"] = None
#
#
# # Update the user points from the database.
# async def update_user_points(username, points_to_add):
#     query_user = {'user': username}
#     find_user = all_users.find_one(query_user)
#     if find_user:
#         user_points = find_user['points']
#         add_points = int(user_points) + points_to_add
#         new_points = {"$set": {"points": str(add_points)}}
#         all_users.update_one(query_user, new_points)
#     else:
#         new_user = {
#             'user': username,
#             'points': '110'
#         }
#         all_users.insert_one(new_user)
#
#
# #  Updates the status on database. If the question has been answered then it will not be repeated
# async def mark_question_answered(question):
#     set_question_as_answered = all_quiz.find_one({"question": question}, {"answered": 1})
#     set_answered_true = {"$set": {"answered": True}}
#     all_quiz.update_one(set_question_as_answered, set_answered_true)
