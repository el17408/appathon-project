# :computer:  Appathon project for the course "Internet and Applications" 

# Περιγραφή Εργασίας
CTGOV-03: Χώρες στις οποίες έχουν λάβει χώρα Κλινικές Μελέτες γύρω από μία συγκεκριμένη Ασθένεια

# :book: Contents
Σκοπός να φτιάξουμε μία διαδικτυακή εφαρμογή που θα παρουσιάζει όλες τις χώρες στις οποίες έχουν λάβει χώρα κλινικές μελέτες για μία συγκεκριμένη Ασθένεια. Ως είσοδο θα λαμβάνει το όνομα της ασθένειας το οποίο θα το ορίζει ο χρήστης μέσω της web σελίδας ή κατάλληλου endpoint( π.χ. localhost:8080/appathon_project/index.html?search={Disease_Name}&format={map or json}) και το output θα είναι οι χώρες ταξινομημένες ανάλογα με τον αριθμό των κλινικών μελετών που έχουν λάβει χώρα ο οποίος θα παρουσιάζεται είτε ως json είτε με markers πάνω σε χάρτη.

Για τις ανάγκες της εφαρμογής αυτής κατεβάσαμε όλες τις διαθέσιμες κλινικές δοκιμές (XML αρχεία) από το https://clinicaltrials.gov/ ώστε να φιλτράρουμε τις κλινικές μελέτες με βάση την ασθένεια και έπειτα να εντοπίσουμε τις χώρες. Τις μελέτες αυτές θα τις προσθέσουμε σε βάση δεδομένων μετά από κατάλληλη επεξεργασία ώστε να κρατάμε τα εξής πεδία : official_title, brief_title , acronym , nct_id , country. Για να γίνει το parsing των δεδομένων δημιουργήθηκε κατάλληλο python script.

Εργαλεία :
  - MySQL,
  - html , css , javascript 
  - php (για επικοινωνία με βάση δεδομένων)
  - χρήση google maps api
  - api για μετατροπή ονόματος χώρας σε συντεταγμένες ώστε να τοποθετηθούν ως markers στον χάρτη (google geocoding) 

Επίσης υποστηρίζονται 2 formats:
  - Επιστροφή δεδομένων σε json μορφή
   [
     { "country_name": "...",
        "cnt" : ...,
        "lat" : ...,
        "lng" : ...
      }
      ...,
      {"status" : 200 ή "Zero_Results"}
   ]
  - Επίστροφή δεδομένων με markers πάνω σε χάρτη
# :pencil: Authors
The author of this project is: Roussis Dimitrios

# :book: Documentation
The powerpoint can be found in the Documentation folder
