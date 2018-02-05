import re

from django.shortcuts import render, redirect

from word.forms import WikiForm
from word.models import Word


def wiki(request, word):
    try:
        word = Word.objects.get(word=word)
    except Word.DoesNotExist:
        return redirect('create_wiki')
    description = word.description.split()
    new_description = list()
    relation_word_list = list()
    camel_re = re.compile("([A-Z]{1}[a-z]+)(([A-Z]{1}[a-z]+)+)")
    bracket_re = re.compile("\[([A-Za-z]+)\]")
    star_re = re.compile("\*([A-Za-z]+)\*")
    strike_re = re.compile("~([A-Za-z]+)~")
    underline_re = re.compile("_([A-Za-z]+)_")

    word_flat = Word.objects.values_list('word', flat=True)

    for des in description:
        if des.startswith(('http://', 'https://')):
            link_des = f'<a href={des}>{des}</a>'
            new_description.append(link_des)
        elif des in word_flat:
            des_in_word = Word.objects.get(word=des)
            link_des = f'<a href={des_in_word.get_absolute_url()}>{des}</a>'
            new_description.append(link_des)
        elif bool(camel_re.search(des)):
            link_des = f'<a href=/wiki/{des}>{des}</a>'
            new_description.append(link_des)
        elif bool(bracket_re.search(des)):
            m = re.search("([A-Za-z]+)", des)
            des = m.group(0)
            link_des = f'<a href=/wiki/{des}>{des}</a>'
            new_description.append(link_des)
        elif bool(star_re.search(des)):
            m = re.search("([A-Za-z]+)", des)
            des = m.group(0)
            bold_des = f'<b>{des}</b>'
            new_description.append(bold_des)
        elif bool(strike_re.search(des)):
            m = re.search("([A-Za-z]+)", des)
            des = m.group(0)
            strike_des = f'<s>{des}</s>'
            new_description.append(strike_des)
        elif bool(underline_re.search(des)):
            m = re.search("([A-Za-z]+)", des)
            des = m.group(0)
            underline_des = f'<span style="text-decoration: underline;">{des}</span>'
            new_description.append(underline_des)
        else:
            new_description.append(des)

    new_description = "<br>".join(new_description)

    for _word in description:
        if _word in word_flat:
            relation_word = Word.objects.get(word=_word)
            relation_word_list.append(relation_word)

    recommend_word = list()
    len_words = len(description)

    for _word in Word.objects.all():
        match = 0
        if _word == word:
            continue
        for rec_word in _word.description.split():
            if rec_word in description:
                match += 1
        if match >= len_words / 2:
            recommend_word.append(_word)

    ctx = {
        'word': word,
        'description': new_description,
        'relation_word_list': relation_word_list,
        'recommend_word': recommend_word,
    }

    return render(request, 'word/wiki.html', ctx)


def create_wiki(request):
    if request.method == "POST":
        form = WikiForm(request.POST)
        if form.is_valid():
            word = form.save()
            return redirect(word.get_absolute_url())
    else:
        form = WikiForm
    return render(request, 'word/create.html', {'form': form})


def recent(request):
    recent_word = Word.objects.order_by('-updated_at', '-created_at')
    return render(request, 'word/recent.html', {'recent_list': recent_word})