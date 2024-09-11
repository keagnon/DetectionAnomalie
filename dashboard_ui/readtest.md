/* Styles généraux pour l'application */
[data-testid="stAppViewContainer"] {
    overflow: auto;
}
.stDataFrame div[data-testid="stHorizontalBlock"] {
    width: 100% !important;
}

/* Header fixable en haut de la page */
[data-testid="stHeader"] {
    position: relative !important;
    background: rgba(0, 0, 0, 0);
    z-index: 1 !important;
    top: auto;
}

/* Customisation du conteneur principal */
[data-testid="stAppViewContainer"] > .main {
    background-color: #F0F2F6;
    max-width: 100%;
    padding-left: 2rem;
    padding-right: 2rem;
    overflow: auto;
    position: relative !important;
}

/* Suppression de la position fixe de la toolbar */
[data-testid="stToolbar"] {
    right: 2rem;
    position: relative !important;
}

.block-container {
    padding: 5rem 1rem 2rem 1rem;
    max-width: 80%;
}

[data-testid="stSidebar"] > div:first-child {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    padding-top: 50px;
}

/* Customizing the selectbox (and multiselect) */
[data-testid="stSelectbox"], [data-testid="stMultiSelect"] {
    border: none !important;
    box-shadow: none !important;
    background-color: #F0F2F6 !important; /* Fond sombre */
    color: white !important;           /* Texte blanc */
    border-radius: 5px !important;     /* Coins arrondis */
    padding: 8px !important;           /* Espacement */
}

/* Customizing the internal appearance of the selectbox */
[data-testid="stSelectbox"] div[role="combobox"], [data-testid="stMultiSelect"] div[role="combobox"] {
    border: none !important;           /* Suppression des bordures internes */
    box-shadow: none !important;       /* Suppression des ombres */
    background-color: transparent !important; /* Fond transparent */
    color: white !important;           /* Texte blanc */
    padding: 0 !important;             /* Ajustement du padding */
}

/* Option dropdown styling */
[data-testid="stSelectbox"] select {
    background-color: transparent !important; /* Fond transparent pour la sélection */
    border: none !important;                  /* Suppression des bordures */
    color: white !important;                  /* Texte blanc */
}

/* Fix the inner dropdown arrow */
[data-testid="stSelectbox"]::after {
    border: none !important; /* Suppression des bordures autour de l'icône de la flèche */
}

/* Appliquer une bordure noire par défaut pour le champ 'Votre nom' */
.name-input input[type="text"] {
    border: 2px solid black !important;  /* Bordure noire */
    border-radius: 5px !important;       /* Coins arrondis */
    padding: 8px !important;
    box-shadow: none !important;         /* Suppression des ombres */
    background-color: #fff !important;   /* Fond blanc */
    color: #000 !important;              /* Texte noir */
}

/* Garder la bordure noire même au focus */
.name-input input[type="text"]:focus {
    border: 2px solid black !important;  /* Bordure noire persistante */
    outline: none !important;
}

/* Appliquer une bordure noire pour la zone de texte 'Vos commentaires / suggestions' */
.feedback-textarea textarea {
    border: 2px solid black !important;  /* Bordure noire */
    border-radius: 10px !important;      /* Coins arrondis pour la zone de texte */
    padding: 12px !important;
    box-shadow: none !important;
    background-color: #fff !important;   /* Fond blanc */
    color: #000 !important;              /* Texte noir */
}

/* Garder la bordure noire même au focus */
.feedback-textarea textarea:focus {
    border: 2px solid black !important;  /* Bordure noire persistante */
    outline: none !important;
}



/* Enlever le footer */
footer {
    visibility: hidden;
}
