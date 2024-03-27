"""
Récupérez les données (Pappers) du fichier csv et les preparer pour l'analyse
"""
import pandas as pd

# Adjusting the date processing to match the provided format (MM/YYYY)

def process_ubo_fixed(row):
    ubo_data_fixed = []
    for i in range(1, 20):  # Handling up to UBO 20
        nom = row.get(f'UBO {i} - Nom')
        prenom = row.get(f'UBO {i} - Prénom')
        dob = row.get(f'UBO {i} - Date de naissance', None)
        
        # Convert date of birth to datetime with correct format and handle missing values
        if pd.notnull(dob):
            try:
                dob_datetime = pd.to_datetime(dob, errors='coerce', format='%m/%Y')
                dob_formatted = dob_datetime.strftime('%Y-%m') if pd.notnull(dob_datetime) else None
            except:
                dob_formatted = None
        else:
            dob_formatted = None
        
        # Only create unique_id for entries with all required information
        if pd.notnull(nom) and pd.notnull(prenom) and dob_formatted:
            unique_id = f"{nom.upper()}_{prenom.upper()}_{dob_formatted}"
            ubo_data_fixed.append({'unique_id': unique_id, 'siren': row['siren']})
    return ubo_data_fixed

def fetch_data():
    """
    Récuperer les données du fichier csv et les filtrer par nom
    """
    pappers_data = pd.read_csv("data/univ-avignon.csv")

    # Apply the corrected function to each row and aggregate the results
    ubo_list_fixed = pappers_data.apply(process_ubo_fixed, axis=1).sum()  # Flatten the list of lists to a single list

    # Creating DataFrame from the processed list
    if ubo_list_fixed:
        ubo_df_fixed = pd.DataFrame(ubo_list_fixed)
        # Ensure 'unique_id' column exists before grouping
        if "unique_id" in ubo_df_fixed.columns:
            final_ubo_df_fixed = ubo_df_fixed.groupby("unique_id")["siren"].apply(list).reset_index()
        else:
            final_ubo_df_fixed = pd.DataFrame(columns=["unique_id", "siren"])
    else:
        final_ubo_df_fixed = pd.DataFrame(columns=["unique_id", "siren"])

    final_ubo_df_fixed.head()

    return final_ubo_df_fixed


