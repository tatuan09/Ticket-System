from django.db import models


class Benutzer(models.Model):
    benutzer_id = models.AutoField(
        primary_key=True,
        db_column='BenutzerID'
    )
    vorname = models.CharField(
        max_length=50,
        db_column='Vorname'
    )
    nachname = models.CharField(
        max_length=50,
        db_column='Nachname'
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        db_column='Email'
    )
    rolle = models.CharField(
        max_length=20,
        db_column='Rolle'
    )

    class Meta:
        db_table = 'Benutzer'
        managed = False

    def __str__(self):
        return f"{self.vorname} {self.nachname}"


class Kategorie(models.Model):
    kategorie_id = models.AutoField(
        primary_key=True,
        db_column='KategorieID'
    )
    name = models.CharField(
        max_length=50,
        db_column='Name'
    )
    beschreibung = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column='Beschreibung'
    )

    class Meta:
        db_table = 'Kategorie'
        managed = False

    def __str__(self):
        return self.name

    
class Ticket(models.Model):
    ticket_id = models.AutoField(
        primary_key=True,
        db_column='TicketID'
    )
    titel = models.CharField(
        max_length=150,
        db_column='Titel'
    )
    beschreibung = models.TextField(
        db_column='Beschreibung'
    )
    status = models.CharField(
        max_length=30,
        default='Offen',
        db_column='Status'
    )
    prioritaet = models.CharField(
        max_length=20,
        default='Normal',
        db_column='Prioritaet'
    )
    erstellt_am = models.DateTimeField(
        db_column='ErstelltAm'
    )
    aktualisiert_am = models.DateTimeField(
        db_column='AktualisiertAm'
    )

    benutzer = models.ForeignKey(
        Benutzer,
        on_delete=models.DO_NOTHING,
        db_column='BenutzerID'
    )

    kategorie = models.ForeignKey(
        Kategorie,
        on_delete=models.DO_NOTHING,
        db_column='KategorieID'
    )

    class Meta:
        db_table = 'Ticket'
        managed = False

    def __str__(self):
        return self.titel

class Kommentar(models.Model):
    kommentar_id = models.AutoField(
        primary_key=True,
        db_column='KommentarID'
    )
    inhalt = models.TextField(
        db_column='Inhalt'
    )
    erstellt_am = models.DateTimeField(
        auto_now_add=True,
        db_column='ErstelltAm'
    )

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.DO_NOTHING,
        db_column='TicketID'
    )

    benutzer = models.ForeignKey(
        Benutzer,
        on_delete=models.DO_NOTHING,
        db_column='BenutzerID'
    )

    class Meta:
        db_table = 'Kommentar'
        managed = False

    def __str__(self):
        return f"Kommentar #{self.kommentar_id}"


class TicketStatusHistorie(models.Model):
    historie_id = models.AutoField(
        primary_key=True,
        db_column='HistorieID'
    )
    alter_status = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        db_column='AlterStatus'
    )
    neuer_status = models.CharField(
        max_length=30,
        db_column='NeuerStatus'
    )
    geaendert_am = models.DateTimeField(
        auto_now_add=True,
        db_column='GeaendertAm'
    )

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.DO_NOTHING,
        db_column='TicketID'
    )

    benutzer = models.ForeignKey(
        Benutzer,
        on_delete=models.DO_NOTHING,
        db_column='BenutzerID'
    )

    class Meta:
        db_table = 'TicketStatusHistorie'
        managed = False

    def __str__(self):
        return f"Statusänderung #{self.historie_id}"