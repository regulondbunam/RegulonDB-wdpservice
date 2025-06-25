# process_riset.py (Versión final esperada)
import pandas as pd
import numpy as np
import json
import sys # Usado en el bloque if __name__ == "__main__":
import io  # Usado por FastAPI para pasar el archivo
import traceback # Para errores detallados

def is_proximal(dist, min_val=-90, max_val=20):
    """Determina si una distancia es proximal."""
    try:
        dist_f = float(dist) # Convertir a float para comparación segura
        return min_val <= dist_f <= max_val
    except (ValueError, TypeError):
        # Si no se puede convertir a float (ej. si es 'Unknown' o NaN después de limpieza)
        return False

def calculate_region_stats_complete(group):
    """Calcula estadísticas para un grupo (promotor+sigma), incluyendo riTypesPresent."""
    try:
        # Las claves de agrupación (promoterID, sigmaFactor) vienen del índice del grupo.
        # Para obtener los valores originales que estaban en las columnas,
        # accedemos a la primera fila del grupo para esas columnas.
        # Esto es más robusto si df_selected se pasó completo a apply.
        
        # Si 'promoterID' y 'sigmaFactor' están en el índice del grupo (group.name)
        # pid, sigma_factor = group.name # group.name es una tupla con las claves de grupo
        pid = group['promoterID'].iloc[0] if 'promoterID' in group.columns and not group['promoterID'].empty else "Unknown_PID_Calc"
        sigma_factor = group['sigmaFactor'].iloc[0] if 'sigmaFactor' in group.columns and not group['sigmaFactor'].empty else "Unknown_SF_Calc"


        region_name = group['promoterName'].iloc[0] if 'promoterName' in group.columns and not group['promoterName'].empty else "Unknown_PName_Calc"
        
        tss_val = None
        if 'tss' in group.columns and not group['tss'].isnull().all():
            tss_mean = group['tss'].mean()
            if pd.notna(tss_mean):
                tss_val = tss_mean

        ri_types_in_group = sorted(list(set(group['riType'].dropna().unique())))

        regulators_list = sorted(list(group['regulatorName'].dropna().unique()))
        num_regulators = len(regulators_list)

        tf_roles = {}; num_activator_tfs = 0; num_repressor_tfs = 0; activator_has_repressing_ris = False
        for tf in regulators_list:
            tf_functions = set(group[group['regulatorName'] == tf]['riFunction'].unique())
            is_a = 'activator' in tf_functions; is_r = 'repressor' in tf_functions; role = 'unknown'
            if is_a and not is_r: role = 'activator'; num_activator_tfs += 1
            elif not is_a and is_r: role = 'repressor'; num_repressor_tfs += 1
            elif is_a and is_r: role = 'both'; activator_has_repressing_ris = True # Marcado si un TF tiene ambos roles
            tf_roles[tf] = role

        num_ris = len(group)
        num_ris_activators = (group['riFunction'] == 'activator').sum()
        num_ris_repressors = (group['riFunction'] == 'repressor').sum()

        proximal_group = group[group['is_proximal']] # is_proximal ya es booleano
        num_prox_ris = len(proximal_group)
        num_prox_ris_activators = (proximal_group['riFunction'] == 'activator').sum()
        num_prox_ris_repressors = (proximal_group['riFunction'] == 'repressor').sum()

        proximal_repressors = proximal_group[proximal_group['riFunction'] == 'repressor']
        one_prox_rep_per_tf = True
        if not proximal_repressors.empty and 'regulatorName' in proximal_repressors.columns:
            tf_prox_rep_counts = proximal_repressors.groupby('regulatorName').size()
            if (tf_prox_rep_counts > 1).any(): one_prox_rep_per_tf = False

        proximal_activators = proximal_group[proximal_group['riFunction'] == 'activator']
        same_tf_act = True # Asume True si no hay activadores proximales o solo uno
        if not proximal_activators.empty and 'regulatorName' in proximal_activators.columns:
            if len(proximal_activators['regulatorName'].unique()) > 1: same_tf_act = False
        elif proximal_activators.empty and num_ris_activators > 0 : # Si hay activadores, pero ninguno proximal
             same_tf_act = False # O True, según la definición estricta que necesites

        # --- Construcción del diccionario de estadísticas ---
        # NO incluimos promoterID ni sigmaFactor aquí, ya que vendrán del índice con reset_index()
        stats_dict = {
            "regionName": region_name,
            "tssPosition": tss_val if pd.notna(tss_val) else "Unknown",
            "regulators": regulators_list,
            "numRegulators": num_regulators,
            "riTypesPresent": ri_types_in_group,
            "numRIs": num_ris, "numRIsActivators": num_ris_activators, "numRIsRepressors": num_ris_repressors,
            "numProxRIs": num_prox_ris, "numProxRIsActivators": num_prox_ris_activators, "numProxRIsRepressors": num_prox_ris_repressors,
            "numActivatorTFs": num_activator_tfs, "numRepressorTFs": num_repressor_tfs,
            "activatorHasRepressingRIs": activator_has_repressing_ris,
            "oneProximalRepressorPerTF": one_prox_rep_per_tf, "sameTFforAllActivatingRIs": same_tf_act,
        }
        # Convertir tipos numpy a nativos para JSON
        final_stats = {}
        for key, value in stats_dict.items():
            if isinstance(value, np.generic): final_stats[key] = value.item()
            elif isinstance(value, (np.bool_)): final_stats[key] = bool(value)
            else: final_stats[key] = value
        return pd.Series(final_stats)

    except Exception as e:
        print(f"Error en calculate_region_stats_complete para un grupo: {e}")
        print(traceback.format_exc())
        # Devolver una Serie con un indicador de error para este grupo
        error_keys = ["regionName", "tssPosition", "regulators", "numRegulators", "riTypesPresent", "numRIs", "numRIsActivators", "numRIsRepressors", "numProxRIs", "numProxRIsActivators", "numProxRIsRepressors", "numActivatorTFs", "numRepressorTFs", "activatorHasRepressingRIs", "oneProximalRepressorPerTF", "sameTFforAllActivatingRIs"]
        error_dict = {key: f"ERROR_IN_GROUP: {e}" for key in error_keys}
        return pd.Series(error_dict)


def process_file_content(file_like_object):
    """
    Procesa el TSV y devuelve dict {"stats": [...], "options": {...}} o dict {"error": ...}.
    """
    try:
        df = pd.read_csv(file_like_object, sep='\t', comment='#', low_memory=False)
        print(f"API: Archivo leído. {len(df)} filas iniciales.")
        print(f"API: Columnas leídas por Pandas: {df.columns.tolist()}") # Log CRUCIAL
    except Exception as e:
        return {"error": f"API Error: Leyendo TSV: {str(e)}"}

    try:
        required_cols = {
            '2)riType': 'riType',
            '4)regulatorName': 'regulatorName',
            '11)riFunction': 'riFunction',
            '12)promoterID': 'promoterID',
            '13)promoterName': 'promoterName',
            '15)sigmaF': 'sigmaFactor',
            '16)tfrsDistToPm': 'distToPm',
            '14)tss': 'tss'
        }
        actual_columns_in_df = df.columns.tolist()
        missing_cols = [col for col in required_cols.keys() if col not in actual_columns_in_df]
        if missing_cols:
            print(f"Error: Columnas requeridas faltantes: {missing_cols}.")
            print(f"Columnas encontradas en el archivo: {actual_columns_in_df}")
            return {"error": f"API Error: Columnas requeridas (SIN '#') faltantes en el archivo: {', '.join(missing_cols)}"}

        df_selected = df[list(required_cols.keys())].copy()
        df_selected.rename(columns=required_cols, inplace=True)
        print("API: Columnas seleccionadas/renombradas.")
    except Exception as e:
        print(f"Error seleccionando/renombrando: {e}")
        print(traceback.format_exc())
        return {"error": f"API Error: Seleccionando/Renombrando columnas: {e}"}

    # --- Limpieza ---
    df_selected['distToPm'] = pd.to_numeric(df_selected['distToPm'], errors='coerce').fillna(float('inf'))
    df_selected['riFunction'] = df_selected['riFunction'].str.lower().fillna('unknown')
    df_selected['sigmaFactor'] = df_selected['sigmaFactor'].fillna('Unknown')
    df_selected['regulatorName'] = df_selected['regulatorName'].astype(str).fillna('Unknown')
    df_selected['promoterID'] = df_selected['promoterID'].astype(str).fillna('Unknown_PID')
    df_selected['promoterName'] = df_selected['promoterName'].astype(str).fillna('Unknown_PName')
    df_selected['riType'] = df_selected['riType'].astype(str).fillna('Unknown')
    df_selected['tss'] = pd.to_numeric(df_selected['tss'], errors='coerce')
    print("API: Limpieza completada.")

    # --- Extraer Opciones Únicas ---
    try:
        unique_regulators = sorted(df_selected[df_selected['regulatorName'] != 'Unknown']['regulatorName'].unique().tolist())
        unique_ri_types = sorted(df_selected[df_selected['riType'] != 'Unknown']['riType'].unique().tolist())
        unique_sigmas = sorted(df_selected[df_selected['sigmaFactor'] != 'Unknown']['sigmaFactor'].unique().tolist())
        print("API: Opciones únicas extraídas.")
    except Exception as e: return {"error": f"API Error: Extrayendo opciones: {e}"}

    # --- Cálculo de Proximidad ---
    proximal_min_threshold = -90; proximal_max_threshold = 20
    df_selected['is_proximal'] = df_selected['distToPm'].apply(lambda x: is_proximal(x, proximal_min_threshold, proximal_max_threshold))

    # --- Agrupación (por promoterID y sigmaFactor) ---
    group_cols = ['promoterID', 'sigmaFactor']
    # Llenar NaNs en estas columnas (ya se hizo con fillna('Unknown') pero por si acaso)
    for col in group_cols:
        if col not in df_selected.columns:
            return {"error": f"API Error: Falta la columna de agrupación '{col}' antes de agrupar."}
        df_selected[col] = df_selected[col].fillna('Unknown')
    try:
        grouped = df_selected.groupby(group_cols, dropna=False)
        print(f"API: Datos agrupados en {len(grouped)} grupos.")
    except KeyError as e: return {"error": f"API Grouping error: {e}"}
    except Exception as e: return {"error": f"API Unexpected grouping error: {e}"}

    # --- Aplicar Cálculo de Estadísticas ---
    try:
        if grouped.ngroups == 0: final_results = []
        else:
            results_df = grouped.apply(calculate_region_stats_complete)
            # Las columnas 'promoterID' y 'sigmaFactor' ahora vienen del índice a través de reset_index()
            # y no deberían estar en las columnas de results_df antes de reset_index si
            # calculate_region_stats_complete no las devuelve explícitamente.
            final_results = results_df.reset_index().to_dict('records')
        print(f"API: Estadísticas calculadas para {len(final_results)} regiones.")
    except Exception as e:
        print(f"Error durante apply(calculate_region_stats_complete): {e}")
        print(traceback.format_exc())
        return {"error": f"API Error durante cálculo stats: {str(e)}"}

    return {
        "stats": final_results,
        "options": { "regulators": unique_regulators, "riTypes": unique_ri_types, "sigmas": unique_sigmas }
    }