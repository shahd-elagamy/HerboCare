from django.shortcuts import render,redirect
from .models import Herb
from django.contrib import messages
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db import connection




# Create your views here.
def home(request):
    herbs = Herb.objects.all()
    return render(request,'core/home.html',
{'herbs':herbs})

# def recommend_view(request):
#     herbs = []
#     user_input = ""

#     if request.method == "POST":
#         user_input = request.POST.get("symptom", "").lower()
#         all_herbs = Herb.objects.all()

#         for herb in all_herbs:
#             if any(symptom.strip().lower() in herb.symptoms.lower() for symptom in user_input.split(',')):
#                 herbs.append(herb)

#     return render(request, 'core/recommendation.html', {'herbs': herbs, 'user_input':user_input})

def recommend_view(request): 
    herbs = []
    user_input = ""
    favorite_ids = []

    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT herb_id FROM herbocare_herb_favorited_by
                WHERE user_id = %s
            """, [request.user.id])
            favorite_ids = [row[0] for row in cursor.fetchall()]

    if request.method == "POST":
        user_input = request.POST.get("symptom", "")
        all_herbs = Herb.objects.all()

        if not all_herbs:
            return render(request, 'core/recommendation.html', {
                'herbs': [],
                'user_input': user_input,
                'favorite_ids': favorite_ids
            })

        herb_symptoms = [herb.symptoms for herb in all_herbs]

        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform(herb_symptoms + [user_input])
        similarity_scores = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

        for i, score in enumerate(similarity_scores):
            if score > 0.1:
                herbs.append((all_herbs[i], score))

        herbs.sort(key=lambda x: x[1], reverse=True)
        herbs = [herb[0] for herb in herbs]

    return render(request, 'core/recommendation.html', {
        'herbs': herbs,
        'user_input': user_input,
        'favorite_ids': favorite_ids
    })


# views.py
from django.shortcuts import render, get_object_or_404
from .models import Herb
from django.contrib.auth.decorators import login_required


@login_required
def herb_detail(request, herb_id):
    herb = get_object_or_404(Herb, id=herb_id)
    return render(request, 'core/herb_detail.html', {'herb': herb})



# from .models import Herb
# from django.shortcuts import get_object_or_404, redirect
# from core.models import Herb

# def add_to_favorites(request, herb_id):
#     herb = get_object_or_404(Herb, id=herb_id)
#     if request.user.is_authenticated:
#         herb.favorited_by.add(request.user)
#     return redirect('dashboard')
