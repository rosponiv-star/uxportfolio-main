# Smart Home Hub · test veloce di usabilità (protocollo)

Scritto il 2026-10-30 per il PDF del Politecnico. Obiettivo: trasformare "nessuna verifica con utenti" in dati veri,
con 5 persone, 4 compiti, 25–30 minuti a persona, il prototipo Figma originale (schermate MD3 del report).

## 1. Cosa vogliamo sapere
1. Le persone riescono ad **aprire al corriere dal citofono** quando sono fuori casa? Lo slider per aprire è chiaro?
2. Riescono a **creare un codice temporaneo** per la babysitter, con giorni, orari e accessi giusti?
3. Quando provano a **inserire l'allarme con una finestra aperta**, capiscono il messaggio e sistemano il problema?
4. Capiscono **cosa è rimasto acceso** dopo essere usciti, e lo spengono?
5. Le scelte "prima la sicurezza" (slider invece dell'interruttore, conferma con "Annulla" in evidenza) aiutano o
   rallentano?

## 2. Partecipanti (5)
Bastano 5 persone per trovare la maggior parte dei problemi gravi (Nielsen). Coprire i profili delle personas:

| # | Profilo | Persona di riferimento |
|---|---|---|
| P1 | 25–40 anni, usa già app per la casa (luci, telecamere, Alexa…) | Marco |
| P2 | 25–40 anni, usa poco la tecnologia per la casa | Giorgia |
| P3 | Genitore con figli piccoli o con una babysitter | Valeria |
| P4 | Over 65, usa lo smartphone ma con cautela | Franco |
| P5 | Chiunque, meglio se vive da solo/a o rientra spesso tardi | Noemi |

Nessuno del team, nessuno che conosca il progetto. Amici di amici e parenti vanno bene.

## 3. Preparazione (una volta sola)
1. **Prototipo:** nel file Figma `PIG-Prototypes`, pagina *Design 1*, controllare in modalità Prototype che i 4 flussi
   siano cliccabili e abbiano un punto di partenza (Flow starting point) ciascuno:
   - **Compito 1, citofono:** *Notifica citofono* (schermata bloccata 9:30) → *Chiamata citofono* → slider per aprire il
     cancello → conferma.
   - **Compito 2, codice temporaneo:** *Codici temporanei* / *Codici permanenti* → schermate *Android Compact 10–19*
     (creazione: profilo, accessi cancello/porta, giorni, fascia oraria) → *Salva nuovo codice* → snackbar.
   - **Compito 3, allarme:** *Sicurezza - 3* → FAB "Arm alarm" → *Sicurezza errore* (snackbar: finestre aperte) →
     *Sicurezza errore risolto* → dialog di conferma → *Notifica casa protetta*.
   - **Compito 4, dimenticato acceso:** *Notifica luce dimenticata* → *Luci generale* → *Luci corridoio* → interruttore →
     *Luci corridoio spento*.
   Se un collegamento manca, va aggiunto (posso farlo io in Figma se me lo chiedi).
2. **Dispositivo:** telefono Android con l'app Figma (Mirror) o, in alternativa, il prototipo a schermo intero su
   laptop. Meglio il telefono: il gesto dello slider è parte del test.
3. **Registrazione:** registrazione dello schermo e dell'audio (con consenso). Se non è possibile, una seconda persona
   prende appunti.
4. **Materiale stampato:** le 4 schede compito (sotto), il modulo dei punteggi, il questionario SUS, il consenso.
5. **Prova generale** con una persona qualsiasi, per controllare i collegamenti e i tempi.

## 4. Copione della sessione (25–30 min)
**Benvenuto (2 min).** "Grazie. Stiamo provando un'app per gestire la casa, non stiamo provando te: se qualcosa non
funziona è colpa dell'app. Ti chiedo di pensare ad alta voce: dimmi cosa guardi, cosa ti aspetti, cosa ti confonde. È
un prototipo: alcune cose non funzionano, te lo dirò io. Possiamo registrare lo schermo e la voce? Le registrazioni
servono solo a noi e non saranno pubblicate."

**Contesto (1 min).** "Immagina di vivere in una casa con cancello, porta d'ingresso, luci e allarme collegati a
quest'app. L'app è già installata e configurata."

**Compiti (15–18 min).** Leggere lo scenario a voce e lasciare la scheda sul tavolo. Non usare mai le parole dei
pulsanti. Non aiutare: se la persona si blocca per più di 2 minuti, dire "Proviamo il prossimo" (conta come non
riuscito).

**Dopo ogni compito (20 s):** "Da 1 a 7, quanto è stato facile?" (SEQ: 1 = molto difficile, 7 = molto facile).

**Fine (5 min):** questionario SUS e 3 domande aperte.

## 5. I 4 compiti (schede da stampare)

**Compito 1 · Il corriere.** "Sei in ufficio. Ti arriva una notifica: qualcuno ha suonato al citofono di casa. È il
corriere con il pacco che aspettavi. Fallo entrare dal cancello, ma non dalla porta di casa."
- Riuscito se: risponde, vede il video, apre **solo il cancello** con lo slider.
- Osservare: capisce che deve trascinare? Prova a toccare? Sa quale ingresso ha suonato? Chiude la chiamata?

**Compito 2 · La babysitter.** "Da martedì la babysitter Anna viene il martedì e il giovedì, dalle 15 alle 19. Fai in
modo che possa aprire il cancello e la porta da sola, solo in quei giorni e in quegli orari."
- Riuscito se: crea un codice **temporaneo** legato ad Anna, con cancello + porta, martedì + giovedì, 15–19, e lo
  attiva.
- Osservare: distingue permanente/temporaneo? Trova i giorni e l'orario? Capisce "Salva e attiva" contro "Salva
  senza attivare"?

**Compito 3 · La notte.** "Stai andando a dormire. Inserisci l'allarme di casa."
- Riuscito se: prova a inserirlo, legge il messaggio sulle finestre aperte, capisce quale finestra, la sistema e
  conferma.
- Osservare: legge la snackbar? Capisce cosa fare? Nel dialogo di conferma tocca per sbaglio "Annulla"? Si sente
  rassicurato o rallentato?

**Compito 4 · Uscito di corsa.** "Sei appena uscito di casa. Ti arriva una notifica. Controlla cosa è successo e
sistemalo."
- Riuscito se: apre la notifica, trova la luce rimasta accesa (corridoio) e la spegne.
- Osservare: usa la piantina o la lista? Capisce i colori delle stanze e acceso/spento?

## 6. Misure (per ogni persona e compito)
| Misura | Come |
|---|---|
| Riuscita | Sì / Con difficoltà / No |
| Tempo | dal "via" alla fine del compito, in secondi |
| Errori | tocchi sbagliati, strade sbagliate; segnare a parte gli **errori critici** (aprire la porta invece del cancello, inserire l'allarme senza volerlo, codice senza limiti) |
| Facilità (SEQ) | 1–7 dopo ogni compito |
| SUS | punteggio 0–100 a fine sessione |
| Citazioni | 1–2 frasi dette ad alta voce, parola per parola |

## 7. Questionario finale

**SUS** (1 = per niente d'accordo, 5 = del tutto d'accordo):
1. Penso che userei volentieri quest'app spesso.
2. Ho trovato l'app inutilmente complessa.
3. Ho trovato l'app facile da usare.
4. Penso che avrei bisogno dell'aiuto di un tecnico per usarla.
5. Ho trovato le varie funzioni ben integrate.
6. Ho trovato troppe incoerenze nell'app.
7. Immagino che la maggior parte delle persone impari a usarla molto in fretta.
8. Ho trovato l'app molto macchinosa da usare.
9. Mi sono sentito/a sicuro/a nell'usarla.
10. Ho dovuto imparare molte cose prima di riuscire a usarla.

Calcolo: domande dispari = (voto − 1), pari = (5 − voto); somma × 2,5. Media di riferimento: 68.

**Domande aperte:**
1. Qual è stato il momento più chiaro? E quello più confuso?
2. Daresti un codice di questa app alla tua babysitter, o a un corriere? Perché?
3. Cosa ti farebbe fidare di più di un'app che apre la porta di casa tua?

## 8. Modulo dei risultati (uno per persona, poi tutti in un foglio)
| Persona | Profilo | C1 riuscito | C1 s | C1 SEQ | C2 … | C3 … | C4 … | Errori critici | SUS | Citazione |
|---|---|---|---|---|---|---|---|---|---|---|

## 9. Analisi (dopo le 5 sessioni)
1. Per ogni compito: tasso di riuscita (es. 4/5), tempo medio, SEQ medio.
2. SUS medio.
3. Problemi: elenco unico, ognuno con quante persone l'hanno avuto e una gravità da 1 (cosmetico) a 4 (blocca o
   causa un errore critico).
4. I 2 problemi più gravi diventano **una piccola iterazione** (prima/dopo in Figma): è esattamente la slide
   "Prototipi" del PDF (testato → cambiato).

## 10. Cosa mandarmi
- Il foglio dei risultati (anche foto del modulo scritto a mano).
- Le citazioni più belle (2–3).
- 2–3 foto delle sessioni: mani sul telefono, niente volti se non c'è il consenso.
- Se possibile, i 2 problemi più gravi con lo screenshot della schermata.

## 11. Come entra nel PDF
- **Slide 07 Prototipi:** "Testato con 5 persone (25–80 anni)", i problemi trovati e l'iterazione prima/dopo.
- **Slide 09 Esito:** riuscita dei compiti (es. "4 compiti, 18/20 riusciti"), SUS medio, una citazione.
- Onestà: 5 persone su un prototipo cliccabile è un test di usabilità leggero, non uno studio; lo diciamo così.

## Consenso (da leggere e firmare)
"Accetto di partecipare a un test di un prototipo per un progetto universitario. Il test dura circa 30 minuti. Posso
fermarmi quando voglio. Lo schermo e la voce vengono registrati solo per l'analisi e non saranno pubblicati. Nel
portfolio potranno comparire risultati anonimi e foto delle mani, senza volto né nome."
Nome, data, firma.
