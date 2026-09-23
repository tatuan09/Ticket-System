
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Ticket, Benutzer, Kategorie, Kommentar, TicketStatusHistorie
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

def get_benutzer_from_request(request):
    user_obj = User.objects.get(id=request.user.id)
    return Benutzer.objects.get(email=user_obj.email)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)

            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'login.html', {
            'error': 'E-Mail oder Passwort ist falsch.'
        })

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):

    benutzer = get_benutzer_from_request(request)

    if benutzer.rolle == 'Support':
        tickets = Ticket.objects.all().order_by('-erstellt_am')
    else:
        tickets = Ticket.objects.filter(
            benutzer=benutzer
        ).order_by('-erstellt_am')

    offene_tickets = tickets.filter(
        status='Offen'
    ).count()

    in_bearbeitung = tickets.filter(
        status='In Bearbeitung'
    ).count()

    geschlossene_tickets = tickets.filter(
        status='Geschlossen'
    ).count()

    alle_tickets = tickets.count()

    context = {
        'tickets': tickets,
        'offene_tickets': offene_tickets,
        'in_bearbeitung': in_bearbeitung,
        'geschlossene_tickets': geschlossene_tickets,
        'alle_tickets': alle_tickets,
        'benutzer': benutzer,
    }

    return render(request, 'index.html', context)


@login_required
def tickets_view(request):
    benutzer = get_benutzer_from_request(request)

    if benutzer.rolle == 'Support':
        tickets = Ticket.objects.all().order_by('-erstellt_am')
    else:
        tickets = Ticket.objects.filter(
            benutzer=benutzer
        ).order_by('-erstellt_am')

    status = request.GET.get('status')
    category = request.GET.get('category')
    search = request.GET.get('search')

    if status:
        tickets = tickets.filter(status=status)

    if category:
        tickets = tickets.filter(kategorie__name=category)

    if search:
        tickets = tickets.filter(titel__icontains=search)

    return render(request, 'tickets.html', {
        'tickets': tickets
    })

@login_required
def create_ticket_view(request):

    if request.method == 'POST':

        titel = request.POST.get('title')
        beschreibung = request.POST.get('description')
        kategorie_id = request.POST.get('category')
        prioritaet = request.POST.get('priority')

        # Kategorie aus der Datenbank holen
        kategorie = Kategorie.objects.get(
            kategorie_id=kategorie_id
        )

        # Eingeloggten Django-Benutzer holen
        user_obj = User.objects.get(
            id=request.user.id
        )

        # Benutzer aus unserer eigenen Benutzer-Tabelle holen
        benutzer = Benutzer.objects.get(
            email=user_obj.email
        )

        # Aktuelles Datum und Uhrzeit
        jetzt = timezone.now()

        # Neues Ticket erstellen
        Ticket.objects.create(
            titel=titel,
            beschreibung=beschreibung,
            status='Offen',
            prioritaet=prioritaet,
            erstellt_am=jetzt,
            aktualisiert_am=jetzt,
            benutzer=benutzer,
            kategorie=kategorie
        )

        return redirect('tickets')

    return render(request, 'create-ticket.html')

@login_required
def ticket_detail_view(request, ticket_id):

    ticket = Ticket.objects.get(
        ticket_id=ticket_id
    )

    user_obj = User.objects.get(
        id=request.user.id
    )

    benutzer = Benutzer.objects.get(
        email=user_obj.email
    )

    # User darf nur eigene Tickets sehen
    if benutzer.rolle != 'Support':
        if ticket.benutzer != benutzer:
            return redirect('tickets')

    if request.method == 'POST':

        kommentar_text = request.POST.get('comment')
        neuer_status = request.POST.get('status')

        # Kommentar hinzufügen
        if kommentar_text:

            Kommentar.objects.create(
                inhalt=kommentar_text,
                ticket=ticket,
                benutzer=benutzer
            )

        # Status ändern - nur Support
        if (
            benutzer.rolle == 'Support'
            and neuer_status
            and neuer_status != ticket.status
        ):

            alter_status = ticket.status

            ticket.status = neuer_status
            ticket.aktualisiert_am = timezone.now()

            ticket.save(
                update_fields=[
                    'status',
                    'aktualisiert_am'
                ]
            )

            TicketStatusHistorie.objects.create(
                alter_status=alter_status,
                neuer_status=neuer_status,
                ticket=ticket,
                benutzer=benutzer
            )

        return redirect(
            'ticket_detail',
            ticket_id=ticket_id
        )

    comments = Kommentar.objects.filter(
        ticket_id=ticket_id
    ).order_by('erstellt_am')

    return render(request, 'ticket-detail.html', {
        'ticket': ticket,
        'comments': comments,
        'benutzer': benutzer
    })

@login_required
def einstellungen_view(request):
    print("EINSTELLUNGEN VIEW:", request.method)

    if request.method == 'POST':

        if 'change_password' in request.POST:

            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            user = authenticate(
                username=request.user.username,
                password=current_password
            )

            if user is None:
                return render(request, 'einstellungen.html', {
                    'password_error': 'Das aktuelle Passwort ist falsch.'
                })

            if new_password != confirm_password:
                return render(request, 'einstellungen.html', {
                    'password_error': 'Die neuen Passwörter stimmen nicht überein.'
                })

            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            return render(request, 'einstellungen.html', {
                'password_success': 'Das Passwort wurde erfolgreich geändert.'
            })

    return render(request, 'einstellungen.html')
